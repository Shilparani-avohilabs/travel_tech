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


def ensure_workflow_states_and_actions():
    """Ensure all required Workflow States and Actions exist with correct names."""
    # Define workflow states and styles
    states = {
        "Draft": "Warning",
        "Pending": "Info",
        "Approved": "Success",
        "Rejected": "Danger"
    }

    for state_name, style in states.items():
        if not frappe.db.exists("Workflow State", {"workflow_state_name": state_name}):
            state = frappe.get_doc({
                "doctype": "Workflow State",
                "workflow_state_name": state_name,
                "style": style
            })
            state.insert(ignore_permissions=True)
            frappe.db.set_value("Workflow State", state.name, "name", state_name)
            frappe.logger().info(f"✅ Created Workflow State: {state_name}")

    # Define workflow actions
    actions = ["Submit", "Approve", "Reject"]
    for action_name in actions:
        if not frappe.db.exists("Workflow Action", {"workflow_action_name": action_name}):
            action = frappe.get_doc({
                "doctype": "Workflow Action",
                "workflow_action_name": action_name
            })
            action.insert(ignore_permissions=True)
            # Force the 'name' to match so Frappe can find it during Workflow link validation
            frappe.db.set_value("Workflow Action", action.name, "name", action_name)
            frappe.logger().info(f"✅ Created Workflow Action: {action_name}")

    frappe.db.commit()
    frappe.clear_cache()


def execute():
    frappe.logger().info("	Create the Travel Request Approval Workflow if missing.")
    ensure_roles_exist()
    ensure_workflow_states_and_actions()

    if frappe.db.exists("Workflow", "Travel Request Approval Workflow"):
        frappe.logger().info("⚠️ Workflow already exists. Skipping creation.")
        return

    states = [
        {"state": "Draft", "doc_status": 0, "allow_edit": "Employee"},
        {"state": "Pending", "doc_status": 0, "allow_edit": "Employee"},
        {"state": "Approved", "doc_status": 1, "allow_edit": "HR Manager"},
        {"state": "Rejected", "doc_status": 1, "allow_edit": "HR Manager"},
    ]

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
