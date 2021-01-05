# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "oic_retail"
app_title = "OIC Retail"
app_publisher = "greycube"
app_description = "Optical Retail"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "info@greycube.in"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/oic_retail/css/oic_retail.css"
# app_include_js = "/assets/oic_retail/js/oic_retail.js"

# include js, css files in header of web template
# web_include_css = "/assets/oic_retail/css/oic_retail.css"
# web_include_js = "/assets/oic_retail/js/oic_retail.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "oic_retail.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "oic_retail.install.before_install"
# after_install = "oic_retail.install.after_install"
after_migrate = "oic_retail.hook_methods.after_migrate"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "oic_retail.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Contract": {
		"on_submit": "oic_retail.hook_methods.on_submit_contract",
	}
}


# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"oic_retail.tasks.all"
# 	],
# 	"daily": [
# 		"oic_retail.tasks.daily"
# 	],
# 	"hourly": [
# 		"oic_retail.tasks.hourly"
# 	],
# 	"weekly": [
# 		"oic_retail.tasks.weekly"
# 	]
# 	"monthly": [
# 		"oic_retail.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "oic_retail.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "oic_retail.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "oic_retail.task.get_dashboard_data"
# }
