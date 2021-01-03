# -*- coding: utf-8 -*-
# Copyright (c) 2021, GreyCube Technologies and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import json
import frappe


def on_submit_contract(doc, method):
    from oic_retail.oic_retail.doctype.retail_outlet.retail_outlet import update_outlet_type
    update_outlet_type(doc.party_name)
