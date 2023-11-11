# Copyright 2023 HELICONIA SOLUTIONS PVT. LTD.
# License OPL-1 or later
# (https://www.odoo.com/documentation/15.0/legal/licenses.html#odoo-apps).

from odoo import models


class MailTemplate(models.Model):
    _inherit = "mail.template"

    def send_mail(
        self,
        res_id,
        force_send=False,
        raise_exception=False,
        email_values=None,
        email_layout_xmlid=False,
    ):
        if self.env.context.get("is_custom_mail_send", False):
            return True
        return super(MailTemplate, self).send_mail(
            res_id, force_send, raise_exception, email_values, email_layout_xmlid
        )
