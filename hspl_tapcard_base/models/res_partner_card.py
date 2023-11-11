# Copyright 2023 HELICONIA SOLUTIONS PVT. LTD.
# License OPL-1 or later
# (https://www.odoo.com/documentation/15.0/legal/licenses.html#odoo-apps).

from lxml import etree

from odoo import api, fields, models


class ResPartnerCard(models.Model):
    _name = "res.partner.card"
    _description = "Card"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "name"

    name = fields.Char(string="Card Name", translate=True)
    card_no = fields.Char(string="Card No.", translate=True)
    partner_id = fields.Many2one("res.partner", string="Account")
    profile_id = fields.Many2one("res.partner", string="Profile")
    contact_ids = fields.Many2many(
        "res.partner.contact",
        "contact_card_rel",
        "card_id",
        "contact_id",
        string="Contacts",
        tracking=True,
    )
    active = fields.Boolean(default=True)

    @api.model
    def get_view(self, view_id=None, view_type="form", **options):
        result = super().get_view(view_id=view_id, view_type=view_type, **options)
        if self._context.get("admin_allow") and self.env.user.has_group(
            "base.group_system"
        ):
            if view_type == "form":
                doc = etree.XML(result["arch"])
                for node in doc.xpath("//form"):
                    node.set("create", "true")
                    node.set("delete", "true")
                result["arch"] = etree.tostring(doc, encoding="unicode")
            if view_type == "tree":
                doc = etree.XML(result["arch"])
                for node in doc.xpath("//tree"):
                    node.set("create", "true")
                    node.set("delete", "true")
                result["arch"] = etree.tostring(doc, encoding="unicode")
        else:
            if view_type == "form":
                doc = etree.XML(result["arch"])
                for node in doc.xpath("//form"):
                    node.set("create", "false")
                    node.set("delete", "false")
                result["arch"] = etree.tostring(doc, encoding="unicode")
            if view_type == "tree":
                doc = etree.XML(result["arch"])
                for node in doc.xpath("//tree"):
                    node.set("create", "false")
                    node.set("delete", "false")
                result["arch"] = etree.tostring(doc, encoding="unicode")
        return result
