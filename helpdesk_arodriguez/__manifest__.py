# Copyright 2021 AEODOO
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Helpdesk Alicia Rodriguez",
    "version": "14.0.1.0.0",
    "author": "Alicia Rodríguez",
    "license": "AGPL-3",
    "depends": [
        "base",
        "mail"
    ],
    "data": [
        "data/delete_tag_cron.xml",
        "security/helpdesk_security.xml",
        "security/ir.model.access.csv",
        "report/helpdesk_ticket_report_templates.xml",        
        "report/res_partner_report.xml",
        "report/helpdesk_ticket_report.xml",  
        "views/helpdesk_menu.xml",
        "wizards/create_ticket_view.xml",
        "views/helpdesk_views.xml",
        "views/helpdesk_tag_views.xml",        
    ],    
}
