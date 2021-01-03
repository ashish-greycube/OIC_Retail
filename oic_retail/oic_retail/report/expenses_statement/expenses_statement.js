// Copyright (c) 2016, greycube and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Expenses Statement"] = {
  filters: [
    {
      fieldname: "from_date",
      label: __("From Date"),
      fieldtype: "Date",
      default: moment().startOf("month").add(15, "d").add(-1, "M"),
      reqd: 1,
    },
    {
      fieldname: "to_date",
      label: __("To Date"),
      fieldtype: "Date",
      default: moment().startOf("month").add(14, "d"),
      reqd: 1,
    },
    {
      fieldname: "employee",
      label: __("Employee"),
      fieldtype: "Link",
      options: "Employee",
    },
  ],
};
