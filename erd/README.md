# ERD generation with eralchemy 1.6.0

This folder contains reproducible options that generate:

- `current_erd` (your original design, represented as-is)
- `improved_erd` (normalized and more efficient design)

## Option 1: Python script

### Install

```bash
python -m pip install "eralchemy==1.6.0" "graphviz"
```

> You also need Graphviz installed on your system (`dot` executable available in PATH).

### Run

```bash
python erd/generate_erd.py
```

## Option 2: Jupyter notebook

Open and run all cells in:

- `erd/erd_generator.ipynb`

The notebook includes a pip-install cell (commented) and generates the same outputs.

## Visuals

If you want immediate visuals without installing dependencies, open:

- `erd/visuals.md` (Mermaid diagrams for current and improved ERDs)


## PNG/PDF fallback generator (no external dependencies)

If Graphviz/eralchemy are unavailable in your environment, run:

```bash
python erd/generate_png_pdf.py
```

This generates local artifacts in `erd/output/` (PNG/PDF), which are intentionally not committed to git.

## Output

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
