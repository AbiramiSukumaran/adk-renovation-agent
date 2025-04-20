

-- Table DDL for Procurement Material Order Status

CREATE TABLE material_order_status (
    order_id VARCHAR(50) PRIMARY KEY,
    material_name VARCHAR(100) NOT NULL,
    supplier_name VARCHAR(100) NOT NULL,
    order_date DATE NOT NULL,
    estimated_delivery_date DATE,
    actual_delivery_date DATE,
    quantity_ordered INT NOT NULL,
    quantity_received INT,
    unit_price DECIMAL(10, 2) NOT NULL,
    total_amount DECIMAL(12, 2),
    order_status VARCHAR(50) NOT NULL, -- e.g., "Ordered", "Shipped", "Delivered", "Cancelled"
    delivery_address VARCHAR(255),
    contact_person VARCHAR(100),
    contact_phone VARCHAR(20),
    tracking_number VARCHAR(100),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    quality_check_passed BOOLEAN,  -- Indicates if the material passed quality control
    quality_check_notes TEXT,        -- Notes from the quality control check
    priority VARCHAR(20),            -- e.g., "High", "Medium", "Low"
    project_id VARCHAR(50),          -- Link to a specific project
    receiver_name VARCHAR(100),        -- Name of the person who received the delivery
    return_reason TEXT,               -- Reason for returning material if applicable
    po_number VARCHAR(50)             -- Purchase order number
);

