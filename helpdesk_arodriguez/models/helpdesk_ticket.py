from odoo import api, models, fields


class HelpdeskTicketAction(models.Model):
    _name = 'helpdesk.ticket.action'
    _description = 'Ticket Actions'

    name = fields.Char(required=True)
    date = fields.Date()
    ticket_id = fields.Many2one(
        comodel_name='helpdesk.ticket', 
        string='Ticket')


class HelpdeskTicketTag(models.Model):
    _name = 'helpdesk.ticket.tag'
    _description = 'Ticket Tags'

    name = fields.Char(
        string='Name', 
        required=True)
    ticket_ids = fields.Many2many(
        comodel_name='helpdesk.ticket', 
        string='Tickets')
    

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
        compute='_compute_assigner')
    deadline = fields.Date(
        string='Deadline')
    action_corrective = fields.Html(
        string='Corrective Action',
        help='Descrive corrective actions to do')
    action_preventive = fields.Html(
        string='Preventive Action',
        help='Descrive preventive actions to do')
    user_id = fields.Many2one(
        comodel_name='res.users', 
        string='Assign to')
    action_ids = fields.One2many(
        comodel_name='helpdesk.ticket.action',
        inverse_name='ticket_id',
        string='Actions')
    tag_ids = fields.Many2many(
        comodel_name='helpdesk.ticket.tag',
        string='Tags')
    ticket_qty = fields.Integer(
        string='Ticket Qty', 
        compute='_compute_ticket_qty')
    tag_name = fields.Char(
        string='Tag Name')
    
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
        
    @api.depends('user_id')
    def _compute_assigner(self):
        for record in self:
            record.assigned = self.user_id and True or False

    @api.depends('user_id')
    def _compute_ticket_qty(self):
        for record in self:
            other_tickets = self.env['helpdesk.ticket'].search([('user_id', '=', record.user_id.id)])
            record.ticket_qty = len(other_tickets)
    
    def create_tag(self):
        self.ensure_one()
        self.write({
            'tag_ids': [(0,0,{'name': self.tag_name})]
        })