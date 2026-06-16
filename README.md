"""
Mondelez Digitalization Methodology - Portfolio Case Study

This is a single-file, sanitized case study of the approach I followed during my
digitalization/automation internship work.

It does not use any company data, internal SharePoint links, screenshots, exported
Power Apps, or Power Automate flows. I created small sample data inside this file
only to explain my thinking process.

Main idea:
Before automating anything, I first try to understand the manual process, find the
stable ID that connects records and documents, test the logic with sample cases,
and then think about edge cases like missing files, duplicate files, and messy user input.
"""

import re
import pandas as pd


 
# STEP 0: Create small sample data
 
# I am using sample data here. In real work, these tables would come from
# Excel files, SharePoint document libraries, shared mailbox attachments,
# or Power Apps / SharePoint lists.

def create_sample_data():
    finance_records = pd.DataFrame(
        {
            "customer": ["EDEKA", "EDEKA", "REWE", "ALDI"],
            "deduction_id": ["DED-1001", "DED-1002", "DED-1003", "DED-1004"],
            "invoice_no": ["INV-77421", "INV-77429", "INV-88112", "INV-90120"],
            "amount_eur": [1250.50, 785.00, 310.75, 620.15],
            "status": ["open", "open", "in review", "open"],
        }
    )

    sharepoint_documents = pd.DataFrame(
        {
            "file_name": [
                "Complaint_Invoice_INV-77421_EDK.pdf",
                "POD_INV-77421_delivery_confirmation.pdf",
                "Complaint_Invoice_INV-77429_EDK.pdf",
                "Claim_INV-88112_REWE_missing_items.pdf",
                "Complaint_Invoice_INV-90120_ALDI.pdf",
                "Duplicate_INV-90120_ALDI_claim.pdf",
            ],
            "folder_path": [
                "/FinanceDocs/EDEKA/",
                "/FinanceDocs/EDEKA/",
                "/FinanceDocs/EDEKA/",
                "/FinanceDocs/REWE/",
                "/FinanceDocs/ALDI/",
                "/FinanceDocs/ALDI/",
            ],
        }
    )

    incoming_attachments = pd.DataFrame(
        {
            "email_subject": [
                "EDEKA claim documents",
                "New price offer file",
                "Order return",
                "Unclear scanned file",
            ],
            "attachment_name": [
                "Complaint_Invoice_INV-77421_EDK.pdf",
                "PriceOffer_EDEKA_Week03.xlsx",
                "Order_Return_REWE_2026.xlsx",
                "scan_001.pdf",
            ],
        }
    )

    broker_orders = pd.DataFrame(
        {
            "customer": ["Retailer A", "Retailer A", "Retailer B", "Retailer C"],
            "order_number_raw": [" PO-45000012 ", "45000012", "PO 45000088", "45000101"],
            "material": ["Chocolate Box", "Biscuits", "Gum", "Candy"],
            "qty": [120, 80, 200, 60],
            "copy_selected": [True, True, False, True],
        }
    )

    return finance_records, sharepoint_documents, incoming_attachments, broker_orders


 
# STEP 1: Check the input data before building any logic
 
# I learned that a dashboard or automation is not useful if the input data
# is unclear. So I first check whether the important columns are available.

def check_required_columns(data, required_columns, table_name):
    missing_columns = []

    for column in required_columns:
        if column not in data.columns:
            missing_columns.append(column)

    if missing_columns:
        return {
            "table": table_name,
            "status": "failed",
            "missing_columns": missing_columns,
        }

    return {
        "table": table_name,
        "status": "passed",
        "missing_columns": [],
    }


 
# STEP 2: Use a stable ID to connect finance records and documents
 
# The main issue was not only storing documents. The main issue was:
# "How can a finance user quickly find the correct document for a record?"
#
# The practical answer was to use a stable identifier, for example invoice number.
# If the finance record has INV-77421 and a document name also contains INV-77421,
# then we can create a clear link between them.

def link_finance_records_to_documents(finance_records, sharepoint_documents):
    linked_rows = []

    for _, finance_row in finance_records.iterrows():
        invoice_no = str(finance_row["invoice_no"]).strip()

        matched_documents = sharepoint_documents[
            sharepoint_documents["file_name"].str.contains(invoice_no, case=False, na=False)
        ]

        # I keep the status simple because business users should understand it.
        if len(matched_documents) == 0:
            match_status = "missing_document"
        elif len(matched_documents) == 1:
            match_status = "matched"
        else:
            match_status = "multiple_documents_review_needed"

        linked_rows.append(
            {
                "customer": finance_row["customer"],
                "deduction_id": finance_row["deduction_id"],
                "invoice_no": invoice_no,
                "amount_eur": finance_row["amount_eur"],
                "finance_status": finance_row["status"],
                "match_status": match_status,
                "matched_file_count": len(matched_documents),
                "matched_files": " | ".join(matched_documents["file_name"].tolist()),
                "folder_paths": " | ".join(matched_documents["folder_path"].tolist()),
            }
        )

    return pd.DataFrame(linked_rows)


 
# STEP 3: Classify incoming attachments before storing them
 
