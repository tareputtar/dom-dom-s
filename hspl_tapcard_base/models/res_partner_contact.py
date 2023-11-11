# Copyright 2023 HELICONIA SOLUTIONS PVT. LTD.
# License OPL-1 or later
# (https://www.odoo.com/documentation/15.0/legal/licenses.html#odoo-apps).

import uuid

from lxml import etree

from odoo import api, fields, models


class ResPartnerContact(models.Model):
    _name = "res.partner.contact"
    _description = "Contact"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char()
    first_name = fields.Char()
    last_name = fields.Char()
    partner_id = fields.Many2one("res.partner", string="Account")
    profile_id = fields.Many2one("res.partner", string="Profile")
    email = fields.Char()
    phone = fields.Char(string="Phone Number")
    position = fields.Char()
    company = fields.Char()
    notes = fields.Text(string="Profile note")
    card_ids = fields.Many2many(
        "res.partner.card",
        "contact_card_rel",
        "contact_id",
        "card_id",
        string="Card No.",
    )
    album_ids = fields.Many2many(
        "res.partner.album",
        "album_contact_rel",
        "contact_id",
        "album_id",
        string="Albums",
    )
    active = fields.Boolean(default=True)
    is_contact = fields.Boolean(default=False)
    title = fields.Many2one("res.partner.title")
    location = fields.Char()
    longitude = fields.Float()
    latitude = fields.Float()

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


class PartnerContactExport(models.TransientModel):

    _name = "res.partner.contact.export"
    _description = "Contact Export"

    name = fields.Char(required=1)
    contact_ids = fields.Json(required=1)
    is_export_vcf = fields.Boolean(default=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals["name"] = str(uuid.uuid4())[:16].replace("-", "")
        return super().create(vals_list)
