# Copyright 2023 HELICONIA SOLUTIONS PVT. LTD.
# License OPL-1 or later
# (https://www.odoo.com/documentation/15.0/legal/licenses.html#odoo-apps).

{
    "name": "TapCard Base",
    "version": "16.0.1.2.0",
    "author": "Heliconia Solutions Pvt. Ltd.",
    "website": "https://heliconia.io/",
    "category": "HSPL Card Base",
    "license": "OPL-1",
    "sequence": 0,
    "Summary": "A Module For Card Base",
    "depends": [
        "mail",
        "contacts",
        "sale",
        "board",
        "product",
        "hspl_custom_theme",
    ],
    "external_dependencies": {"python": ["vobject"]},
    "data": [
        "security/ir.model.access.csv",
        "security/res_group.xml",
        "security/hspl_partner_wise_reporting.xml",
        "data/ir_config.xml",
        "data/reset_password_template.xml",
        "views/menu.xml",
        "views/res_partner_contact_view.xml",
        "views/res_partner_account_view.xml",
        "views/res_partner_album_view.xml",
        "views/res_partner_card_view.xml",
        "views/res_partner_dashboard_view.xml",
        "views/profile_template.xml",
        "views/res_partner_social_view.xml",
    ],
    "assets": {
        "web.assets_frontend_tap_card_css": [
            "hspl_tapcard_base/static/css/nucleo-icons.css",
            "hspl_tapcard_base/static/css/font-awesome.css",
            "hspl_tapcard_base/static/css/argon-design-system.css",
            "hspl_tapcard_base/static/css/custom.css",
        ],
        "web.assets_frontend_tap_card_js": [
            # "hspl_tapcard_base/static/js/jquery.slim.min.js",
            # "hspl_tapcard_base/static/js/popper.min.js",
            # "hspl_tapcard_base/static/js/bootstrap.bundle.min.js",
            "hspl_tapcard_base/static/js/custom.js",
        ],
    },
    "installable": True,
    "application": True,
}
