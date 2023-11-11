# Copyright 2023 HELICONIA SOLUTIONS PVT. LTD.
# License OPL-1 or later
# (https://www.odoo.com/documentation/15.0/legal/licenses.html#odoo-apps).

from odoo import fields, models


class ResPartnerProfileView(models.Model):
    _name = "res.partner.profile.view"
    _description = (
        "Show Profile page views counts and short the data according to date."
    )

    count = fields.Integer("Views Count")
    track_date = fields.Date("Date")
    res_partner_id = fields.Many2one("res.partner", string="Contact")
    reference = fields.Char(related="res_partner_id.uuid")


class ResPartnerSocialMediaLink(models.Model):
    _name = "res.partner.social"
    _description = "Show Social media links inside Accounts."

    name = fields.Many2one(
        "res.partner.social.channel", string="Social channel", required=True
    )
    url = fields.Char("Social url", required=True)
    partner_id = fields.Many2one("res.partner", string="Partner")
    sequence = fields.Integer("Sequence id")


class ResPartnerSocialChannel(models.Model):
    _name = "res.partner.social.channel"
    _description = "Add social media to social ids"

    name = fields.Char(required=True)
