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
Document linking logic (incoorporated in Excel)
          |
          v
User opens related evidence directly from the finance record and Power Apps interface by just one click. 
```

The key design decision is to avoid manual folder navigation and use a stable identifier such as an invoice number, deduction ID, claim ID, or order number.
Future work: Modify the Power Apps respect to the feedback team provides on weekly meetings.

