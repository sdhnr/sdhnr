# ERD generation with eralchemy 1.6.0

This folder contains a reproducible script that generates:

- `current_erd` (your original design, represented as-is)
- `improved_erd` (normalized and more efficient design)

## Install

```bash
python -m pip install "eralchemy==1.6.0" "graphviz"
```

> You also need Graphviz installed on your system (`dot` executable available in PATH).

## Run

```bash
python erd/generate_erd.py
```

Generated outputs are written to `erd/output/` as:

- `.er` source files
- `.png` diagrams

## Efficiency improvements applied

- Replaced `Order.CustomerName` with `Order.CustomerID` FK.
- Replaced `Product.Category` text with `Product.CategoryID` FK.
- Split customer addresses into `CustomerAddress` and linked order billing/shipping addresses.
- Replaced duplicated warehouse text in inventory with `WarehouseID` FK.
- Added `ProductSupplier` bridge for many-to-many Product↔Supplier relationships.
- Added `Payment.ProcessedByEmployeeID` FK and consistent status/amount fields.
- Added timestamps and uniqueness hints for key natural identifiers (`Email`, `SKU`, `TransactionID`).