# In Power Automate, I used logic like this with conditions/switch cases.
# The idea is simple:
# If the file name tells us what it is, send it to the right folder.
# If it is unclear, do not lose it. Send it to a review folder.

def classify_attachment_folder(file_name):
    name = file_name.lower()

    if "priceoffer" in name or "price_offer" in name:
        return "Customer Uploads / PriceOffer Returns"

    if "order" in name:
        return "Customer Uploads / Order Returns"

    if "invoice" in name or "complaint" in name or "claim" in name:
        return "Finance Documents / Claims and Invoices"

    return "Manual Review / Unclassified"


def route_incoming_attachments(incoming_attachments):
    result = incoming_attachments.copy()
    result["target_folder"] = result["attachment_name"].apply(classify_attachment_folder)
    result["needs_manual_review"] = result["target_folder"].eq("Manual Review / Unclassified")
    return result


 
# STEP 4: Clean broker/order numbers before saving or copying
 
# In a Power Apps style workflow, users may enter order numbers in different ways:
# "PO-45000012", "PO 45000012", "45000012".
#
# If this is not cleaned, duplicates and wrong searches can happen.
# So I normalize the order number and keep only the digits.

def clean_order_number(raw_value):
    if pd.isna(raw_value):
        return ""

    text = str(raw_value).upper().replace("PO", "")
    digits_only = re.findall(r"\d+", text)

    return "".join(digits_only)


def prepare_broker_order_lines(broker_orders):
    result = broker_orders.copy()

    result["order_number_clean"] = result["order_number_raw"].apply(clean_order_number)

    # This shows if the same customer has the same cleaned order number more than once.
    result["duplicate_order_number"] = result.duplicated(
        subset=["customer", "order_number_clean"],
        keep=False,
    )

    # This is similar to preparing selected order details for copy/paste from the app.
    result["copy_text"] = result.apply(
        lambda row: (
            f"{row['customer']} | Order: {row['order_number_clean']} | "
            f"Material: {row['material']} | Qty: {row['qty']}"
        ),
        axis=1,
    )

    return result


def build_selected_order_copy_text(cleaned_orders):
    selected_rows = cleaned_orders[cleaned_orders["copy_selected"] == True]
    return "\n".join(selected_rows["copy_text"].tolist())


 
# STEP 5: Prepare a simple summary for business discussion
 
# I try to finish with a summary that a business user can understand.
# This is usually more useful than only showing technical output.

def create_business_summary(linked_documents, routed_attachments, cleaned_orders):
    missing_documents = (linked_documents["match_status"] == "missing_document").sum()
    duplicate_document_matches = (
        linked_documents["match_status"] == "multiple_documents_review_needed"
    ).sum()
    attachments_for_review = routed_attachments["needs_manual_review"].sum()
    duplicate_orders = cleaned_orders["duplicate_order_number"].sum()

    summary = f"""
Business Summary

Finance document linking:
- Missing document cases: {missing_documents}
- Multiple document matches needing review: {duplicate_document_matches}

Incoming attachment routing:
- Attachments needing manual review: {attachments_for_review}

Broker order workflow:
- Duplicate cleaned order numbers found: {duplicate_orders}

My approach:
1. Understand the manual process before automating it.
2. Find the stable ID, such as invoice number or order number.
3. Build simple matching/routing logic.
4. Make missing and duplicate cases visible instead of hiding them.
5. Keep the output understandable for business users.
6. Document the logic so it can be maintained or extended later.
"""
    return summary.strip()

 
# MAIN DEMO
 
# This runs the small case study end to end.

def main():
    print("Creating sample data...")
    finance_records, sharepoint_documents, incoming_attachments, broker_orders = create_sample_data()

    print("\nStep 1: Checking required columns")
    checks = [
        check_required_columns(
            finance_records,
            ["customer", "deduction_id", "invoice_no", "amount_eur", "status"],
            "finance_records",
        ),
        check_required_columns(
            sharepoint_documents,
            ["file_name", "folder_path"],
            "sharepoint_documents",
        ),
        check_required_columns(
            incoming_attachments,
            ["email_subject", "attachment_name"],
            "incoming_attachments",
        ),
        check_required_columns(
            broker_orders,
            ["customer", "order_number_raw", "material", "qty", "copy_selected"],
            "broker_orders",
        ),
    ]

    for check in checks:
        print(check)

    print("\nStep 2: Linking finance records to documents")
    linked_documents = link_finance_records_to_documents(finance_records, sharepoint_documents)
    print(linked_documents)

    print("\nStep 3: Routing incoming email attachments")
    routed_attachments = route_incoming_attachments(incoming_attachments)
    print(routed_attachments)

    print("\nStep 4: Cleaning broker order numbers")
    cleaned_orders = prepare_broker_order_lines(broker_orders)
    print(cleaned_orders)

    print("\nSelected order lines prepared for copy/paste")
    selected_copy_text = build_selected_order_copy_text(cleaned_orders)
    print(selected_copy_text)

    print("\nStep 5: Business summary")
    summary = create_business_summary(linked_documents, routed_attachments, cleaned_orders)
    print(summary)


if __name__ == "__main__":
    main()
