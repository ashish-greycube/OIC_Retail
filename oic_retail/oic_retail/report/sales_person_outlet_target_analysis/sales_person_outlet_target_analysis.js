// Copyright (c) 2016, greycube and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Sales Person Outlet Target Analysis"] = {
  filters: [
    {
      fieldname: "sales_person",
      label: __("Sales Person"),
      fieldtype: "Link",
      options: "Sales Person",
      reqd: 0,
    },
    {
      fieldname: "from_date",
      label: __("From"),
      fieldtype: "Date",
      reqd: 0,
      default: moment().startOf("month"),
    },
    {
      fieldname: "to_date",
      label: __("To"),
      fieldtype: "Date",
      reqd: 0,
      default: moment().endOf("month"),
    },
  ],
};
