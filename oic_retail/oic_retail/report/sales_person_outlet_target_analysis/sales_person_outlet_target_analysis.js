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
      fieldname: "year",
      label: __("Year"),
      fieldtype: "Select",
      options: [2021, 2022, 2023, 2024, 2025, 2026, 2027, 2028, 2029, 2030],
      reqd: 0,
    },
    {
      fieldname: "month",
      label: __("Month"),
      fieldtype: "Select",
      options: "\nJan\nFeb\nMar\nApr\nMay\nJun\nJul\nAug\nSep\nOct\nNov\nDec",
    },

    ,
  ],
};
