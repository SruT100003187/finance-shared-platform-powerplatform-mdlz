# Approach steps

This explains the approach I followed to understand the finance and broker workflow problem, design the logic, and convert it into a more structured digital process.

1. Understood the manual business process first

Before thinking about automation, I first tried to understand how the work was actually being done by the business users.

The main questions I focused on were:

Where are the documents coming from?
Who receives the files?
Where are the files stored?
Which Excel files or SharePoint folders are used by the finance team?
What information do users search for most often?
Which steps are repetitive or causing delays?
Where do errors happen, for example missing files, wrong names, duplicate records, or broken links?

This was important because the problem was not only technical. It was mainly a process problem involving finance records, customer documents, emails, SharePoint folders, and manual follow-ups.

2. Identified the main pain point

The key issue was that finance and sales users had to spend unnecessary time searching for supporting documents related to deductions, invoices, claims, or orders.

Documents could be stored in different places, such as:

shared mailbox attachments,
SharePoint folders,
Excel-based working files,
manual uploads,
customer-specific document folders.

Because of this, users often needed to manually search by invoice number, customer name, or file name. This made the process slower and less reliable.

3. Defined the stable identifier

After understanding the process, I focused on finding a stable key that could connect finance records with documents.

For this type of process, a useful identifier can be:

invoice number,
deduction ID,
claim ID,
order number,
customer-specific reference number.

The idea was simple: if the finance record contains an invoice number, and the document file name also contains the same invoice number, then the system can automatically suggest or create the link between them.

This became the base logic for the shared finance platform.

4. Designed the document-linking logic

The next step was to design logic that could compare finance records with document names.

The basic logic was:

Read the finance record.
Extract the stable ID, for example invoice number.
Search the document repository for file names containing that ID.
If one file is found, mark it as matched.
If no file is found, mark it as missing document.
If multiple files are found, mark it for review.
Return the matched file names and SharePoint-style paths.

This helped turn manual searching into a structured matching process.

5. Considered edge cases early

I did not assume that every file would be clean or perfectly named. I considered practical edge cases such as:

missing documents,
duplicate documents,
inconsistent file naming,
wrong customer folders,
documents uploaded manually,
attachments with unclear names,
SharePoint permission issues,
old or broken file references.

This was important because automation only becomes useful when it handles real-world imperfections, not only the perfect scenario.

6. Designed Power Automate-style routing rules

For incoming email attachments, I followed a simple classification approach.

The routing logic was based on filename patterns:

files containing PriceOffer go to a price offer folder,
files containing Order go to an order return folder,
files containing Invoice, Complaint, or Claim go to a finance document folder,
unclear files go to a manual review folder.

This approach keeps the flow understandable and easier to troubleshoot. Instead of silently failing, unknown files are still captured and sent for review.

7. Worked with Power Apps-style broker workflow logic

For the broker/order workflow, the focus was on reducing manual entry and making the app easier to use.

The logic included:

keeping one clean order number field,
normalizing order numbers before saving,
avoiding duplicate order number issues,
allowing users to select multiple lines,
preparing selected order details for copy/paste,
patching structured data into a SharePoint list.

The goal was not only to build a screen, but to make the workflow easier and more reliable for users.

8. Validated the logic using sample data

To test the approach, I used sample data representing:

finance deduction records,
document repository records,
incoming email attachments,
broker/order records.

I checked whether the logic could correctly identify:

matched documents,
missing documents,
duplicate document matches,
unknown attachment types,
duplicate order numbers,
selected order lines for copying.

This helped confirm that the logic worked before thinking about broader rollout.

9. Documented the process clearly

I documented the process because digitalization work should be understandable by both business users and technical teams.

The documentation explains:

the problem context,
the solution architecture,
Power Automate routing logic,
Power Apps broker app logic,
edge cases and testing approach.

This makes the solution easier to maintain and easier to explain during handover or future improvements.

10. Focused on practical improvement, not over-engineering

The main goal was to create a practical solution that users could understand and rely on.

Instead of starting with a complex system, I focused on:

simple matching rules,
stable identifiers,
clear folder routing,
visible review cases,
structured outputs,
user-friendly workflow logic.

This approach helped reduce manual effort and made the process easier to scale across more customers or similar finance workflows.

What this project demonstrates

This GitHub project is a sanitized recreation of my approach. It does not contain internal company data or production assets.

It demonstrates how I think through a digitalization problem:

Understand the business process.
Identify the manual pain points.
Find the stable data keys.
Build simple and testable logic.
Handle edge cases.
Document the solution.
Keep the process usable for business users.

The purpose is to show my practical problem-solving approach in finance process digitalization, Power Platform logic, SharePoint-based document handling, and business-oriented automation.
