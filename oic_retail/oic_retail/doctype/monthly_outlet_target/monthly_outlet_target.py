# -*- coding: utf-8 -*-
# Copyright (c) 2021, greycube and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe
from frappe.model.document import Document


class MonthlyOutletTarget(Document):
    pass


@frappe.whitelist()
def get_cumulative__target_listing(sales_person, month, year):
    month_date = frappe.utils.getdate(
        frappe.utils.formatdate(f"{year}-{month}-01", "yyyy-MMM-dd")
    )

    cumulative_listing = frappe.db.sql(
        """
    select round(sum(monthly_listing_target)) tgt
    from `tabMonthly Outlet Target` mot
    where str_to_date(concat(year,month,'01'),'%%Y%%b%%d') < %s""",
        (month_date),
    )
    return cumulative_listing and cumulative_listing[0][0] or 0


@frappe.whitelist()
def get_cumulative_target_acquisition(sales_person, month, year):
    month_date = frappe.utils.getdate(
        frappe.utils.formatdate(f"{year}-{month}-01", "yyyy-MMM-dd")
    )

    cumulative_acquisition = frappe.db.sql(
        """
    select round(sum(monthly_acquisition_target)) tgt
    from `tabMonthly Outlet Target` mot
    where str_to_date(concat(year,month,'01'),'%%Y%%b%%d') < %s""",
        (month_date),
    )
    return cumulative_acquisition and cumulative_acquisition[0][0] or 0
