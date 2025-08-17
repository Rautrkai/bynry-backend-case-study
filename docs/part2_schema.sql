CREATE TABLE companies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE warehouses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    company_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    CONSTRAINT fk_warehouses_company FOREIGN KEY (company_id) REFERENCES companies(id)
);

CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    sku VARCHAR(100) NOT NULL UNIQUE,
    price DECIMAL(10,2) NOT NULL,
    product_type VARCHAR(50)
);

CREATE TABLE inventory (
    product_id INT NOT NULL,
    warehouse_id INT NOT NULL,
    quantity INT NOT NULL DEFAULT 0,
    PRIMARY KEY (product_id, warehouse_id),
    CONSTRAINT fk_inventory_product FOREIGN KEY (product_id) REFERENCES products(id),
    CONSTRAINT fk_inventory_warehouse FOREIGN KEY (warehouse_id) REFERENCES warehouses(id)
);

CREATE TABLE inventory_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    warehouse_id INT NOT NULL,
    change_qty INT NOT NULL,
    change_reason VARCHAR(255),
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_inv_hist_product FOREIGN KEY (product_id) REFERENCES products(id),
    CONSTRAINT fk_inv_hist_warehouse FOREIGN KEY (warehouse_id) REFERENCES warehouses(id)
);

CREATE TABLE suppliers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    contact_email VARCHAR(255)
);

CREATE TABLE product_suppliers (
    product_id INT NOT NULL,
    supplier_id INT NOT NULL,
    PRIMARY KEY (product_id, supplier_id),
    CONSTRAINT fk_prod_sup_product FOREIGN KEY (product_id) REFERENCES products(id),
    CONSTRAINT fk_prod_sup_supplier FOREIGN KEY (supplier_id) REFERENCES suppliers(id)
);

CREATE TABLE product_bundles (
    bundle_id INT NOT NULL,
    component_id INT NOT NULL,
    quantity INT NOT NULL,
    PRIMARY KEY (bundle_id, component_id),
    CONSTRAINT fk_bundle_product FOREIGN KEY (bundle_id) REFERENCES products(id),
    CONSTRAINT fk_bundle_component FOREIGN KEY (component_id) REFERENCES products(id)
);
