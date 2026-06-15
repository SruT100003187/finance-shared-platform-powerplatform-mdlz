# Solution Architecture

```text
Shared Mailbox / Manual Upload
          |
          v
Power Automate classification logic
          |
          v
SharePoint document libraries
          |
          v
Excel / Finance working file with stable invoice or deduction ID
          |
          v
Document linking logic
          |
          v
User opens related evidence directly from the finance record
```

The key design decision is to avoid manual folder navigation and use a stable identifier such as an invoice number, deduction ID, claim ID, or order number.
