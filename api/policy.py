import frappe
import requests
import os
from PyPDF2 import PdfReader

def upload_policy_to_external_api(doc, method):
    """
    Upload Travel Policy PDF to external API and store its content in another Doctype (Policy Data)
    """
    try:
        if not doc.policy_file:
            frappe.throw("Please attach a PDF file before saving the Travel Policy.")

        # Get the File doc
        file_doc = frappe.get_doc("File", {"file_url": doc.policy_file})
        file_path = frappe.get_site_path(file_doc.file_url.strip("/"))

        if not os.path.exists(file_path):
            frappe.throw(f"File not found at path: {file_path}")

        # --- 1. Upload to external API ---
        with open(file_path, "rb") as pdf_file:
            response = requests.post(
                "https://1677945acfd9.ngrok-free.app/api/policy/upload",
                files={"pdf": pdf_file},
                timeout=30
            )

        # --- 2. Log and update response ---
        frappe.logger().info(f"External API Response: {response.status_code} - {response.text}")

        if response.status_code == 200:
            doc.api_response = "✅ Successfully uploaded to external API"
        else:
            doc.api_response = f"❌ Upload failed ({response.status_code}): {response.text}"
        doc.save(ignore_permissions=True)

        # --- 3. Read PDF Content ---
        pdf_reader = PdfReader(file_path)
        pdf_text = ""
        for page in pdf_reader.pages:
            pdf_text += page.extract_text() or ""

        # Optional: limit size if too long
        pdf_text = pdf_text[:5000]

        # --- 4. Create a new record in Doctype "Policy Data" ---
        policy_data_doc = frappe.get_doc({
            "doctype": "Policy Data",
            "policy_name": doc.name1,
            "company": doc.company,
            "file_content": pdf_text
        })
        policy_data_doc.insert(ignore_permissions=True)
        frappe.db.commit()

        frappe.msgprint("✅ Policy uploaded and content stored successfully in Policy Data Doctype.")

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Travel Policy Upload Error")
        frappe.throw(f"Error while uploading policy: {str(e)}")
