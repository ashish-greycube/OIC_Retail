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
        where_clause += [" fn.sales_person = %(sales_person)s"]
    if filters.get("from_date"):
        where_clause += ["fn.start_date >= %(from_date)s"]
    if filters.get("to_date"):
        where_clause += ["fn.end_date <= %(to_date)s"]
    where_clause = where_clause and " where " + " and ".join(where_clause) or ""

    data = frappe.db.sql(
        """
        with fn as
        (
            select mot.month, mot.year, mot.sales_person,prospects_on_hand outlets_planned, 
            monthly_listing_target, monthly_acquisition_target,
            str_to_date(concat(year,month,'01'),'%%Y%%b%%d') start_date,
            last_day(str_to_date(concat(year,month,'01'),'%%Y%%b%%d')) end_date
            from `tabMonthly Outlet Target` mot
        ) 
        select fn.sales_person, fn.year, fn.month, 
        max(fn.outlets_planned) outlets_planned,
        max(fn.monthly_listing_target) monthly_listing_target, 
        max( monthly_acquisition_target) monthly_acquisition_target,
        count(al.name) actual_listed,
        round(count(al.name)/(timestampdiff(DAY,fn.start_date, fn.end_date)+1)) listing_daily_avg,
        count(ro.name) actual_acquired,
        round(count(ro.name)/(timestampdiff(DAY,fn.start_date, fn.end_date)+1)) acquired_daily_avg
        from fn
        left outer join `tabRetail Outlet` al on al.sales_person = fn.sales_person
        and al.creation BETWEEN fn.start_date and fn.end_date
        and al.outlet_status = 'Listed'
        left outer join tabContract con on con.docstatus = 1 
        and con.start_date between fn.start_date and fn.end_date
        left outer join tabCustomer c on c.name = con.party_name
        left outer join `tabRetail Outlet` ro on ro.name = c.retail_outlet and ro.sales_person = fn.sales_person
            {where_clause}
        group by fn.sales_person, fn.start_date""".format(
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
