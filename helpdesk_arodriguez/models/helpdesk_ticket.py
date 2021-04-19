from odoo import models, fields

class HelpdeskTicket(models.Model):
    _name = 'helpdesk.ticket'
    _description = 'Ticket'

    name = fields.Char(
        string='Name', 
        required=True)
    description = fields.Text(
        string='Description')
    date = fields.Date(
        string='Date')
    state = fields.Selection([
        ('new', 'New'),
        ('assigned', 'Assigned'),
        ('in_progress', 'In progress'),
        ('pending', 'Pending'),
        ('revolsed', 'Resolved'),
        ('canceled', 'Canceled')], 
        string='State',
        default='new')
    time = fields.Float(
        string='Time')
    assigned = fields.Boolean(
        string='Assigned',
        readonly=True)
    deadline = fields.Date(
        string='Deadline')
    action_corrective = fields.Html(
        string='Corrective Action',
        help='Descrive corrective actions to do')
    action_preventive = fields.Html(
        string='Preventive Action',
        help='Descrive preventive actions to do')
    
    #Asignar, cambia estado a asignado y pone a true el campo asignado, visible sólo con estado = nuevo
    def do_assign(self):
        self.ensure_one()
        self.write({
            'state': 'assigned',
            'assigned': True
        })
    
    def do_pending(self):
        self.ensure_one()
        self.state = 'pending'
    
    def do_resolved(self):
        self.ensure_one()
        self.state = 'resolved'
    
    def do_canceled(self):
        self.ensure_one()
        self.state = 'canceled'
        
