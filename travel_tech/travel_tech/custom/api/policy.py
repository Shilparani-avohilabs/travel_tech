import frappe
import requests
import os
from PyPDF2 import PdfReader

def upload_policy_to_external_api(doc, method):
    """
    Upload Travel Policy PDF to external API and store its content in Policy Data Doctype.
    Works for both new and updated Travel Policy records.
    """
    try:
        logger = frappe.logger("travel_policy")
        logger.info(f"Triggered upload_policy_to_external_api for {doc.name} | Method: {method}")

        if not doc.policy_file:
            frappe.throw("Please attach a PDF file before saving the Travel Policy.")

        # 🧠 Avoid duplicate trigger only immediately after insert
        if method == "on_update" and getattr(frappe.flags, "skip_next_update_upload", False):
            logger.info("Skipping on_update trigger immediately after insert.")
            frappe.flags.skip_next_update_upload = False
            return

        # --- 1. Get file path ---
        file_doc = frappe.get_doc("File", {"file_url": doc.policy_file})
        file_path = frappe.get_site_path(file_doc.file_url.strip("/"))

        if not os.path.exists(file_path):
            frappe.throw(f"File not found at path: {file_path}")

        # --- 2. Upload PDF to external API ---
        with open(file_path, "rb") as pdf_file:
            response = requests.post(
                "https://1677945acfd9.ngrok-free.app/api/policy/upload",
                files={"pdf": pdf_file},
                timeout=30
            )

        logger.info(f"External API Response: {response.status_code} - {response.text}")

        if response.status_code == 200:
            api_response_msg = "✅ Successfully uploaded to external API"
        else:
            api_response_msg = f"❌ Upload failed ({response.status_code}): {response.text}"

        # --- 3. Read PDF Content ---
        pdf_reader = PdfReader(file_path)
        pdf_text = "".join(page.extract_text() or "" for page in pdf_reader.pages)
        pdf_text = pdf_text[:5000]

        # --- 4. Create or Update Policy Data ---
        existing_policy_data = frappe.db.exists("Policy Data", {"policy_name": doc.name1, "company": doc.company})

        if existing_policy_data:
            # Update existing
            policy_data_doc = frappe.get_doc("Policy Data", existing_policy_data)
            policy_data_doc.file_content = pdf_text
            policy_data_doc.save(ignore_permissions=True)
            action_message = "✅ Policy PDF updated successfully in Policy Data Doctype."
        else:
            # Create new
            frappe.get_doc({
                "doctype": "Policy Data",
                "policy_name": doc.name1,
                "company": doc.company,
                "file_content": pdf_text
            }).insert(ignore_permissions=True)
            action_message = "✅ New Policy uploaded and stored successfully in Policy Data Doctype."

            # 🧠 Mark next update to skip (only for this immediate system update)
            frappe.flags.skip_next_update_upload = True

        # --- 5. Update Travel Policy.api_response safely ---
        frappe.db.set_value("Travel Policy", doc.name, "api_response", api_response_msg)

        frappe.db.commit()
        frappe.msgprint(action_message)
        logger.info(action_message)

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Travel Policy Upload Error")
        frappe.throw(f"Error while uploading policy: {str(e)}")
