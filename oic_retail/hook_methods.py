# -*- coding: utf-8 -*-
# Copyright (c) 2021, GreyCube Technologies and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import json
import frappe


def on_submit_contract(doc, method):
    from oic_retail.oic_retail.doctype.retail_outlet.retail_outlet import (
        update_outlet_type,
    )

    update_outlet_type(doc.party_name)


def after_migrate():
    custom_fields = [
        {
            "doctype": "Custom Field",
            "dt": "Customer",
            "label": "Retail Outlet",
            "fieldname": "retail_outlet_cf",
            "fieldtype": "Link",
            "options": "Retail Outlet",
            "allow_in_quick_entry": 1,
        },
        {
            "doctype": "Custom Field",
            "dt": "Territory",
            "label": "Territory Type",
            "fieldname": "territory_type_cf",
            "insert_after": "territory_manager",
            "fieldtype": "Link",
            "options": "Territory Type CT",
            "allow_in_quick_entry": 1,
        },
        {
            "doctype": "Custom Field",
            "dt": "Expense Claim Detail",
            "label": "Town Worked",
            "fieldname": "town_worked_cf",
            "insert_after": "travel_to_cf",
            "fieldtype": "Data",
            "depends_on": "eval:doc.expense_type == 'Travel';",
        },
        {
            "doctype": "Custom Field",
            "dt": "Expense Claim Detail",
            "label": "Travel To",
            "fieldname": "travel_to_cf",
            "insert_after": "travel_from_cf",
            "fieldtype": "Data",
            "depends_on": "eval:doc.expense_type == 'Travel'; ",
        },
        {
            "doctype": "Custom Field",
            "dt": "Expense Claim Detail",
            "label": "Travel From",
            "fieldname": "travel_from_cf",
            "insert_after": "section_break_4",
            "fieldtype": "Data",
            "depends_on": "eval:doc.expense_type == 'Travel';",
        },
    ]
    for d in custom_fields:
        if not frappe.get_meta(d["dt"]).has_field(d["fieldname"]):
            frappe.get_doc(d).insert()
