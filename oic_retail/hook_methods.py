# -*- coding: utf-8 -*-
# Copyright (c) 2021, GreyCube Technologies and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import json
import frappe
from frappe import _


def on_submit_contract(doc, method):
    frappe.db.set_value("Customer", doc.party_name, "outlet_status_cf", "Acquired")
    outlet = frappe.db.get_value("Customer", doc.party_name, "retail_outlet_cf")
    if outlet:
        frappe.db.set_value("Retail Outlet", outlet, "outlet_status", "Acquired")


def on_cancel_contract(doc, method):
    frappe.db.set_value("Customer", doc.party_name, "outlet_status_cf", "Listed")
    outlet = frappe.db.get_value("Customer", doc.party_name, "retail_outlet_cf")
    if outlet:
        frappe.db.set_value("Retail Outlet", outlet, "outlet_status", "Listed")


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
            "dt": "Customer",
            "label": "Outlet Status",
            "fieldname": "outlet_status_cf",
            "fieldtype": "Select",
            "options": "Listed\nAcquired",
            "allow_in_quick_entry": 1,
            "translatable": 0,
            "insert_after": "retail_outlet_cf",
            "read_only": 1,
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
        {
            "doctype": "Customer Group",
            "customer_group_name": _("Retailer"),
            "is_group": 0,
            "parent_customer_group": _("All Customer Groups"),
        },
        {
            "doctype": "Customer Group",
            "customer_group_name": _("Eye Hospital"),
            "is_group": 0,
            "parent_customer_group": _("All Customer Groups"),
        },
        {
            "doctype": "Customer Group",
            "customer_group_name": _("Optometrist"),
            "is_group": 0,
            "parent_customer_group": _("All Customer Groups"),
        },
    ]
    for d in custom_fields:
        if not frappe.get_meta(d["dt"]).has_field(d["fieldname"]):
            frappe.get_doc(d).insert()
