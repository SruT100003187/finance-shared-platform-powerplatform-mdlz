# Power Automate Flow Specification

## Trigger

When a new email arrives in a shared mailbox.

## Classification rules

| Condition | Target folder |
|---|---|
| File name contains PriceOffer | Customer Uploads/PriceOffer_returns |
| File name contains Order | Customer Uploads/Orders_returns |
| File name contains Invoice, Complaint, or Claim | FinanceDocs/Incoming_Invoices_Claims |
| No matching rule | Review/Unclassified |

## Error handling

- If file content is empty, stop and write an error record.
- If SharePoint permission fails, notify the responsible owner.
- If filename does not match a rule, route to manual review.
- Use stable file identifiers instead of fragile paths where possible.
