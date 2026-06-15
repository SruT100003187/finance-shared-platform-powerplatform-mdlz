# Power Apps Formula Examples

These are simplified formula patterns, not exported from any company app.

## Normalize order number before saving

```powerfx
Set(
    varCleanOrderNumber,
    Substitute(
        Substitute(
            Upper(Trim(txtOrderNumber.Text)),
            "PO-",
            ""
        ),
        "PO ",
        ""
    )
)
```

## Select all checkbox pattern

```powerfx
UpdateContext({locSelectAll: chkSelectAll.Value});
```

## Patch selected order line to SharePoint list

```powerfx
Patch(
    'Broker Data',
    Defaults('Broker Data'),
    {
        Customer: ddCustomer.Selected.Value,
        OrderNumber: varCleanOrderNumber,
        Material: txtMaterial.Text,
        Quantity: Value(txtQuantity.Text),
        CreatedByUser: User().Email
    }
)
```

## Build copy text for selected lines

```powerfx
Concat(
    Filter(galOrderLines.AllItems, chkCopy.Value = true),
    Customer & " | Order: " & OrderNumber & " | Material: " & Material & " | Qty: " & Quantity,
    Char(10)
)
```
