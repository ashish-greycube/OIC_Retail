# -*- coding: utf-8 -*-
# Copyright (c) 2021, GreyCube Technologies and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import json
import frappe
from frappe.model.document import Document
from erpnext.accounts.doctype.sales_invoice.pos import make_customer_and_address
from erpnext.selling.doctype.customer.customer import make_address
from frappe.utils import cint


class RetailOutlet(Document):
    def validate(self):
        if self.is_new():
            self.make_customer()
            self.make_address()
            self.make_contact({
                'full_name': self.outlet_owner,
                "mobile_no": self.contact_number,
                "email_id": self.contact_email,
                'is_primary_contact': 1,
            })
            if self.manager:
                self.make_contact({
                    'full_name': self.manager,
                    "mobile_no": self.manager_contact,
                    "email_id": self.manager_email,
                    'is_primary_contact': 0,
                 })

    def make_customer(self):
        customer = make_customer_and_address({
                self.outlet_name: json.dumps({"full_name": self.outlet_name})
            })

        # sales_person = frappe.db.sql("""
        #         select sp.name
        #         from tabEmployee e
        #         inner join `tabSales Person` sp on sp.employee = e.name
        #         where e.user_id = %(user)s""", dict(user=frappe.session.user))

        # if not sales_person:
        #     frappe.throw("%s not associated with a Sales Person" % frappe.session.user)

        customer = frappe.get_doc("Customer", customer[0])
        customer.append("sales_team", {
        "sales_person": self.sales_person,
        "allocated_percentage": 100
        })
        customer.account_manager = frappe.session.user
        if self.territory:
            customer.territory = self.territory
        customer.save()

    def make_address(self):
        make_address({
                "doctype": "Customer",
                "name": self.outlet_name,
                "address_line1": self.address_line_1,
                "city": self.city,
                "state": self.state,
                "country": frappe.db.get_default("country")
            }, is_primary_address=1)

    def make_contact(self, args):
        contact = frappe.get_doc({
            'doctype': 'Contact',
            'first_name': args.get('full_name'),
            'is_primary_contact': cint(args.get("is_primary_contact")) or 1,
            'links': [{
                'link_doctype': 'Customer',
                'link_name': self.outlet_name
            }]
        })
        if args.get('email_id'):
            contact.add_email(args.get('email_id'), is_primary=True)
        if args.get('mobile_no'):
            contact.add_phone(args.get('mobile_no'), is_primary_mobile_no=True)
        contact.insert()

        return contact


def update_outlet_type(customer_name):
    outlet = frappe.get_all("Retail Outlet", {"outlet_name": customer_name})
    if outlet:
        frappe.db.set_value("Retail Outlet", outlet[0].name, "outlet_type", "Confirmed")
        frappe.db.commit()
