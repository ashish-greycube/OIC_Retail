// Copyright (c) 2021, greycube and contributors
// For license information, please see license.txt

frappe.ui.form.on("Monthly Outlet Target", {
  refresh: function (frm) {},

  month: function (frm) {
    update_listing_target(frm);
    update_acquisition_target(frm);
  },

  year: function (frm) {
    update_listing_target(frm);
    update_acquisition_target(frm);
  },

  monthly_listing_target: function (frm) {
    update_listing_target(frm);
  },

  monthly_acquisition_target: function (frm) {
    update_acquisition_target(frm);
  },

  sales_person: function (frm) {
    //   set prospects on hand from Listed Retail Outlets for sales person
    frappe.db
      .count("Retail Outlet", {
        filters: { outlet_status: "Listed" },
      })
      .then((count) => {
        frm.set_value("prospects_on_hand", count);
      });
    update_listing_target(frm);
  },
});

function update_listing_target(frm) {
  let total = frm.doc.monthly_listing_target;
  frappe.call({
    method:
      "oic_retail.oic_retail.doctype.monthly_outlet_target.monthly_outlet_target.get_cumulative__target_listing",
    args: {
      month: frm.doc.month,
      year: frm.doc.year,
      sales_person: frm.doc.sales_person,
    },
    callback: function (r) {
      frm.set_value(
        "cumulative__target_listing",
        flt(r.message) + flt(frm.doc.monthly_listing_target)
      );
    },
  });
}

function update_acquisition_target(frm) {
  let total = frm.doc.monthly_acquisition_target;
  frappe.call({
    method:
      "oic_retail.oic_retail.doctype.monthly_outlet_target.monthly_outlet_target.get_cumulative_target_acquisition",
    args: {
      month: frm.doc.month,
      year: frm.doc.year,
      sales_person: frm.doc.sales_person,
    },
    callback: function (r) {
      frm.set_value(
        "cumulative_target_acquisition",
        flt(r.message) + flt(frm.doc.monthly_acquisition_target)
      );
    },
  });
}
