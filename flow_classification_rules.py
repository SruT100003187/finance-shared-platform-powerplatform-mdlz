import pandas as pd

def classify_attachment(file_name: str) -> str:
    normalized = file_name.lower()
    if "priceoffer" in normalized or "price_offer" in normalized:
        return "Customer Uploads/PriceOffer_returns"
    if "order" in normalized:
        return "Customer Uploads/Orders_returns"
    if "complaint" in normalized or "invoice" in normalized or "claim" in normalized:
        return "FinanceDocs/Incoming_Invoices_Claims"
    return "Review/Unclassified"

def classify_email_attachments(attachments: pd.DataFrame) -> pd.DataFrame:
    data = attachments.copy()
    data["target_folder"] = data["attachment_name"].apply(classify_attachment)
    data["needs_manual_review"] = data["target_folder"].eq("Review/Unclassified")
    return data
