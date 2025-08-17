from flask import Flask, jsonify
from datetime import datetime, timedelta
from sqlalchemy import func
from decimal import Decimal

app = Flask(__name__)

# Threshold mapping by product type (dummy assumption)
PRODUCT_THRESHOLDS = {
    "widget": 20,
    "gadget": 15,
    "default": 10
}

@app.route('/api/companies/<int:company_id>/alerts/low-stock', methods=['GET'])
def get_low_stock_alerts(company_id):
    try:
        # Step 1: Find all warehouses belonging to this company
        warehouses = Warehouse.query.filter_by(company_id=company_id).all()
        if not warehouses:
            return jsonify({"alerts": [], "total_alerts": 0}), 200

        warehouse_ids = [w.id for w in warehouses]

        # Step 2: Check recent sales activity (last 30 days)
        cutoff_date = datetime.utcnow() - timedelta(days=30)

        recent_sales_subq = (
            db.session.query(
                SalesOrder.product_id,
                SalesOrder.warehouse_id,
                func.sum(SalesOrder.quantity).label("total_sold"),
                func.count(SalesOrder.id).label("sales_count"),
                (func.sum(SalesOrder.quantity) / 30.0).label("avg_daily_sales")
            )
            .filter(SalesOrder.warehouse_id.in_(warehouse_ids))
            .filter(SalesOrder.created_at >= cutoff_date)
            .group_by(SalesOrder.product_id, SalesOrder.warehouse_id)
            .subquery()
        )

        # Step 3: Join inventories, products, suppliers, warehouses
        results = (
            db.session.query(
                Product.id.label("product_id"),
                Product.name.label("product_name"),
                Product.sku,
                Product.type_id,
                Inventory.quantity.label("current_stock"),
                Warehouse.id.label("warehouse_id"),
                Warehouse.name.label("warehouse_name"),
                Supplier.id.label("supplier_id"),
                Supplier.name.label("supplier_name"),
                Supplier.contact_email,
                recent_sales_subq.c.avg_daily_sales
            )
            .join(Inventory, Inventory.product_id == Product.id)
            .join(Warehouse, Warehouse.id == Inventory.warehouse_id)
            .join(Supplier, Supplier.id == Product.supplier_id)
            .join(recent_sales_subq, 
                  (recent_sales_subq.c.product_id == Product.id) &
                  (recent_sales_subq.c.warehouse_id == Warehouse.id))
            .filter(Warehouse.company_id == company_id)
            .all()
        )

        alerts = []
        for row in results:
            # Step 4: Determine threshold by product type
            threshold = PRODUCT_THRESHOLDS.get(row.type_id, PRODUCT_THRESHOLDS["default"])

            if row.current_stock < threshold:
                avg_daily_sales = row.avg_daily_sales or 1  # avoid divide by zero
                days_until_stockout = (
                    row.current_stock / avg_daily_sales if avg_daily_sales > 0 else None
                )

                alerts.append({
                    "product_id": row.product_id,
                    "product_name": row.product_name,
                    "sku": row.sku,
                    "warehouse_id": row.warehouse_id,
                    "warehouse_name": row.warehouse_name,
                    "current_stock": int(row.current_stock),
                    "threshold": threshold,
                    "days_until_stockout": int(days_until_stockout) if days_until_stockout else None,
                    "supplier": {
                        "id": row.supplier_id,
                        "name": row.supplier_name,
                        "contact_email": row.contact_email
                    }
                })

        return jsonify({
            "alerts": alerts,
            "total_alerts": len(alerts)
        }), 200

    except Exception as e:
        # Log the error in real application
        return jsonify({"error": "Unexpected server error"}), 500