-- Sample Insert Statements (25 rows)
INSERT INTO material_order_status (order_id, material_name, supplier_name, order_date, estimated_delivery_date, actual_delivery_date, quantity_ordered, quantity_received, unit_price, total_amount, order_status, delivery_address, contact_person, contact_phone, tracking_number, notes, quality_check_passed, quality_check_notes, priority, project_id, receiver_name, return_reason, po_number) VALUES
('ORD-001', 'Lumber - 2x4', 'ABC Lumber Co.', '2025-04-01', '2025-04-06', '2025-04-06', 100, 100, 2.50, 250.00, 'Delivered', '123 Main St', 'John Doe', '555-1234', 'TRACK123', 'Standard grade lumber.', TRUE, 'No issues found.', 'Medium', 'PROJ-001', 'Jane Smith', NULL, 'PO-001'),
('ORD-002', 'Cement Bags', 'XYZ Cement Inc.', '2025-04-02', '2025-04-08', '2025-04-08', 50, 50, 8.00, 400.00, 'Delivered', '123 Main St', 'John Doe', '555-1234', 'TRACK456', 'Portland cement.', TRUE, 'All bags in good condition.', 'High', 'PROJ-001', 'Jane Smith', NULL, 'PO-002'),
('ORD-003', 'Roofing Shingles', 'Roofing Supplies Ltd.', '2025-04-03', '2025-04-10', '2025-04-10', 200, 200, 1.75, 350.00, 'Delivered', '123 Main St', 'John Doe', '555-1234', 'TRACK789', 'Asphalt shingles.', TRUE, 'Color matches sample.', 'Medium', 'PROJ-001', 'Jane Smith', NULL, 'PO-003'),
('ORD-004', 'Plywood Sheets', 'ABC Lumber Co.', '2025-04-04', '2025-04-11', '2025-04-11', 50, 50, 15.00, 750.00, 'Delivered', '123 Main St', 'John Doe', '555-1234', 'TRACK101', 'CDX plywood.', TRUE, 'No warping or damage.', 'Medium', 'PROJ-001', 'Jane Smith', NULL, 'PO-004'),
('ORD-005', 'Insulation Rolls', 'Insulation Experts Inc.', '2025-04-05', '2025-04-12', '2025-04-12', 30, 30, 25.00, 750.00, 'Delivered', '123 Main St', 'John Doe', '555-1234', 'TRACK112', 'Fiberglass insulation.', TRUE, 'Correct R-value.', 'Medium', 'PROJ-001', 'Jane Smith', NULL, 'PO-005'),
('ORD-006', 'Electrical Wiring', 'Electric Supply Co.', '2025-04-06', '2025-04-13', '2025-04-13', 1000, 1000, 0.50, 500.00, 'Delivered', '123 Main St', 'John Doe', '555-1234', 'TRACK123', '14-gauge wire.', TRUE, 'Meets UL standards.', 'High', 'PROJ-001', 'Jane Smith', NULL, 'PO-006'),
('ORD-007', 'Plumbing Pipes', 'Plumbing Supplies Inc.', '2025-04-07', '2025-04-14', '2025-04-14', 50, 50, 10.00, 500.00, 'Delivered', '123 Main St', 'John Doe', '555-1234', 'TRACK456', 'PVC pipes.', TRUE, 'No cracks or leaks.', 'High', 'PROJ-001', 'Jane Smith', NULL, 'PO-007'),
('ORD-008', 'Drywall Sheets', 'Drywall Depot', '2025-04-08', '2025-04-15', '2025-04-15', 40, 40, 12.00, 480.00, 'Delivered', '123 Main St', 'John Doe', '555-1234', 'TRACK789', '1/2 inch drywall.', TRUE, 'Smooth surface.', 'Medium', 'PROJ-001', 'Jane Smith', NULL, 'PO-008'),
('ORD-009', 'Paint - White', 'Paint Store Plus', '2025-04-09', '2025-04-16', '2025-04-16', 10, 10, 30.00, 300.00, 'Delivered', '123 Main St', 'John Doe', '555-1234', 'TRACK101', 'Interior latex paint.', TRUE, 'Correct shade of white.', 'Medium', 'PROJ-001', 'Jane Smith', NULL, 'PO-009'),
('ORD-010', 'Nails - Assorted', 'Hardware Supply Co.', '2025-04-10', '2025-04-17', '2025-04-17', 5, 5, 20.00, 100.00, 'Delivered', '123 Main St', 'John Doe', '555-1234', 'TRACK112', 'Various sizes of nails.', TRUE, 'No rust or defects.', 'Low', 'PROJ-001', 'Jane Smith', NULL, 'PO-010'),
('ORD-011', 'Tile - Ceramic', 'Tile World', '2025-04-11', '2025-04-18', '2025-04-18', 100, 100, 3.00, 300.00, 'Delivered', '123 Main St', 'John Doe', '555-1234', 'TRACK123', 'White ceramic tiles.', TRUE, 'No chips or cracks.', 'Medium', 'PROJ-002', 'Peter Jones', NULL, 'PO-011'),
('ORD-012', 'Kitchen Cabinets', 'Cabinet Makers Inc.', '2025-04-12', '2025-04-19', NULL, 6, NULL, 200.00, NULL, 'Ordered', '123 Main St', 'John Doe', '555-1234', NULL, 'Custom-built cabinets.', NULL, NULL, 'High', 'PROJ-002', NULL, NULL, 'PO-012'),
('ORD-013', 'Countertop - Granite', 'Stone Creations', '2025-04-13', '2025-04-20', NULL, 1, NULL, 500.00, NULL, 'Ordered', '123 Main St', 'John Doe', '555-1234', NULL, 'Granite slab.', NULL, NULL, 'High', 'PROJ-002', NULL, NULL, 'PO-013'),
('ORD-014', 'Sink - Stainless Steel', 'Plumbing Supplies Inc.', '2025-04-14', '2025-04-21', NULL, 1, NULL, 150.00, NULL, 'Shipped', '123 Main St', 'John Doe', '555-1234', 'TRACK456', 'Single bowl sink.', NULL, NULL, 'Medium', 'PROJ-002', NULL, NULL, 'PO-014'),
('ORD-015', 'Faucet - Chrome', 'Plumbing Supplies Inc.', '2025-04-15', '2025-04-22', NULL, 1, NULL, 80.00, NULL, 'Shipped', '123 Main St', 'John Doe', '555-1234', 'TRACK789', 'Chrome finish faucet.', NULL, NULL, 'Medium', 'PROJ-002', NULL, NULL, 'PO-015'),
('ORD-016', 'Light Fixtures', 'Electric Supply Co.', '2025-04-16', '2025-04-23', NULL, 4, NULL, 40.00, NULL, 'Ordered', '123 Main St', 'John Doe', '555-1234', NULL, 'Recessed lighting.', NULL, NULL, 'Medium', 'PROJ-002', NULL, NULL, 'PO-016'),
('ORD-017', 'Backsplash Tiles', 'Tile World', '2025-04-17', '2025-04-24', NULL, 50, NULL, 2.50, NULL, 'Ordered', '123 Main St', 'John Doe', '555-1234', NULL, 'Glass backsplash tiles.', NULL, NULL, 'Medium', 'PROJ-002', NULL, NULL, 'PO-017'),
('ORD-018', 'Grout - White', 'Tile World', '2025-04-18', '2025-04-25', NULL, 2, NULL, 15.00, NULL, 'Shipped', '123 Main St', 'John Doe', '555-1234', 'TRACK101', 'White grout.', NULL, NULL, 'Low', 'PROJ-002', NULL, NULL, 'PO-018'),
('ORD-019', 'Adhesive - Tile', 'Tile World', '2025-04-19', '2025-04-26', NULL, 1, NULL, 20.00, NULL, 'Shipped', '123 Main St', 'John Doe', '555-1234', 'TRACK112', 'Tile adhesive.', NULL, NULL, 'Low', 'PROJ-002', NULL, NULL, 'PO-019'),
('ORD-020', 'Appliance - Refrigerator', 'Appliance Depot', '2025-04-20', '2025-04-27', NULL, 1, NULL, 1200.00, NULL, 'Ordered', '123 Main St', 'John Doe', '555-1234', NULL, 'Stainless steel refrigerator.', NULL, NULL, 'High', 'PROJ-002', NULL, NULL, 'PO-020'),
('ORD-021', 'Appliance - Oven', 'Appliance Depot', '2025-04-21', '2025-04-28', NULL, 1, NULL, 800.00, NULL, 'Ordered', '123 Main St', 'John Doe', '555-1234', NULL, 'Electric oven.', NULL, NULL, 'High', 'PROJ-002', NULL, NULL, 'PO-021'),
('ORD-022', 'Appliance - Microwave', 'Appliance Depot', '2025-04-22', '2025-04-29', NULL, 1, NULL, 250.00, NULL, 'Shipped', '123 Main St', 'John Doe', '555-1234', 'TRACK123', 'Stainless steel microwave.', NULL, NULL, 'Medium', 'PROJ-002', NULL, NULL, 'PO-022'),
('ORD-023', 'Ventilation Fan', 'HVAC Supplies', '2025-04-23', '2025-04-30', NULL, 1, NULL, 100.00, NULL, 'Shipped', '123 Main St', 'John Doe', '555-1234', 'TRACK456', 'Kitchen ventilation fan.', NULL, NULL, 'Medium', 'PROJ-002', NULL, NULL, 'PO-023'),
('ORD-024', 'Drywall Screws', 'Hardware Supply Co.', '2025-04-24', '2025-05-01', NULL, 3, NULL, 10.00, NULL, 'Ordered', '123 Main St', 'John Doe', '555-1234', NULL, 'Box of drywall screws.', NULL, NULL, 'Low', 'PROJ-002', NULL, NULL, 'PO-024'),
('ORD-025', 'Safety Glasses', 'Safety Gear Ltd.', '2025-04-25', '2025-05-02', NULL, 5, NULL, 5.00, NULL, 'Ordered', '123 Main St', 'John Doe', '555-1234', NULL, 'Protective safety glasses.', NULL, NULL, 'Low', 'PROJ-002', NULL, NULL, 'PO-025');
