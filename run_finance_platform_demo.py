from pathlib import Path
import sys
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from src.document_linking_logic import build_document_links, summarize_matching_results
from src.flow_classification_rules import classify_email_attachments
from src.broker_order_cleaning import clean_broker_orders, build_clipboard_text_for_selected_lines

def main():
    output_dir = ROOT / "outputs"
    output_dir.mkdir(exist_ok=True)

    deductions = pd.read_csv(ROOT / "data/sample_deduction_records.csv")
    documents = pd.read_csv(ROOT / "data/sample_document_repository.csv")
    attachments = pd.read_csv(ROOT / "data/sample_email_attachments.csv")
    broker_orders = pd.read_csv(ROOT / "data/sample_broker_orders.csv")

    linked_records = build_document_links(deductions, documents)
    linked_records.to_csv(output_dir / "linked_finance_records.csv", index=False)

    summary = summarize_matching_results(linked_records)
    summary.to_csv(output_dir / "document_matching_summary.csv", index=False)

    routed_attachments = classify_email_attachments(attachments)
    routed_attachments.to_csv(output_dir / "attachment_routing_result.csv", index=False)

    cleaned_orders = clean_broker_orders(broker_orders)
    cleaned_orders.to_csv(output_dir / "cleaned_broker_orders.csv", index=False)

    clipboard_text = build_clipboard_text_for_selected_lines(cleaned_orders)
    (output_dir / "selected_order_lines_for_copy.txt").write_text(clipboard_text, encoding="utf-8")

    print("Demo completed.")
    print("Outputs created in:", output_dir)

if __name__ == "__main__":
    main()
