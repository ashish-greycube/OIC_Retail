# -*- coding: utf-8 -*-
# Copyright (c) 2021, GreyCube Technologies and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import json
import frappe
from frappe import _
from frappe.model.naming import make_autoname
from frappe.model.document import Document
from erpnext.selling.doctype.customer.customer import make_address
from frappe.utils import cint


class RetailOutlet(Document):
    def autoname(self):
        self.name = make_autoname(
            f"{self.state_abbreviation}.-.{self.city_abbreviation}.-.#"
        )

    def after_insert(self):
        if self.outlet_status == "Listed":
            self.make_customer()
            self.make_address()
            self.make_contact(
                {
                    "full_name": self.outlet_owner,
                    "mobile_no": self.contact_number,
                    "email_id": self.contact_email,
                    "is_primary_contact": 1,
                }
            )
            if self.manager:
                self.make_contact(
                    {
                        "full_name": self.manager,
                        "mobile_no": self.manager_contact,
                        "email_id": self.manager_email,
                        "is_primary_contact": 0,
                    }
                )

    def make_customer(self):
        customer_doc = frappe.new_doc("Customer")
        customer_doc.customer_name = self.outlet_name
        customer_doc.customer_type = "Company"
        customer_doc.customer_group = frappe.db.get_single_value(
            "Selling Settings", "customer_group"
        ) or frappe.db.get_value("Customer Group", {"is_group": 0}, "name")

        customer_doc.territory = (
            self.territory
            or frappe.db.get_single_value("Selling Settings", "territory")
            or _("All Territories")
        )

        customer_doc.append(
            "sales_team",
            {"sales_person": self.sales_person, "allocated_percentage": 100},
        )
        customer_doc.retail_outlet_cf = self.name
        customer_doc.account_manager = frappe.session.user
        if frappe.db.exists("Customer Group", self.outlet_type):
            customer_doc.customer_group = self.outlet_type
        customer_doc.flags.ignore_mandatory = True
        customer_doc.save(ignore_permissions=True)

    def get_sales_person_for_user():
        sales_person = frappe.db.sql(
            """
                select sp.name
                from tabEmployee e
                inner join `tabSales Person` sp on sp.employee = e.name
                where e.user_id = %(user)s""",
            dict(user=frappe.session.user),
        )

        if not sales_person:
            frappe.throw("%s not associated with a Sales Person" % frappe.session.user)
        return sales_person[0][0]

    def make_address(self):
        make_address(
            {
                "doctype": "Customer",
                "name": self.outlet_name,
                "address_line1": self.address_line_1,
                "city": self.city,
                "state": self.state,
                "country": frappe.db.get_default("country"),
            },
            is_primary_address=1,
        )

    def make_contact(self, args):
        contact = frappe.get_doc(
            {
                "doctype": "Contact",
                "first_name": args.get("full_name"),
                "is_primary_contact": cint(args.get("is_primary_contact")) or 0,
                "links": [{"link_doctype": "Customer", "link_name": self.outlet_name}],
            }
        )
        if args.get("email_id"):
            contact.add_email(args.get("email_id"), is_primary=True)
        if args.get("mobile_no"):
            contact.add_phone(args.get("mobile_no"), is_primary_mobile_no=True)
        contact.insert()

        return contact

