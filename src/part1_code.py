from flask import request, jsonify
from decimal import Decimal
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload

@app.route('/api/products', methods=['POST'])
def create_product():
    data = request.get_json() or {}

    # Validate required fields
    required_fields = ['name', 'sku', 'price', 'warehouse_id']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

    # Check SKU uniqueness
    if Product.query.filter_by(sku=data['sku']).first():
        return jsonify({"error": "SKU already exists"}), 409

    #  Validate warehouse existence 
    warehouse = Warehouse.query.get(data['warehouse_id'])
    if not warehouse:
        return jsonify({"error": "Invalid warehouse ID"}), 400

    try:
        # Start atomic transaction
        product = Product(
            name=data['name'],
            sku=data['sku'],
            price=Decimal(str(data['price'])),
            warehouse_id=data['warehouse_id']
        )
        db.session.add(product)
        db.session.flush()  

        # Create inventory record (default 0 if not provided)
        inventory = Inventory(
            product_id=product.id,
            warehouse_id=data['warehouse_id'],
            quantity=data.get('initial_quantity', 0)
        )
        db.session.add(inventory)

        db.session.commit()

        return jsonify({
            "message": "Product created successfully",
            "product_id": product.id
        }), 201

    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Database integrity error"}), 500
