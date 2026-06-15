import re
import pandas as pd

def normalize_order_number(value: str) -> str:
    if pd.isna(value):
        return ""
    text = str(value).upper().replace("PO", "")
    digits = re.findall(r"\d+", text)
    return "".join(digits)

def clean_broker_orders(orders: pd.DataFrame) -> pd.DataFrame:
    data = orders.copy()
    data["order_number_clean"] = data["order_number_raw"].apply(normalize_order_number)
    data["duplicate_order_number"] = data.duplicated(
        subset=["customer", "order_number_clean"], keep=False
    )
    data["copy_line_text"] = data.apply(
        lambda row: f"{row['customer']} | Order: {row['order_number_clean']} | Material: {row['material']} | Qty: {row['qty']}",
        axis=1,
    )
    return data

def build_clipboard_text_for_selected_lines(cleaned_orders: pd.DataFrame) -> str:
    selected = cleaned_orders[cleaned_orders["copy_selected"] == True]
    return "\n".join(selected["copy_line_text"].tolist())
