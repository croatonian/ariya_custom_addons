from odoo import _, api, models, fields
from odoo.exceptions import UserError
from datetime import datetime
import json, requests, logging, base64
_logger = logging.getLogger(__name__)

class Trip(models.Model):
    _name = 'ariya_trip_manager.trip'
    _inherit = ['mail.thread', 'tier.validation']  # <-- added
    _description = 'Trip'

    state = fields.Selection([
        ("draft", "Чорновик"),
        ("to_validate", "На Схваленні"),
        ("validated", "Схвалено"),
        ("done", "Завершено"),
        ("rejected", "Відхилено"),
    ], default="draft", string="Статус", tracking=True,
        compute="_compute_state", store=True, inverse="_inverse_state", copy=False, required=True, index=True)

    @api.depends("validation_status")
    def _compute_state(self):
        for rec in self:
            if rec.validation_status == "validated":
                rec.state = "validated"
            elif rec.validation_status == "rejected":
                rec.state = "rejected"
            elif rec.validation_status in ("waiting", "pending"):
                rec.state = "to_validate"
            else:  # "no"
                if rec.state not in ("done",):  # don’t overwrite finished trips
                    rec.state = "draft"

    def _inverse_state(self):
        for rec in self:
            if rec.state == "done":
                # no tier logic, allow manual override
                continue

    _state_from = ["draft", "to_validate"]
    _state_to = ["validated"]
    _tier_validation_state_field_is_computed = True
    _tier_validation_manual_config = False
    # _tier_validation_field = 'state'

    name = fields.Char(
        string='Назва',
        required=True,
        default='Відрядження',
        copy=False
    )

    date_from = fields.Date(string='Start date', default=fields.Date.today(), required=True)
    date_to = fields.Date(string='End date')

    destination_ids = fields.Many2many('res.country.state', string="Куди вiдрядження:", required=True)
    comment = fields.Text(string='Коментар')
    employees_ids = fields.Many2many('hr.employee', string='Співробітники', required=True)
    reason_for_trip_id = fields.Many2one('ariya_trip_manager.reason_for_trip', string='Мета відрядження', required=True)

    reason_for_trip_name = fields.Char(related='reason_for_trip_id.name', string='Мета відрядження')
    destination_names = fields.Char(compute='_compute_destination_names', string="Куди вiдрядження:")
    # employees_1c_ids = fields.Char(compute='_compute_employees_1c_ids', string="guid співробітників:")
    employees_1c_json = fields.Text(
        string="Employees 1C JSON",
        compute="_compute_employees_1c_json",
        store=True
    )

    author_1c_id = fields.Char(
        string="Author 1C Ref Key",
        readonly=True,
        copy=False
    )

    # @api.depends("create_uid")
    # def _compute_author_1c_id(self):
    #     for rec in self:
    #         employee = rec.create_uid.employee_id
    #         rec.author_1c_id = employee.ref_key if employee and employee.ref_key else False

    @api.depends('destination_ids')
    def _compute_destination_names(self):
        for record in self:
            if record.destination_ids:
                names = [name + " область" for name in record.destination_ids.mapped('name')]
                record.destination_names = ", ".join(names)
            else:
                record.destination_names = False

    @api.depends("employees_ids.ref_key")
    def _compute_employees_1c_json(self):
        for record in self:
            employees = []
            for ref in record.employees_ids.mapped("ref_key"):
                if ref:  # skip empty values
                    employees.append({
                        "EmployeeID": str(ref),
                        "TASK_ID": "",
                        "Parameter": ""
                    })
            record.employees_1c_json = json.dumps(employees, ensure_ascii=False)


    # -------------------------
    # Helpers
    # -------------------------
    # def _check_employees_trip_status(self, employee_commands):
    #     """Raise error if any selected employee is already on trip (on_trip_1c=True)."""
    #     if not employee_commands:
    #         return
    #
    #     emp_ids = []
    #     for command in employee_commands:
    #         if command[0] == 4:  # add single
    #             emp_ids.append(command[1])
    #         elif command[0] == 6:  # replace all
    #             emp_ids.extend(command[2])
    #
    #     if emp_ids:
    #         employees = self.env['hr.employee'].browse(emp_ids)
    #         busy_employees = employees.filtered(lambda e: e.on_trip_1c)
    #         if busy_employees:
    #             names = ", ".join(busy_employees.mapped("name"))
    #             raise UserError(_(
    #                 "Неможливо створити відрядження. "
    #                 "Наступні співробітники значаться як у відрядженні в 1С: %s"
    #             ) % names)


    def _check_employees_trip_status(self, employee_commands, date_from=None):
        """Send employees to 1C API and raise error if they are already on trip."""

        if not employee_commands:
            return

        emp_ids = []
        for command in employee_commands:
            if command[0] == 4:  # add existing
                emp_ids.append(command[1])
            elif command[0] == 6:  # replace all
                emp_ids.extend(command[2])

        if not emp_ids:
            return

        employees = self.env["hr.employee"].browse(emp_ids)
        payload = []

        # ✅ Use provided date_from (from vals or record) or fallback to now
        if isinstance(date_from, str):
            date_begin = fields.Datetime.from_string(date_from)
        else:
            date_begin = date_from

        # date_begin = date_from or fields.Datetime.now()
        date_begin_iso = date_begin.strftime("%Y-%m-%dT%H:%M:%S")
        # date_begin_iso = fields.Datetime.to_string(date_begin)

        for emp in employees:
            if not emp.ref_key:
                raise UserError(_("У співробітника %s відсутній ref_key для 1С.") % emp.name)

            payload.append({
                "EmployeeID": emp.ref_key,
                "DateBegin": date_begin_iso,
            })

        url = "http://1c8.ariya.poltava.ua/Accodoo/hs/data/employeesontrip"
        # config = self.env["ir.config_parameter"].sudo()
        username = "Дігтяр Є.А."  # 🔒 replace with your real generic login
        password = "1234"  # 🔒 replace with your real generic password

        auth_str = f"{username}:{password}"
        b64_auth = base64.b64encode(auth_str.encode("utf-8")).decode("utf-8")

        headers = {
            "Authorization": f"Basic {b64_auth}",
            "Content-Type": "application/json"
        }

        # response = requests.post(url, json=payload, headers=headers, timeout=30)
        _logger.info("1C Payload: %s", payload)
        try:
            response = requests.post(
                url,
                json=payload,
                headers=headers,
                timeout=30
            )
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise UserError(_("Помилка з'єднання з 1С: %s") % str(e))

        try:
            result = response.json()
        except ValueError:
            raise UserError(_("Некоректна відповідь від 1С: %s") % response.text)

        busy = []
        for emp in employees:
            emp_status = next((r for r in result if r.get("Employee") == emp.ref_key), None)
            if emp_status and emp_status.get("Status") == "В командировке":
                busy.append(emp.name)

        if busy:
            raise UserError(_(
                "Неможливо створити відрядження.\n"
                "Наступні співробітники вже у відрядженні (за даними 1С): %s"
            ) % ", ".join(busy))




    def _ensure_trip_name(self):
        """Append record ID to name if not already present."""
        for rec in self:
            if rec.name and not rec.name.endswith(str(rec.id)):
                rec.name = f"{rec.name} {rec.id}"

    # -------------------------
    # ORM overrides
    # -------------------------
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get("author_1c_id"):  # Записуємо guid автора
                user = self.env.user
                if user.employee_id and user.employee_id.ref_key:
                    vals["author_1c_id"] = user.employee_id.ref_key

            if vals.get("employees_ids"):
                self._check_employees_trip_status(vals["employees_ids"], vals["date_from"])

        records = super().create(vals_list)
        records._ensure_trip_name()
        return records

    # def write(self, vals):
    #     if "employees_ids" in vals:
    #         self._check_employees_trip_status(vals["employees_ids"])
    #
    #     res = super().write(vals)
    #     self._ensure_trip_name()
    #     return res
    #
    # def _on_validated(self):
    #     # """Custom logic when trip gets validated"""
    #     self.message_post(body="✅ Trip approved and confirmed!")
    #     # do whatever extra you need

    def _can_be_deleted(self):
        self.ensure_one()
        return self.state == "draft"

    def unlink(self):
        for request in self:
            if not request._can_be_deleted():
                raise UserError(
                    _("Ви не можете видалити відрядження що не знаходиться в статусі чорновик.")
                )
        return super().unlink()

    def button_done(self):
        return self.write({"state": "done"})

    # def button_save(self):
    #     return self.write({"state": "draft"})

    # Для валідації
    @api.model
    def _get_under_validation_exceptions(self):
        """Allow extra fields to be updated while record is under validation"""
        return super()._get_under_validation_exceptions() + [
            "author_1c_id",
            "state",
            "name"
        ]

    @api.model
    def _get_after_validation_exceptions(self):
        """Allow extra fields to be updated after validation"""
        return super()._get_after_validation_exceptions() + [
            "state"
        ]