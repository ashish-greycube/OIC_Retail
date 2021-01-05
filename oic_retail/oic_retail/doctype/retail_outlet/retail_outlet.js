// Copyright (c) 2021, GreyCube Technologies and contributors
// For license information, please see license.txt

frappe.ui.form.on("Retail Outlet", {
  refresh: function (frm) {
    //
    if (frm.is_new()) {
      frappe.db.get_value(
        "Employee",
        { user_id: frappe.session.user },
        "name",
        (r) => {
          frappe.db.get_value(
            "Sales Person",
            { employee: r.name },
            "name",
            (t) => {
              frm.set_value("sales_person", t.name);
            }
          );
        }
      );
    }
    //
  },
});
