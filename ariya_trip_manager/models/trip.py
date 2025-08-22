from odoo import _, api, models, fields
from odoo.exceptions import UserError

_STATES = [
    ("draft", "Чорновик"),
    ("to_validate", "На Схваленні"),
    ('validated', 'Схвалено'),
    ("done", "Завершено"),
    ("rejected", "Відхилено"),
]


class Trip(models.Model):
    _name = 'ariya_trip_manager.trip'
    _inherit = ['mail.thread', 'tier.validation']  # <-- added
    _description = 'Trip'

    state = fields.Selection(
        selection=_STATES,
        string="Статус",
        index=True,
        tracking=True,
        required=True,
        copy=False,
        default="draft",
    )

    _state_from = ["draft"]
    _state_to = ["validated"]

    _tier_validation_manual_config = False
    _tier_validation_field = 'state'


    name = fields.Char(string='Назва', required=True, default='Відрядження')

    date_from = fields.Date(string='Start date', default=fields.Date.today(), required=True)
    date_to = fields.Date(string='End date')

    destination_ids = fields.Many2many('res.country.state', string="Куди вiдрядження:", required=True)
    comment = fields.Text(string='Коментар')
    employees_ids = fields.Many2many('hr.employee', string='Співробітники', required=True)
    reason_for_trip_id = fields.Many2one('ariya_trip_manager.reason_for_trip', string='Мета відрядження', required=True)

    reason_for_trip_name = fields.Char(related='reason_for_trip_id.name', string='Мета відрядження')
    destination_names = fields.Char(compute='_compute_destination_names', string="Куди вiдрядження:")

    @api.depends('destination_ids')
    def _compute_destination_names(self):
        for record in self:
            if record.destination_ids:
                # Example: Join names of related records with a comma
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
