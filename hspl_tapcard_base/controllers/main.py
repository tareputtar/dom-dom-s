import csv
import tempfile
from datetime import date, datetime

import vobject

from odoo import _, http
from odoo.http import request


class ContactsIndividualUID(http.Controller):
    def _check_required_field_in_form(self, kw):
        error = dict()
        error_message = []

        # Required fields from form
        required_fields = [f for f in (kw.get("field_required") or "").split(",") if f]
        # error message for empty required fields
        for field_name in required_fields:
            if not kw.get(field_name):
                error[field_name] = "missing"

        if [err for err in error.values() if err == "missing"]:
            error_message.append(_("Some required fields are empty."))

        return error, error_message

    @http.route(
        "/view-profile/<string:uuid>",
        type="http",
        auth="public",
        website=True,
        csrf=False,
    )
    def partner_contact_template(self, uuid, **kw):
        errors = {}
        is_break = True
        partner_env = request.env["res.partner"].sudo()
        partner_id = partner_env.search([("uuid", "=", uuid)], limit=1)
        today_date = date.today()
        contact_profile_rec = partner_id.res_partner_profile_ids.filtered(
            lambda l: l.track_date == today_date
        )
        if contact_profile_rec:
            view = contact_profile_rec.count
            view += 1
            contact_profile_rec.write(
                {
                    "count": view,
                    "track_date": date.today(),
                }
            )

        else:
            partner_id.write(
                {
                    "res_partner_profile_ids": [
                        (
                            0,
                            0,
                            {"count": 1, "track_date": date.today(), "reference": uuid},
                        )
                    ]
                }
            )

        if not partner_id:
            return request.not_found()
        if "submitted" in kw:
            errors, error_msg = self._check_required_field_in_form(kw)
            if errors:
                errors["error_message"] = error_msg
                is_break = False
            if is_break:
                contact_form = request.env["res.partner.contact"]
                contact_form.create(
                    {
                        "first_name": kw.get("fname"),
                        "last_name": kw.get("lname"),
                        "email": kw.get("email"),
                        "phone": kw.get("phone"),
                        "position": kw.get("position"),
                        "company": kw.get("comp") or "",
                    }
                )
                # vcf_file = self.generate_vcf_file(kw)
                return http.request.render("hspl_tapcard_base.contacts_success")
            if error_msg:
                errors["error_message"] = error_msg
        contact_parent_id = partner_id.parent_id
        vals = {
            "contact": partner_id,
            "parent": contact_parent_id,
            "error": errors,
            "uuid": uuid,
        }
        return http.request.render("hspl_tapcard_base.contacts_page_uid", vals)

    @http.route(
        "/profile/vcf/download/<string:uuid>",
        type="http",
        auth="public",
        website=True,
        csrf=False,
    )
    def profile_data_fetch(self, uuid, **kw):
        partner_env = request.env["res.partner"].sudo()
        profile_rec = partner_env.search([("uuid", "=", uuid)], limit=1)
        if not profile_rec:
            return request.not_found()
        temp_dir = tempfile.mkdtemp()

        vcard = vobject.vCard()
        vcard.add("fn").value = profile_rec.name or ""
        if profile_rec.email_req:
            vcard.add("email").value = profile_rec.email or ""
        if profile_rec.mobile_req:
            vcard.add("phone").value = profile_rec.phone or ""
        if profile_rec.position_req:
            vcard.add("position").value = profile_rec.function or ""
        if profile_rec.company_name_req:
            vcard.add("company").value = (
                profile_rec.parent_id and profile_rec.parent_id.name or ""
            )
        vcf_file_name = profile_rec.name.lower().replace(" ", "_") + ".vcf"
        vcf_file_path = temp_dir + "/" + vcf_file_name

        with open(vcf_file_path, "w") as f:
            f.write(vcard.serialize())
            f.close()
        vcf_file_data = None

        vcf_file_data = open(vcf_file_path).read()

        headers = [
            ("Content-Type", "text/x-vcard"),
            ("Content-Disposition", 'attachment; filename="%s"' % vcf_file_name),
        ]

        return request.make_response(vcf_file_data, headers)

    @http.route(
        "/contact/vcf/download/<string:token>",
        type="http",
        auth="public",
        website=True,
        csrf=False,
    )
    def contact_export_vcf_download(self, token, **kw):
        contact_rec = (
            request.env["res.partner.contact.export"]
            .sudo()
            .search([("name", "=", token), ("is_export_vcf", "=", True)], limit=1)
        )
        contact_id = (
            request.env["res.partner.contact"]
            .sudo()
            .search([("id", "in", contact_rec.contact_ids)])
        )
        if not contact_id:
            return request.not_found()
        temp_dir = tempfile.mkdtemp()

        vcf_file_name = "contact_export_%s.vcf" % datetime.now().strftime(
            "%d_%m_%Y_%H_%M_%S"
        )
        vcf_file_path = temp_dir + "/" + vcf_file_name

        for contact in contact_id:
            vcard = vobject.vCard()
            vcard.add("fn").value = contact.name or ""
            vcard.add("email").value = contact.email or ""
            vcard.add("title").value = contact.position or ""
            vcard.add("tel").value = contact.phone or ""
            vcard.add("company").value = contact.company or ""
            vcard.add("note").value = contact.notes or ""
            with open(vcf_file_path, "a+") as f:
                f.write(vcard.serialize())
                f.close()

        vcf_file_data = None

        vcf_file_data = open(vcf_file_path).read()

        headers = [
            ("Content-Type", "text/x-vcard"),
            ("Content-Disposition", 'attachment; filename="%s"' % vcf_file_name),
        ]

        return request.make_response(vcf_file_data, headers)

    @http.route(
        "/contact/export/csv/<string:token>",
        type="http",
        auth="public",
        methods=["GET"],
        website=True,
        csrf=False,
    )
    def contact_export_csv_download(self, token, **kwargs):
        data = []
        export_record = request.env["res.partner.contact.export"].search(
            [("name", "=", token)], limit=1
        )

        contact_ids = request.env["res.partner.contact"].search(
            [("id", "in", export_record.contact_ids)]
        )
        for contact in contact_ids:
            contact_data = [
                contact.name or "",
                contact.position or "",
                contact.phone or "",
                contact.company or "",
                contact.email or "",
                contact.notes or "",
            ]
            data.append(contact_data)
        # if not profile_rec:
        temp_dir = tempfile.mkdtemp()

        # csv_file_name = profile_rec.name.lower().replace(" ", "_") + ".csv"
        csv_file_name = "contact_export_%s.csv" % datetime.now().strftime(
            "%d_%m_%Y_%H_%M_%S"
        )
        csv_file_path = temp_dir + "/" + csv_file_name

        with open(csv_file_path, "w", newline="") as file:
            # create a CSV writer object
            writer = csv.writer(file)
            # write the header row
            writer.writerow(["Name", "Position", "Phone", "Company", "Email", "Notes"])
            # write the data rows
            for row in data:
                writer.writerow(row)

        csv_file_data = open(csv_file_path).read()

        headers = [
            ("Content-Type", "text/csv"),
            ("Content-Disposition", 'attachment; filename="%s"' % csv_file_name),
        ]

        return request.make_response(csv_file_data, headers)
