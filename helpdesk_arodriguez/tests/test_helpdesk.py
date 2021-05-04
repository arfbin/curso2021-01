from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError


class TestHelpdesk(TransactionCase):
    def setUp(self):
        super(TestHelpdesk, self).setUp()

        self.ticket = self.env["helpdesk.ticket"].create({
            "name": "Ticket Test01"
        })
        self.user_id = self.env.ref("base.user_admin")
    
    def test_01_ticket(self):
        self.assertEqual(self.ticket.name, "Ticket Test01")
        self.ticket.user_id = self.user_id
        self.assertEqual(self.ticket.user_id, self.user_id)
    
    def test_02_ticket(self):
        self.ticket.time = 20
        self.assertEqual(self.ticket.time, 20)
        
        with self.assertRaises(ValidationError):
            self.ticket.time = -4
        