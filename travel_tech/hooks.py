app_name = "travel_tech"
app_title = "Travel Tech"
app_publisher = "shilparani"
app_description = "Travel Tech"
app_email = "shilpa@avohilabs.com"
app_license = "mit"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "travel_tech",
# 		"logo": "/assets/travel_tech/logo.png",
# 		"title": "Travel Tech",
# 		"route": "/travel_tech",
# 		"has_permission": "travel_tech.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/travel_tech/css/travel_tech.css"
# app_include_js = "/assets/travel_tech/js/travel_tech.js"

# include js, css files in header of web template
# web_include_css = "/assets/travel_tech/css/travel_tech.css"
# web_include_js = "/assets/travel_tech/js/travel_tech.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "travel_tech/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "travel_tech/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# automatically load and sync documents of this doctype from downstream apps
# importable_doctypes = [doctype_1]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "travel_tech.utils.jinja_methods",
# 	"filters": "travel_tech.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "travel_tech.install.before_install"
# after_install = "travel_tech.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "travel_tech.uninstall.before_uninstall"
# after_uninstall = "travel_tech.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "travel_tech.utils.before_app_install"
# after_app_install = "travel_tech.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "travel_tech.utils.before_app_uninstall"
# after_app_uninstall = "travel_tech.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "travel_tech.notifications.get_notification_config"

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

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }
doc_events = {
    "Travel Policy": {
        "after_insert": "travel_tech.custom.api.policy.upload_policy_to_external_api",
        "on_update": "travel_tech.custom.api.policy.upload_policy_to_external_api"
    },
    "Employee": {
        "after_insert": [
            "travel_tech..custom.manager.user_creation.create_user_for_manager",
            "travel_tech.custom.manager.auto_user_permission.create_user_permission_for_hr_manager"
        ],
        "on_update": [
            "travel_tech.custom.manager.user_creation.create_user_for_manager",
            "travel_tech.custom.manager.auto_user_permission.create_user_permission_for_hr_manager"
        ]
    },
    "Travel Request": {
        "after_insert": "travel_tech.custom.manager.auto_submit_travel_request.auto_submit_travel_request"
    }
}




# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"travel_tech.tasks.all"
# 	],
# 	"daily": [
# 		"travel_tech.tasks.daily"
# 	],
# 	"hourly": [
# 		"travel_tech.tasks.hourly"
# 	],
# 	"weekly": [
# 		"travel_tech.tasks.weekly"
# 	],
# 	"monthly": [
# 		"travel_tech.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "travel_tech.install.before_tests"

# Extend DocType Class
# ------------------------------
#
# Specify custom mixins to extend the standard doctype controller.
# extend_doctype_class = {
# 	"Task": "travel_tech.custom.task.CustomTaskMixin"
# }

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "travel_tech.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "travel_tech.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["travel_tech.utils.before_request"]
# after_request = ["travel_tech.utils.after_request"]

# Job Events
# ----------
# before_job = ["travel_tech.utils.before_job"]
# after_job = ["travel_tech.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"travel_tech.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

fixtures = [
    "Custom Field",
    "Property Setter",
    "Workflow",
    "Workflow State",
    "Workflow Action Master",
    "Role"
]

