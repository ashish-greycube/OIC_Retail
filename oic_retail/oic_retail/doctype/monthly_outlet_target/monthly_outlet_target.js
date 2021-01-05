// Copyright (c) 2021, greycube and contributors
// For license information, please see license.txt

frappe.ui.form.on("Monthly Outlet Target", {
  refresh: function (frm) {},

  sales_person: function (frm) {
    //   set prospects on hand from Listed Retail Outlets for sales person
    frappe.db
      .count("Retail Outlet", {
        filters: { outlet_status: "Listed" },
      })
      .then((count) => {
        frm.set_value("prospects_on_hand", count);
      });
  },
});
