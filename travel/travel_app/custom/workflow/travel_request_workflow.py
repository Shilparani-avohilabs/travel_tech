import frappe

def ensure_roles_exist():
    """Ensure required roles (Employee, HR Manager) exist."""
    for role in ["Employee", "HR Manager"]:
        if not frappe.db.exists("Role", role):
            frappe.get_doc({
                "doctype": "Role",
                "role_name": role
            }).insert(ignore_permissions=True)
            frappe.logger().info(f"✅ Created missing Role: {role}")
    frappe.db.commit()


def ensure_workflow_actions_exist():
    """Ensure required workflow actions exist before using them."""
    for action in ["Submit", "Approve", "Reject"]:
        if not frappe.db.exists("Workflow Action Master", action):
            frappe.get_doc({
                "doctype": "Workflow Action Master",
                "workflow_action_name": action
            }).insert(ignore_permissions=True)
            frappe.logger().info(f"✅ Created missing Workflow Action: {action}")
    frappe.db.commit()


def execute():
    ensure_roles_exist()
    ensure_workflow_actions_exist()

    # Check if workflow already exists
    if frappe.db.exists("Workflow", "Travel Request Approval Workflow"):
        frappe.logger().info("⚠️ Workflow already exists. Skipping creation.")
        return

    # Define workflow states
    states = [
        {"state": "Draft", "doc_status": 0, "allow_edit": "Employee"},
        {"state": "Pending", "doc_status": 1, "allow_edit": "HR Manager"},
        {"state": "Approved", "doc_status": 1, "allow_edit": "HR Manager"},
        {"state": "Rejected", "doc_status": 1, "allow_edit": "HR Manager"},
    ]

    # Define transitions
    transitions = [
        {
            "state": "Draft",
            "action": "Submit",
            "next_state": "Pending",
            "allowed": "Employee",
            "allow_self_approval": 0
        },
        {
            "state": "Pending",
            "action": "Approve",
            "next_state": "Approved",
            "allowed": "HR Manager",
            "allow_self_approval": 0
        },
        {
            "state": "Pending",
            "action": "Reject",
            "next_state": "Rejected",
            "allowed": "HR Manager",
            "allow_self_approval": 0
        }
    ]

    # Create the workflow
    workflow = frappe.get_doc({
        "doctype": "Workflow",
        "workflow_name": "Travel Request Approval Workflow",
        "document_type": "Travel Request",
        "is_active": 1,
        "override_status": "status",
        "send_email_alert": 0,
        "states": states,
        "transitions": transitions
    })

    workflow.insert(ignore_permissions=True)
    frappe.db.commit()
    frappe.logger().info("✅ Created 'Travel Request Approval Workflow' successfully.")
