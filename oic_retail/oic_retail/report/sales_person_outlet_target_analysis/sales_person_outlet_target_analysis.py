# Copyright (c) 2013, greycube and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe
from frappe.utils import add_days, add_months
import pandas


def execute(filters=None):
    return get_data(filters)


def get_data(filters):
    where_clause = []
    if filters.get("sales_person"):
        where_clause += [" mot.sales_person = %(sales_person)s"]
    if filters.get("month"):
        where_clause += ["mot.month = %(month)s"]
    if filters.get("year"):
        where_clause += ["mot.year = %(year)s"]
    where_clause = where_clause and " where " + " and ".join(where_clause) or ""

    data = frappe.db.sql(
        """
        select sales_person, month, year, 
        prospects_on_hand outlets_planned, monthly_listing_target, 0 actual_listed,
        monthly_acquisition_target, 0 actual_acquired
        from `tabMonthly Outlet Target` mot
        {where_clause}""".format(
            where_clause=where_clause
        ),
        filters,
        as_dict=True,
    )

    columns = [
        dict(
            label="Sales Person",
            fieldname="sales_person",
            fieldtype="Link",
            options="Sales Person",
            width=200,
        ),
        dict(label="Month", fieldname="month", fieldtype="Data", width=100),
        dict(label="Year", fieldname="year", fieldtype="Int", width=100),
        dict(
            label="Outlets Planned",
            fieldname="outlets_planned",
            fieldtype="Int",
            width=120,
        ),
        dict(
            label="Listing Target",
            fieldname="monthly_listing_target",
            fieldtype="Int",
            width=120,
        ),
        dict(
            label="Actual Listed",
            fieldname="actual_listed",
            fieldtype="Int",
            width=120,
        ),
        dict(
            label="Acquisition Target",
            fieldname="monthly_acquisition_target",
            fieldtype="Int",
            width=120,
        ),
        dict(
            label="Actual Acquired",
            fieldname="actual_acquired",
            fieldtype="Int",
            width=120,
        ),
    ]

    return columns, data
