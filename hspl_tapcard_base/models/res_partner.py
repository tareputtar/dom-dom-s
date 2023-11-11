# Copyright 2023 HELICONIA SOLUTIONS PVT. LTD.
# License OPL-1 or later
# (https://www.odoo.com/documentation/15.0/legal/licenses.html#odoo-apps).

import uuid

from odoo import api, fields, models


class Partner(models.Model):
    _inherit = "res.partner"

    album_count = fields.Integer(compute="_compute_album_count")
    card_count = fields.Integer(compute="_compute_card_count")
    contact_count = fields.Integer(compute="_compute_contact_count")
    profile_contact_count = fields.Integer(
        compute="_compute_profile_contact_count", store=True
    )
    contact_ids = fields.One2many(
        "res.partner.contact", "partner_id", string="Contacts"
    )
    profile_ids = fields.One2many(
        "res.partner.contact", "profile_id", string="Contacts"
    )
    card_ids = fields.One2many("res.partner.card", "partner_id", string="Cards")
    profile_card_ids = fields.One2many("res.partner.card", "profile_id", string="Cards")
    album_ids = fields.One2many("res.partner.album", "partner_id", string="Albums")
    contact_album_ids = fields.One2many(
        "res.partner.album", "profile_id", string="Albums"
    )
    profile_album_ids = fields.One2many(
        "res.partner.album", "profile_id", string="Albums"
    )
    is_account_partner = fields.Boolean(default=False)
    is_account_admin = fields.Boolean(default=False)
    uuid = fields.Char(string="UUID", readonly=True)
    cover_image = fields.Binary("Cover page")
    background_color = fields.Char("Page background color")
    text_color = fields.Char("Text color")
    button_bg_color = fields.Char("Button background color")
    button_text_color = fields.Char("Button text color")
    contain_bg_color = fields.Char("Contain background color")
    employee_edit_access = fields.Boolean("Employee Editing Access")
    name_req = fields.Boolean("Full name", readonly=True, default=True)
    email_req = fields.Boolean("Email Id")
    mobile_req = fields.Boolean("Mobile Number")
    position_req = fields.Boolean("Job title")
    company_name_req = fields.Boolean("Company name")
    consent_statement_req = fields.Boolean("Consent_statement")
    social_ids = fields.One2many(
        "res.partner.social", "partner_id", string="Social Media"
    )
    res_partner_profile_ids = fields.One2many(
        "res.partner.profile.view", "res_partner_id"
    )
    profile_view_count = fields.Integer(
        "Views", compute="_compute_profile_view_count", store=True
    )
    profile_count = fields.Integer(compute="_compute_profile_count", store=True)
    profile_album = fields.Integer(compute="_compute_profile_album")
    shared_profile_ids = fields.Many2many(
        "res.partner",
        "share_profile_contact_rel",
        "partner_id_col",
        "contact_id_col",
        string="Shared with",
        domain="[('parent_id', '=', parent_id), ('id', '!=', active_id)]",
    )
    account_contact_count = fields.Integer(compute="_compute_account_contact_count")
    account_card_count = fields.Integer(compute="_compute_account_card_count")
    contact_album_count = fields.Integer(compute="_compute_contact_album_count")
    profile_card_count = fields.Integer(compute="_compute_profile_card_count")
    reset_url = fields.Char(string="URL", compute="_compute_reset_url")

    def _compute_reset_url(self):
        base_url = (
            self.env["ir.config_parameter"].sudo().get_param("flutter.web.base.url")
        )
        for partner in self:
            partner.reset_url = (
                "{}/#/createPassword?uuid={}".format(base_url, partner.uuid) or ""
            )

    @api.depends("res_partner_profile_ids.count")
    def _compute_profile_view_count(self):
        self.profile_view_count = False
        for rec in self:
            partner_child_ids = self.env["res.partner.profile.view"].search(
                [("res_partner_id", "=", rec.id)]
            )
            total = 0
            for line in partner_child_ids:
                total += line.count
            rec.profile_view_count = total

    _sql_constraints = [
        ("contact_uid_uniq", "UNIQUE (uuid)", "Contact uid must be unique")
    ]

    @api.depends("child_ids")
    def _compute_profile_count(self):
        for rec in self:
            rec.profile_count = len(rec.child_ids)

    @api.depends("contact_ids")
    def _compute_contact_count(self):
        for rec in self:
            rec.contact_count = len(rec.contact_ids)

    @api.depends("album_ids")
    def _compute_album_count(self):
        for rec in self:
            rec.album_count = len(rec.album_ids)

    @api.depends("card_ids")
    def _compute_card_count(self):
        for rec in self:
            rec.card_count = len(rec.card_ids)

    @api.depends("contact_album_ids")
    def _compute_contact_album_count(self):
        for rec in self:
            rec.contact_album_count = len(rec.contact_album_ids)

    @api.depends("profile_card_ids")
    def _compute_profile_card_count(self):
        for rec in self:
            rec.profile_card_count = len(rec.profile_card_ids)

    @api.depends("profile_ids")
    def _compute_profile_contact_count(self):
        for rec in self:
            rec.profile_contact_count = len(rec.profile_ids)

    @api.depends("profile_album_ids")
    def _compute_profile_album(self):
        for rec in self:
            rec.profile_album = len(rec.profile_album_ids)

    def get_albums(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Albums",
            "view_mode": "tree,form",
            "res_model": "res.partner.album",
            "domain": [("partner_id", "=", self.id)],
            "context": {"admin_allow": True, "default_partner_id": self.id},
        }

    def get_card(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Cards",
            "view_mode": "tree,form",
            "res_model": "res.partner.card",
            "context": {"default_partner_id": self.id},
            "domain": [("partner_id", "=", self.id)],
        }

    def get_contact(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Contacts",
            "view_mode": "tree,form",
            "res_model": "res.partner.contact",
            "domain": [("partner_id", "=", self.id)],
            "context": {"default_partner_id": self.id},
        }

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get("uuid") or vals["uuid"]:
                vals["uuid"] = str(uuid.uuid4())[:16].replace("-", "")
        return super().create(vals_list)

    def write(self, vals):
        if vals.get("active") is False:
            users = self.env["res.users"].search([("partner_id", "in", self.ids)])
            if users:
                users.write({"active": False})
        res = super(Partner, self).write(vals)
        return res

    def action_view_profile(self):
        action = (
            self.env.ref("hspl_tapcard_base.action_res_partner_profile")
            .sudo()
            .read()[0]
        )
        context = self.env.context.copy()
        context.update(
            {
                "default_profile_id": self.id,
                "default_is_account_partner": False,
                "default_parent_id": self.id,
                "default_street": self.street,
                "default_street2": self.street2,
                "default_city": self.city,
                "default_state_id": self.state_id,
                "default_zip": self.zip,
                "default_country_id": self.country_id,
                "default_lang": self.lang,
                "default_type": "contact",
            }
        )
        action["context"] = context
        action["domain"] = [("id", "in", self.child_ids.mapped("id"))]
        return action

    def action_view_profile_contacts(self):
        action = self.env.ref(
            "hspl_tapcard_base.action_res_partner_contact_view"
        ).read()[0]
        context = self.env.context.copy()
        context.update(
            {
                "default_profile_id": self.id,
                "admin_allow": True,
                "default_partner_id": self.parent_id.id,
            }
        )
        action["context"] = context
        action["domain"] = [("profile_id", "=", self.id)]
        return action

    def action_view_profile_album(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Albums",
            "view_mode": "tree,form",
            "res_model": "res.partner.album",
            "domain": [("profile_id", "=", self.id)],
            "context": "{'create': False}",
        }

    def action_view_profile_cards(self):
        action = self.env.ref(
            "hspl_tapcard_base.action_res_partner_card_form_view"
        ).read()[0]
        action["context"] = {
            "default_profile_id": self.id,
            "admin_allow": True,
            "default_partner_id": self.parent_id.id,
        }
        action["domain"] = [("profile_id", "=", self.id)]
        return action

    def action_view_profile_albums(self):
        action = (
            self.env.ref("hspl_tapcard_base.res_partner_album_form_view")
            .sudo()
            .read()[0]
        )
        action["context"] = {
            "default_profile_id": self.id,
            "admin_allow": True,
            "default_partner_id": self.parent_id.id,
        }
        action["domain"] = [("profile_id", "=", self.id)]
        return action

    def _compute_account_contact_count(self):
        contacts_env = self.env["res.partner.contact"]
        account_contact_count = contacts_env.search([("partner_id", "=", self.id)])
        for rec in self:
            rec.account_contact_count = len(account_contact_count)

    def _compute_account_card_count(self):
        contacts_env = self.env["res.partner.card"]
        account_card_count = contacts_env.search([("partner_id", "=", self.id)])
        for rec in self:
            rec.account_card_count = len(account_card_count)

    def flutter_action_send_email(self):
        mail_template = self.sudo().env.ref(
            "hspl_tapcard_base.flutter_reset_password_emails_template"
        )
        user_id = self.env["res.users"].search([("partner_id", "=", self.id)], limit=1)
        mail_template.with_context(is_custom_mail_send=False).send_mail(
            user_id.id, force_send=True
        )
