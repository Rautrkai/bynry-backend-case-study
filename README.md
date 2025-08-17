# bynry-backend-case-study
Case study solution for Backend Intern role at Bynry Inc


---

## Tech Stack
- **Language**: Python 3.x
- **Framework**: Flask
- **ORM**: SQLAlchemy
- **Database**: MySQL (assumed)
- **Tools**: ERD tool for schema design, GitHub for version control

---

## Part 1 – Code Review & Debugging
- **Goal**: Identify issues in the provided Flask endpoint for adding a new product, explain production impact, and provide a corrected implementation.
- **My Approach**:
  - Validated inputs to avoid runtime errors.
  - Ensured **SKU uniqueness** across the platform.
  - Verified **warehouse existence** before insertion.
  - Used **atomic transactions** to maintain data integrity.
  - Applied `Decimal` for price precision.
  - Returned consistent JSON responses with proper HTTP status codes.

 **Files**:
- [`src/part1_code.py`](src/part1_code.py) – Corrected implementation
- Details of identified issues and fixes are included as comments within the file.

---

##  Part 2 – Database Design
- **Goal**: Create a database schema supporting multi-warehouse inventory management, supplier relationships, bundles, and inventory change tracking.
- **My Approach**:
  - Designed **normalized tables** with proper foreign keys and indexes.
  - Added a **junction table** for product–warehouse relationships (`inventory`).
  - Introduced `inventory_history` to track quantity changes over time.
  - Self-referential table for product bundles.
  - Included **indexes** on `sku`, `warehouse_id`, and frequently queried columns.

 **Files**:
- [`docs/part2_schema.sql`](docs/part2_schema.sql) – Full DDL script
- [`docs/part2_schema.png`](docs/part2_schema.png) – ERD diagram
- [`docs/assumptions_and_gaps.md`](docs/assumptions_and_gaps.md) – Questions for product team and design considerations.

---

##  Part 3 – Low-Stock Alerts API
- **Goal**: Return alerts for products whose stock has fallen below threshold, factoring in recent sales and supplier details.
- **My Approach**:
  - Joined multiple tables to retrieve product, warehouse, and supplier data.
  - Applied product-type-specific thresholds.
  - Calculated `days_until_stockout` based on recent sales velocity.
  - Filtered out products without recent sales.
  - Considered edge cases (no supplier assigned, missing threshold, no sales history).

**Files**:
- [`src/part3_code.py`](src/part3_code.py) – API implementation with comments explaining logic and assumptions.

---

## Assumptions
1. Price is stored as `DECIMAL(10,2)` in the DB for financial accuracy.
2. SKUs are globally unique across all companies.
3. A “recent sale” is defined as a sale within the last 30 days.
4. Low-stock threshold is defined per product type, with a default fallback.
5. Bundled products’ stock counts are derived from their individual components.

---

##  How to Run Locally
1. Clone the repository:
   ```bash
   git clone https://github.com/Rautrkai/bynry-backend-case-study.git
   cd bynry-backend-case-study
