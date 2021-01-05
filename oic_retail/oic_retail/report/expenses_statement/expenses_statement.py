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

    if filters.get("employee"):
        where_clause += [" ec.employee = %(employee)s"]
    # if filters.get("month"):
    #     filters["from_date"] = add_days(add_months(filters.get("from_date"), -1), 16)
    #     filters["to_date"] = add_days(filters.get("from_date"), 15)

    where_clause += ["ec.posting_date BETWEEN %(from_date)s and %(to_date)s"]
    where_clause = where_clause and " where " + " and ".join(where_clause) or ""

    data = frappe.db.sql(
        """
    select %(from_date)s + INTERVAL seq DAY `posting_date`, 
    ec.name `claim`, ecd.amount,
    ecd.expense_type,
    coalesce(ecd.description,'') description, 
     coalesce(ecd.town_worked_cf, '') town_worked_cf,
     coalesce(ecd.travel_from_cf, '') travel_from_cf,
     coalesce(ecd.travel_to_cf, '') travel_to_cf
    FROM seq_0_to_31
    left outer join `tabExpense Claim` ec on ec.posting_date = %(from_date)s + INTERVAL seq DAY
    left outer join `tabExpense Claim Detail` ecd on ecd.parent = ec.name
    {where_clause}
    order by seq, claim""".format(
            where_clause=where_clause
        ),
        filters,
        as_dict=True,
        debug=0,
    )

    if not data:
        return [], []

    df = pandas.DataFrame.from_records(data)
    df1 = pandas.pivot_table(
        df,
        index=[
            "posting_date",
            "claim",
            "description",
            "town_worked_cf",
            "travel_from_cf",
            "travel_to_cf",
        ],
        values=["amount"],
        columns=["expense_type"],
        fill_value="",
        margins=True,
        margins_name="Total",
        aggfunc=sum,
        dropna=True,
    )
    df1.drop(index="Total", axis=0)
    df1.columns = df1.columns.to_series().str[1]
    df2 = df1.reset_index()

    columns = [
        dict(label="Date", fieldname="posting_date", fieldtype="Date", width=100),
        dict(label="Town", fieldname="town_worked_cf", fieldtype="Data", width=100),
        dict(
            label="Travel From", fieldname="travel_from_cf", fieldtype="Data", width=100
        ),
        dict(label="Travel To", fieldname="travel_to_cf", fieldtype="Data", width=100),
        dict(
            label="Claim",
            fieldname="claim",
            fieldtype="Link",
            options="Expense Claim",
            width=180,
        ),
        dict(label="Description", fieldname="description", fieldtype="Data", width=200),
    ]
    for col in df1.columns.to_list():
        columns += [
            dict(label=col, fieldname=col, fieldtype="Currency", width=100),
        ]

    return columns, df2.to_dict("r")
