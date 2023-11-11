# Copyright 2023 HELICONIA SOLUTIONS PVT. LTD.
# License OPL-1 or later
# (https://www.odoo.com/documentation/15.0/legal/licenses.html#odoo-apps).

from odoo import api, models


class Country(models.Model):
    _inherit = "res.country"

    @api.model
    def _search(
        self,
        args,
        offset=0,
        limit=None,
        order=None,
        count=False,
        access_rights_uid=None,
    ):
        if self.env.context.get("search_specific_country", False):
            args.append(
                ("id", "in", [self.env.ref("base.nz").id, self.env.ref("base.au").id])
            )
        return super(Country, self)._search(
            args,
            offset=offset,
            limit=limit,
            order=order,
            count=count,
            access_rights_uid=access_rights_uid,
        )
