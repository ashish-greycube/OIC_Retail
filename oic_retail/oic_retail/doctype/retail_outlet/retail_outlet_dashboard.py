from __future__ import unicode_literals

from frappe import _


def get_data():
    return {
        "fieldname": "retail_outlet",
        "non_standard_fieldnames": {
            "Customer": "retail_outlet_cf",
            "Outlet Visit": "outlet",
        },
        "transactions": [
            {"label": _("Visits"), "items": ["Outlet Visit",],},
            {"label": _("Party"), "items": ["Customer",]},
        ],
    }
