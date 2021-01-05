from __future__ import unicode_literals
from frappe import _
import frappe


def get_data():
    config = [
        {
            "label": _("Documents"),
            "items": [
                {
                    "name": "Retail Outlet",
                    "type": "doctype",
                    "label": _("Retail Outlet"),
                },
                {
                    "name": "Outlet Visit",
                    "type": "doctype",
                    "label": _("Outlet Visit"),
                },
                {
                    "name": "Monthly Outlet Target",
                    "type": "doctype",
                    "label": _("Monthly Outlet Target"),
                },
            ],
        },
        {
            "label": _("Setup"),
            "items": [
                {"name": "City CT", "type": "doctype", "label": _("City"),},
                {"name": "State CT", "type": "doctype", "label": _("State"),},
                {
                    "name": "Territory Type CT",
                    "type": "doctype",
                    "label": _("Territory Type"),
                },
                {
                    "name": "Visit Activity",
                    "type": "doctype",
                    "label": _("Visit Activity"),
                },
            ],
        },
        {
            "label": _("Standard Reports"),
            "items": [
                {
                    "type": "report",
                    "name": "Expenses Statement",
                    "label": "Expenses Statement",
                    "is_query_report": True,
                },
            ],
        },
    ]
    return config
