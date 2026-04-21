"""Generate current and improved ERDs using eralchemy==1.6.0.

Usage:
    python erd/generate_erd.py

Outputs are written to erd/output/ as both .er source and .png diagrams.
"""

from __future__ import annotations

from pathlib import Path

from eralchemy import render_er


OUTPUT_DIR = Path(__file__).parent / "output"


CURRENT_ERD = """
[Customer]
*CustomerID int
Name varchar
Email varchar
Phone varchar
Address varchar
BirthDate date

[Order]
*OrderID int
OrderDate date
TotalAmount decimal
CustomerName varchar
PaymentStatus varchar
ShippingAddress varchar

[Product]
*ProductID int
ProductName varchar
Category varchar
Price decimal
StockQuantity int
Description text

[Category]
*CategoryID int
CategoryName varchar
ParentCategoryID int
Description text
IsActive bool
CreatedDate datetime

[OrderDetails]
*OrderDetailID int
OrderID int
ProductID int
Quantity int
Price decimal
Discount decimal

[Supplier]
*SupplierID int
SupplierName varchar
ContactPerson varchar
Email varchar
Phone varchar
Address varchar

[Inventory]
*InventoryID int
ProductID int
WarehouseLocation varchar
StockLevel int
LastUpdated datetime
ReorderPoint int
Warehouse varchar

[Warehouse]
*WarehouseID int
WarehouseName varchar
Location varchar
ManagerName varchar
Phone varchar
Capacity int

[Payment]
*PaymentID int
OrderID int
PaymentMethod varchar
AmountPaid decimal
PaymentDate datetime
TransactionID varchar

[Employee]
*EmployeeID int
Name varchar
Position varchar
Email varchar
Phone varchar
DepartmentID int

OrderDetails.OrderID > Order.OrderID
OrderDetails.ProductID > Product.ProductID
Inventory.ProductID > Product.ProductID
Payment.OrderID > Order.OrderID
Category.ParentCategoryID > Category.CategoryID
""".strip()


IMPROVED_ERD = """
[Customer]
*CustomerID int
FullName varchar
Email varchar UNIQUE
Phone varchar
DateOfBirth date
CreatedAt datetime
UpdatedAt datetime

[CustomerAddress]
*AddressID int
CustomerID int
AddressType varchar
Line1 varchar
Line2 varchar
City varchar
State varchar
PostalCode varchar
Country varchar
IsDefault bool

[Order]
*OrderID int
CustomerID int
OrderDate datetime
OrderStatus varchar
PaymentStatus varchar
ShippingAddressID int
BillingAddressID int
SubtotalAmount decimal
TaxAmount decimal
ShippingAmount decimal
DiscountAmount decimal
TotalAmount decimal

[OrderItem]
*OrderItemID int
OrderID int
ProductID int
Quantity int
UnitPrice decimal
DiscountAmount decimal
LineTotal decimal

[Category]
*CategoryID int
CategoryName varchar
ParentCategoryID int
Description text
IsActive bool
CreatedAt datetime

[Product]
*ProductID int
ProductName varchar
CategoryID int
SKU varchar UNIQUE
UnitPrice decimal
IsActive bool
Description text
CreatedAt datetime
UpdatedAt datetime

[Supplier]
*SupplierID int
SupplierName varchar
ContactPerson varchar
Email varchar
Phone varchar

[ProductSupplier]
*ProductSupplierID int
ProductID int
SupplierID int
SupplierSKU varchar
CostPrice decimal
LeadTimeDays int

[Warehouse]
*WarehouseID int
WarehouseName varchar
Location varchar
Capacity int

[Inventory]
*InventoryID int
ProductID int
WarehouseID int
BinLocation varchar
StockLevel int
ReservedStock int
ReorderPoint int
LastUpdated datetime

[Payment]
*PaymentID int
OrderID int
ProcessedByEmployeeID int
PaymentMethod varchar
AmountPaid decimal
PaymentDate datetime
TransactionID varchar UNIQUE
PaymentStatus varchar

[Employee]
*EmployeeID int
FullName varchar
Position varchar
Email varchar
Phone varchar
DepartmentID int

CustomerAddress.CustomerID > Customer.CustomerID
Order.CustomerID > Customer.CustomerID
Order.ShippingAddressID > CustomerAddress.AddressID
Order.BillingAddressID > CustomerAddress.AddressID
OrderItem.OrderID > Order.OrderID
OrderItem.ProductID > Product.ProductID
Product.CategoryID > Category.CategoryID
Category.ParentCategoryID > Category.CategoryID
ProductSupplier.ProductID > Product.ProductID
ProductSupplier.SupplierID > Supplier.SupplierID
Inventory.ProductID > Product.ProductID
Inventory.WarehouseID > Warehouse.WarehouseID
Payment.OrderID > Order.OrderID
Payment.ProcessedByEmployeeID > Employee.EmployeeID
""".strip()


def _write_and_render(name: str, content: str) -> None:
    er_path = OUTPUT_DIR / f"{name}.er"
    png_path = OUTPUT_DIR / f"{name}.png"
    er_path.write_text(content + "\n", encoding="utf-8")
    render_er(str(er_path), str(png_path))
    print(f"Generated: {er_path}")
    print(f"Generated: {png_path}")


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    _write_and_render("current_erd", CURRENT_ERD)
    _write_and_render("improved_erd", IMPROVED_ERD)


if __name__ == "__main__":
    main()
