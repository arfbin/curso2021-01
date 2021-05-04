from odoo import api, models, fields, _
from datetime import timedelta
from odoo.exceptions import ValidationError


class HelpdeskTicketAction(models.Model):
    _name = 'helpdesk.ticket.action'
    _description = 'Ticket Actions'

    name = fields.Char(required=True)
    date = fields.Date()
    ticket_id = fields.Many2one(
        comodel_name='helpdesk.ticket', 
        string='Ticket')
    time = fields.Float(
        string='Time')


class HelpdeskTicketTag(models.Model):
    _name = 'helpdesk.ticket.tag'
    _description = 'Ticket Tags'

    name = fields.Char(
        string='Name', 
        required=True)
    ticket_ids = fields.Many2many(
        comodel_name='helpdesk.ticket', 
        string='Tickets')

    @api.model
    def cron_delete_tag(self):
        result = self.search([('ticket_ids', '=', False)])
        result.unlink()


class HelpdeskTicket(models.Model):
    _name = 'helpdesk.ticket'
    _description = 'Ticket'
    _inherit = ['mail.thread.cc', 'mail.activity.mixin']

    def _date_default_today(self):
        return fields.Date.today()

    name = fields.Char(
        string='Name', 
        required=True)
    description = fields.Text(
        string='Description')
    date = fields.Date(
        string='Date',
        default=_date_default_today)
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
        compute='_get_time', 
        inverse='_set_time', 
        search='_search_time',
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
    partner_id = fields.Many2one(
        comodel_name='res.partner', 
        string='Partner')
    
    @api.constrains('time')
    def _verify_time(self):
        for record in self:
            if record.time and record.time < 0:
                raise ValidationError(_("The TIME can not be negative."))
    
    @api.onchange('date')
    def _onchange_date(self):
        self.deadline = self.date and self.date + timedelta(days=1)
    
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
    
    def do_canceled_multi(self):
        for record in self:
            record.do_canceled()
        
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
        #self.write({
        #   'tag_ids': [(0,0,{'name': self.tag_name})]
        #})
        action = self.env.ref('helpdesk_arodriguez.action_new_tag').read()[0]
        action['context'] = {
            'default_name': self.tag_name,
            'default_ticket_ids': [(6, 0 , self.ids)]
        }
        self.tag_name = False
        return action

    @api.depends('action_ids.time')
    def _get_time(self):
        for record in self:
            record.time = sum(record.action_ids.mapped('time'))
            
    def _set_time(self):
        for record in self:
            if record.time:
                time_now = sum(record.action_ids.mapped('time'))
                next_time = record.time - time_now
                if next_time:
                    data = {'name': '/', 'date': fields.Date.today(), 'time': next_time, 'ticket_id': record.id}
                    self.env['helpdesk.ticket.action'].create(data)
    
    def _search_time(self, operator, value):
        actions = self.env['helpdesk.ticket.action'].search[('time', operator, value)]
        return [('id', 'in', actions.mapped(ticket_id).ids)]


