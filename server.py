#!/usr/bin/env python3
"""
Vua Pin - Production-Ready Battery E-commerce System
Backend: Flask + SQLite
"""

from flask import Flask, request, jsonify, render_template_string, send_file
from flask_cors import CORS
import sqlite3
import json
import os
import math
from datetime import datetime
from functools import wraps
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

# Database configuration
DB_PATH = 'vuapin.db'
SECRET_KEY = 'vua-pin-secret-2024'

# Email configuration
EMAIL_CONFIG = {
    'sender': os.getenv('EMAIL_SENDER', 'vuapin.shop@gmail.com'),
    'password': os.getenv('EMAIL_PASSWORD', 'your_app_password_here'),
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587
}

# ============================================================================
# DATABASE SETUP
# ============================================================================

def init_db():
    """Initialize SQLite database and run migrations"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Orders table
    c.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT,
            config TEXT NOT NULL,
            voltage REAL,
            capacity REAL,
            energy REAL,
            bms INTEGER,
            cell_type TEXT,
            price REAL DEFAULT 0,
            status TEXT DEFAULT 'new',
            note TEXT,
            image_data LONGTEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Products table
    c.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            price REAL NOT NULL,
            config TEXT NOT NULL,
            image_url TEXT,
            status TEXT DEFAULT 'active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Admin users table
    c.execute('''
        CREATE TABLE IF NOT EXISTS admin_users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Migrations: add columns if missing
    existing_cols = {row[1] for row in c.execute('PRAGMA table_info(orders)')}
    if 'email' not in existing_cols:
        c.execute('ALTER TABLE orders ADD COLUMN email TEXT')
        print("[OK] Migration: added email column to orders")

    if 'image_data' not in existing_cols:
        c.execute('ALTER TABLE orders ADD COLUMN image_data LONGTEXT')
        print("[OK] Migration: added image_data column to orders")

    conn.commit()
    conn.close()
    print("[OK] Database ready")

# ============================================================================
# UTILITIES
# ============================================================================

def get_db():
    """Get database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def dict_from_row(row):
    """Convert sqlite3.Row to dict"""
    if row is None:
        return None
    return dict(row)

