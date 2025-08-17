# Assumptions & Gaps – Bynry Backend Case Study

##  Assumptions Made
1. **Price Precision** – Stored as `DECIMAL(10,2)` to avoid floating-point errors.
2. **SKU Uniqueness** – Globally unique across all companies.
3. **Recent Sales Definition** – Sales within the last 30 days are considered “recent”.
4. **Low Stock Threshold** – Defined per product type; default threshold = 20 units if not specified.
5. **Bundles** – Stock for a bundle is derived from the lowest available stock among its components.
6. **Inventory History** – Tracks every change with timestamp, quantity change, and reason.
7. **Multi-Warehouse** – A product can exist in multiple warehouses with independent quantities.

---

##  Gaps / Questions for Product Team
1. **Threshold Source** – Is the low-stock threshold stored per product, per type, or per warehouse?
2. **Bundle Pricing** – Is bundle price fixed or dynamically calculated from components?
3. **Sales Data Source** – Which table or service provides recent sales info for the low-stock API?
4. **Supplier Priority** – If multiple suppliers exist, how do we choose which one to show in alerts?
5. **Inventory Units** – Are quantities always integers, or do we support fractional units (e.g., weight)?
6. **Soft Deletes** – Should products/warehouses be soft-deleted or hard-deleted?
7. **Audit Requirements** – Do we need to track which user performed inventory changes?

---

##  Design Decisions Justification
- **Indexes**: Added on `sku`, `warehouse_id`, and foreign keys for faster lookups.
- **Constraints**: Foreign keys to enforce referential integrity; unique constraint on `sku`.
- **Scalability**: Many-to-many relationships for product–warehouse and product–bundle to allow flexible expansion.
- **History Table**: Separate `inventory_history` table to avoid bloating the main `inventory` table.
