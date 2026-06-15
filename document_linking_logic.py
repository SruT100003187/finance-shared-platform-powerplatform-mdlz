import pandas as pd

def build_document_links(deduction_records: pd.DataFrame, document_repository: pd.DataFrame, id_column: str = "invoice_no") -> pd.DataFrame:
    """Match finance deduction records to supporting documents using a stable ID."""
    results = []
    for _, record in deduction_records.iterrows():
        record_id = str(record[id_column]).strip()
        matches = document_repository[
            document_repository["file_name"].str.contains(record_id, case=False, na=False)
        ].copy()

        if matches.empty:
            status = "missing_document"
        elif len(matches) > 1:
            status = "multiple_documents_review_needed"
        else:
            status = "matched"

        results.append({
            **record.to_dict(),
            "match_status": status,
            "matched_file_count": len(matches),
            "matched_files": " | ".join(matches["file_name"].tolist()),
            "sharepoint_paths": " | ".join(matches["sharepoint_path"].tolist()),
        })

    return pd.DataFrame(results)

def summarize_matching_results(linked_records: pd.DataFrame) -> pd.DataFrame:
    return (
        linked_records.groupby(["customer", "match_status"], as_index=False)
        .agg(records=("deduction_id", "count"), total_amount_eur=("amount_eur", "sum"))
        .sort_values(["customer", "match_status"])
    )
