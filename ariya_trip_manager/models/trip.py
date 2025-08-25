from odoo import _, api, models, fields
from odoo.exceptions import UserError
# import logging
# _logger = logging.getLogger(__name__)

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

    @api.model_create_multi
    def create(self, vals):
        record = super().create(vals)
        if record.name and not record.name.endswith(str(record.id)):
            record.name = f"{record.name} {record.id}"
        return record

    def write(self, vals):
        res = super().write(vals)
        for rec in self:
            # if rec.state == "validated":
            #     rec._on_validated()
            if rec.name and not rec.name.endswith(str(rec.id)):
                rec.name = f"{rec.name} {rec.id}"
        return res

    def _on_validated(self):
        # """Custom logic when trip gets validated"""
        self.message_post(body="✅ Trip approved and confirmed!")
        # do whatever extra you need

    @api.depends('destination_ids')
    def _compute_destination_names(self):
        for record in self:
            if record.destination_ids:
                #Join names of related records with a comma
                names = [name + " область" for name in record.destination_ids.mapped('name')]
                record.destination_names = ", ".join(names)
            else:
                record.destination_names = False


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

    # Для валідації
    @api.model
    def _get_under_validation_exceptions(self):
        res = super()._get_under_validation_exceptions()
        return res