def send_order_confirmation_email(customer_email, customer_name, order_id, order_data):
    """Send order confirmation email to customer"""
    try:
        # Create email message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f'✅ Xác nhận đơn hàng #{order_id} - Vua Pin'
        msg['From'] = EMAIL_CONFIG['sender']
        msg['To'] = customer_email

        # HTML email content
        html_content = f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; border: 1px solid #ddd; border-radius: 8px; padding: 20px; background-color: #f9f9f9;">
                    <h2 style="color: #0f766e;">🔋 Vua Pin - Xác nhận đơn hàng</h2>

                    <p>Xin chào <strong>{customer_name}</strong>,</p>

                    <p>Cảm ơn bạn đã đặt hàng tại Vua Pin! Đơn hàng của bạn đã được ghi nhận thành công.</p>

                    <div style="background: white; padding: 15px; border-radius: 5px; margin: 20px 0; border-left: 4px solid #0f766e;">
                        <h3 style="margin-top: 0; color: #0f766e;">Chi tiết đơn hàng</h3>
                        <p><strong>Mã đơn:</strong> #{order_id}</p>
                        <p><strong>Cấu hình:</strong> {order_data.get('config', 'N/A')}</p>
                        <p><strong>Số điện thoại:</strong> {order_data.get('phone', 'N/A')}</p>
                        <p><strong>Địa chỉ:</strong> {order_data.get('address', '')} {order_data.get('district', '')}, {order_data.get('city', '')}</p>
                        {f'<p><strong>Ghi chú:</strong> {order_data.get("note", "")}</p>' if order_data.get('note') else ''}
                        <p><strong>Hình thức thanh toán:</strong> {order_data.get('payment', 'N/A')}</p>
                    </div>

                    <div style="background: #e8f5e9; padding: 15px; border-radius: 5px; margin: 20px 0;">
                        <h3 style="margin-top: 0; color: #10b981;">📍 Tiếp theo?</h3>
                        <p>✓ Chúng tôi sẽ gọi điện xác nhận đơn hàng trong 1-2 giờ</p>
                        <p>✓ Giao hàng trong 7 ngày làm việc</p>
                        <p>✓ Bảo hành 24 tháng cho tất cả sản phẩm</p>
                    </div>

                    <div style="background: #fff3e0; padding: 15px; border-radius: 5px; margin: 20px 0;">
                        <h3 style="margin-top: 0; color: #f59e0b;">📞 Liên hệ nhanh</h3>
                        <p><strong>Hotline:</strong> 0814830562</p>
                        <p><strong>Zalo:</strong> 0814830562</p>
                        <p><strong>Email:</strong> vuapin.shop@gmail.com</p>
                    </div>

                    <p style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; color: #666; font-size: 12px;">
                        © 2024 Vua Pin - Giải pháp pin lithium tối ưu
                    </p>
                </div>
            </body>
        </html>
        """

        msg.attach(MIMEText(html_content, 'html'))

        # Send email
        with smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port']) as server:
            server.starttls()
            server.login(EMAIL_CONFIG['sender'], EMAIL_CONFIG['password'])
            server.send_message(msg)

        return True
    except Exception as e:
        print(f'[ERROR] Email sending error: {str(e)}')
        return False

# Initialize DB at import time (supports both direct run and WSGI/gunicorn)
init_db()

# ============================================================================
# ROUTES: PUBLIC
# ============================================================================

@app.route('/')
def home():
    """Serve landing page"""
    return send_file('index.html')

@app.route('/admin')
def admin():
    """Serve admin dashboard"""
    return send_file('admin.html')

# ============================================================================
# ROUTES: API
# ============================================================================

@app.route('/api/calculate', methods=['POST'])
def calculate():
    """Calculate battery configuration"""
    try:
        data = request.json

        # Validate inputs
        v_cell = float(data.get('v_cell', 3.7))
        ah_cell = float(data.get('ah_cell', 3))
        target_voltage = float(data.get('target_voltage', 48))
        parallel = int(data.get('parallel', 1))
        cell_type = data.get('cell_type', 'standard')

        # Input validation
        if not all([v_cell > 0, ah_cell > 0, target_voltage > 0, parallel > 0]):
            return jsonify({'error': 'Giá trị phải lớn hơn 0'}), 400

        if v_cell < 2 or v_cell > 5:
            return jsonify({'error': 'V cell phải từ 2-5V'}), 400

        if target_voltage > 120:
            return jsonify({'error': 'Điện áp quá cao (>120V)'}), 400

        # Cell type specs
        CELL_SPECS = {
            'cheap': {'name': 'Loại rẻ', 'max_current': 5},
            'standard': {'name': 'Standard 18650', 'max_current': 10},
            'high_drain': {'name': 'High Drain', 'max_current': 20},
            'premium': {'name': 'Premium', 'max_current': 30}
        }

        if cell_type not in CELL_SPECS:
            cell_type = 'standard'

        specs = CELL_SPECS[cell_type]

        # CALCULATIONS
        S = math.ceil(target_voltage / v_cell)
        voltage = S * v_cell
        capacity = ah_cell * parallel
        energy = voltage * capacity
        total_cells = S * parallel
        max_voltage = 4.2 * S
        min_voltage = 2.5 * S
        nominal_voltage = 3.7 * S

        # Current & BMS
        cell_max_current = specs['max_current']
        pack_max_current = cell_max_current * parallel
        bms_rating = math.ceil(pack_max_current * 1.2)

        # Warnings
        warnings = []
        if voltage > 72:
            warnings.append('⚠️ Điện áp cao (>72V): Cần BMS và cách điện cực tốt')
        if capacity > 200:
            warnings.append('⚠️ Dung lượng rất lớn: Nên chia thành nhiều pack nhỏ')
        if parallel > 20:
            warnings.append('⚠️ Quá nhiều cell nối song song: Khó cân bằng')
        if S > 30:
            warnings.append('⚠️ Quá nhiều cell nối tiếp: Rủi ro cao')

        return jsonify({
            'success': True,
            'config': f'{S}S{parallel}P',
            'S': S,
            'P': parallel,
            'voltage': round(voltage, 2),
            'capacity': round(capacity, 2),
            'energy': round(energy, 1),
            'total_cells': total_cells,
            'max_voltage': round(max_voltage, 2),
            'min_voltage': round(min_voltage, 2),
            'nominal_voltage': round(nominal_voltage, 2),
            'cell_type': cell_type,
            'cell_max_current': cell_max_current,
            'pack_max_current': round(pack_max_current, 2),
            'bms_rating': bms_rating,
            'warnings': warnings
        }), 200

    except Exception as e:
        return jsonify({'error': f'Lỗi: {str(e)}'}), 500

@app.route('/api/calculate-price', methods=['POST'])
def calculate_price():
    """Calculate cost and suggested price"""
    try:
        data = request.json

        num_cells = int(data.get('total_cells', 130))
        cell_price = float(data.get('cell_price', 50000))
        bms_price = float(data.get('bms_price', 300000))
        extra_cost = float(data.get('extra_cost', 100000))

        # Cost calculation
        material_cost = num_cells * cell_price
        total_cost = material_cost + bms_price + extra_cost

        # Suggested selling prices (1.3x - 1.7x)
        price_low = total_cost * 1.3
        price_mid = total_cost * 1.5
        price_high = total_cost * 1.7

        return jsonify({
            'success': True,
            'material_cost': round(material_cost),
            'total_cost': round(total_cost),
            'price_low': round(price_low),
            'price_mid': round(price_mid),
            'price_high': round(price_high),
            'margin_low': round(price_low - total_cost),
            'margin_mid': round(price_mid - total_cost),
            'margin_high': round(price_high - total_cost)
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/order', methods=['POST'])
def create_order():
    """Create new order"""
    try:
        data = request.json

        name = data.get('name', '').strip()
        phone = data.get('phone', '').strip()
        email = data.get('email', '').strip()
        config = data.get('config', '').strip()
        voltage = data.get('voltage')
        capacity = data.get('capacity')
        energy = data.get('energy')
        bms = data.get('bms')
        cell_type = data.get('cell_type', '')
        price = float(data.get('price', 0))
        note = data.get('note', '').strip()
        address = data.get('address', '').strip()
        district = data.get('district', '').strip()
        city = data.get('city', '').strip()
        delivery_note = data.get('delivery_note', '').strip()
        payment = data.get('payment', '').strip()

        # Validation
        if not name or len(name) < 2:
            return jsonify({'error': 'Tên phải có ít nhất 2 ký tự'}), 400

        if not phone or len(phone) < 10:
            return jsonify({'error': 'Số điện thoại không hợp lệ'}), 400

        if not email:
            return jsonify({'error': 'Email không được để trống'}), 400

        # Save to database
        conn = get_db()
        c = conn.cursor()

        c.execute('''
            INSERT INTO orders
            (name, phone, email, config, voltage, capacity, energy, bms, cell_type, price, note, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, phone, email, config, voltage, capacity, energy, bms, cell_type, price, note, 'new'))

        conn.commit()
        order_id = c.lastrowid
        conn.close()

        # Prepare order data for email
        order_data = {
            'name': name,
            'phone': phone,
            'email': email,
            'config': config,
            'address': address,
            'district': district,
            'city': city,
            'delivery_note': delivery_note,
            'payment': payment,
            'note': note
        }

        # Send confirmation email (non-blocking)
        try:
            send_order_confirmation_email(email, name, order_id, order_data)
        except Exception as e:
            print(f'Warning: Could not send email: {str(e)}')

        return jsonify({
            'success': True,
            'message': 'Đặt hàng thành công! Email xác nhận đã được gửi.',
            'order_id': order_id
        }), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============================================================================
# ROUTES: ADMIN API
# ============================================================================

@app.route('/api/admin/orders', methods=['GET'])
def get_orders():
    """Get all orders"""
    try:
        conn = get_db()
        c = conn.cursor()

        # Get summary stats
        c.execute('SELECT COUNT(*) as total_orders FROM orders')
        total_orders = c.fetchone()['total_orders']

        c.execute('SELECT SUM(price) as total_revenue FROM orders')
        total_revenue = c.fetchone()['total_revenue'] or 0

        c.execute('SELECT COUNT(*) as completed FROM orders WHERE status = "done"')
        completed = c.fetchone()['completed']

        # Get all orders
        c.execute('''
            SELECT * FROM orders
            ORDER BY created_at DESC
        ''')

        orders = [dict_from_row(row) for row in c.fetchall()]
        conn.close()

        return jsonify({
            'success': True,
            'stats': {
                'total_orders': total_orders,
                'total_revenue': round(total_revenue),
                'completed': completed,
                'pending': total_orders - completed
            },
            'orders': orders
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/order/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    """Update order status, price, and image"""
    try:
        data = request.json
        status = data.get('status')
        price = data.get('price')
        image_data = data.get('image_data')

        if status not in ['new', 'processing', 'done', 'cancelled']:
            return jsonify({'error': 'Status không hợp lệ'}), 400

        conn = get_db()
        c = conn.cursor()

        if price is not None and image_data is not None:
            c.execute('UPDATE orders SET status = ?, price = ?, image_data = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?',
                     (status, price, image_data, order_id))
        elif price is not None:
            c.execute('UPDATE orders SET status = ?, price = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?',
                     (status, price, order_id))
        elif image_data is not None:
            c.execute('UPDATE orders SET status = ?, image_data = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?',
                     (status, image_data, order_id))
        else:
            c.execute('UPDATE orders SET status = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?',
                     (status, order_id))

        conn.commit()
        conn.close()

        return jsonify({
            'success': True,
            'message': 'Cập nhật thành công'
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/order/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    """Delete order"""
    try:
        conn = get_db()
        c = conn.cursor()
        c.execute('DELETE FROM orders WHERE id = ?', (order_id,))
        conn.commit()
        conn.close()

        return jsonify({'success': True}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============================================================================
# ROUTES: PRODUCTS ADMIN
# ============================================================================

@app.route('/api/admin/products', methods=['GET'])
def get_products():
    """Get all products"""
    try:
        conn = get_db()
        c = conn.cursor()
        c.execute('SELECT id, name, description, price, config, image_url, status, created_at FROM products ORDER BY id DESC')
        rows = c.fetchall()
        conn.close()

        products = [dict(row) for row in rows]
        return jsonify({'products': products}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/product', methods=['POST'])
def create_product():
    """Create new product"""
    try:
        data = request.json
        name = data.get('name', '').strip()
        description = data.get('description', '').strip()
        price = float(data.get('price', 0))
        config = data.get('config', '').strip()
        image_url = data.get('image_url', '').strip()
        status = data.get('status', 'active')

        if not all([name, description, config]):
            return jsonify({'error': 'Thông tin không đầy đủ'}), 400

        conn = get_db()
        c = conn.cursor()
        c.execute('''
            INSERT INTO products (name, description, price, config, image_url, status)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (name, description, price, config, image_url, status))

        product_id = c.lastrowid
        conn.commit()
        conn.close()

        return jsonify({
            'success': True,
            'message': 'Thêm sản phẩm thành công',
            'product_id': product_id
        }), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/product/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    """Update product"""
    try:
        data = request.json
        name = data.get('name', '').strip()
        description = data.get('description', '').strip()
        price = float(data.get('price', 0))
        config = data.get('config', '').strip()
        image_url = data.get('image_url', '').strip()
        status = data.get('status', 'active')

        if not all([name, description, config]):
            return jsonify({'error': 'Thông tin không đầy đủ'}), 400

        conn = get_db()
        c = conn.cursor()
        c.execute('''
            UPDATE products
            SET name = ?, description = ?, price = ?, config = ?, image_url = ?, status = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (name, description, price, config, image_url, status, product_id))

        conn.commit()
        conn.close()

        return jsonify({
            'success': True,
            'message': 'Cập nhật sản phẩm thành công'
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/product/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    """Delete product"""
    try:
        conn = get_db()
        c = conn.cursor()
        c.execute('DELETE FROM products WHERE id = ?', (product_id,))
        conn.commit()
        conn.close()

        return jsonify({'success': True, 'message': 'Xóa sản phẩm thành công'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': 'Server error'}), 500

@app.route('/orders/<order_id>', methods=['PUT'])
def update_order(order_id):
    """Update order status and price"""
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'Dữ liệu không hợp lệ'}), 400
        if FIREBASE_READY:
            ref = db.reference(f'orders/{order_id}')
            ref.update(data)
        return jsonify({'success': True, 'message': 'Order updated'}), 200
    except Exception as e:
        return jsonify({'error': f'Lỗi: {str(e)}'}), 500

@app.route('/orders/<order_id>', methods=['DELETE'])
def delete_order(order_id):
    """Delete an order"""
    try:
        if FIREBASE_READY:
            ref = db.reference(f'orders/{order_id}')
            ref.delete()
        return jsonify({'success': True, 'message': 'Order deleted'}), 200
    except Exception as e:
        return jsonify({'error': f'Lỗi: {str(e)}'}), 500

@app.route('/api/calculate-price', methods=['POST'])
def calculate_price():
    """Calculate product pricing with margins"""
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'Dữ liệu không hợp lệ'}), 400

        total_cells = int(data.get('total_cells', 0))
        cell_price = float(data.get('cell_price', 0))
        bms_price = float(data.get('bms_price', 0))
        extra_cost = float(data.get('extra_cost', 0))

        material_cost = total_cells * cell_price
        total_cost = material_cost + bms_price + extra_cost

        price_low = total_cost * 1.3
        price_mid = total_cost * 1.5
        price_high = total_cost * 1.7

        return jsonify({
            'success': True,
            'material_cost': round(material_cost),
            'total_cost': round(total_cost),
            'price_low': round(price_low),
            'price_mid': round(price_mid),
            'price_high': round(price_high),
            'margin_low': round(price_low - total_cost),
            'margin_high': round(price_high - total_cost)
        }), 200
    except Exception as e:
        return jsonify({'error': f'Lỗi: {str(e)}'}), 500

# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    print("""
    ============================================================
    VUA PIN - Battery E-commerce System
    ============================================================

    Landing Page:  http://127.0.0.1:5000
    Admin Panel:   http://127.0.0.1:5000/admin

    API Routes:
       POST /api/calculate          - Calculate battery config
       POST /api/calculate-price    - Calculate cost/price
       POST /api/order              - Create order
       GET  /api/admin/orders       - Get all orders
       PUT  /api/admin/order/<id>   - Update order
       DELETE /api/admin/order/<id> - Delete order

    ============================================================
    """)
    app.run(debug=True, port=5000, host='127.0.0.1')
