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
from frappe.utils import cint, today


class RetailOutlet(Document):
    def validate(self):
        if self.outlet_status == "Acquired":
            if not frappe.db.exists(
                """
            select c.name, c.retail_outlet_cf 
                from tabCustomer c
                inner join tabContract con on con.docstatus = 1 and con.party_name = c.name 
                and c.retail_outlet_cf = %s
                and %s BETWEEN con.start_date and con.end_date""",
                (self.name, today()),
            ):
                frappe.throw(
                    "Cannot set Outlet Status to Acquired without an active Contract."
                )

    def after_insert(self):
        if self.outlet_status == "Listed":
            customer_doc = self.make_customer()
            address = self.make_address()
            contact = self.make_contact(
                {
                    "full_name": self.contact_name,
                    "phone": self.contact_phone,
                    "mobile_no": self.contact_mobile,
                    "email_id": self.contact_email,
                    "designation": self.designation,
                    "is_primary_contact": 1,
                }
            )

            customer_doc.update(
                {
                    "customer_primary_address": address.name,
                    "customer_primary_contact": contact.name,
                }
            )
            customer_doc.save()

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
        return customer_doc

    def make_address(self):
        return make_address(
            {
                "doctype": "Customer",
                "name": self.outlet_name,
                "address_line1": self.address_line_1,
                "address_line2": self.address_line_2,
                "city": self.city,
                "state": self.state,
                "country": frappe.db.get_default("country"),
                "pincode": self.pin_code,
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
        if args.get("phone"):
            contact.append(
                "phone_nos",
                {
                    "phone": args.get("phone"),
                    "is_primary_phone": 1,
                    "is_primary_mobile_no": 0,
                },
            )

        if args.get("mobile_no"):
            contact.append(
                "phone_nos",
                {
                    "phone": args.get("mobile_no"),
                    "is_primary_phone": 0,
                    "is_primary_mobile_no": 1,
                },
            )

        contact.insert()

        return contact

