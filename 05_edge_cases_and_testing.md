# Edge Cases and Testing

## Document linking

- No document contains invoice number: flag as missing_document.
- More than one document contains invoice number: flag as multiple_documents_review_needed.
- Inconsistent file naming: route to review or improve naming rule.
- User cannot open SharePoint link: check permission and path construction.

## Power Automate

- Empty attachment.
- Large attachment.
- Unexpected filename.
- Duplicate upload.
- Failed SharePoint create-file action.

## Power Apps

- Blank order number.
- Duplicate order number.
- User selects all then unselects one line.
- Patch fails because a SharePoint column changed.
