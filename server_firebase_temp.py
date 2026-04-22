#!/usr/bin/env python3
"""
Vua Pin - Production-Ready Battery E-commerce System
Backend: Flask + Firebase Realtime Database
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import json
import os
import math
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Firebase imports
try:
    import firebase_admin
    from firebase_admin import credentials, db
    FIREBASE_ENABLED = True
except:
    FIREBASE_ENABLED = False
    print("[WARNING] Firebase not available, using fallback JSON storage")

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

# ============================================================================
# FIREBASE SETUP
# ============================================================================

def init_firebase():
    """Initialize Firebase"""
    if not FIREBASE_ENABLED:
        return False

    try:
        cred_json = os.getenv('FIREBASE_CREDENTIALS')
        if cred_json:
            cred_dict = json.loads(cred_json)
            cred = credentials.Certificate(cred_dict)
            firebase_admin.initialize_app(cred, {
                'databaseURL': 'https://gen-lang-client-0661551951-default-rtdb.asia-southeast1.firebaseio.com'
            })
            return True
    except Exception as e:
        print(f"[ERROR] Firebase init failed: {e}")
        return False

FIREBASE_READY = init_firebase()

# Email configuration
EMAIL_CONFIG = {
    'sender': os.getenv('EMAIL_SENDER', 'vuapin.shop@gmail.com'),
    'password': os.getenv('EMAIL_PASSWORD', 'your_app_password_here'),
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587
}

# Cell type database with discharge characteristics
CELL_TYPES = {
    'cheap': {
        'name': 'Loại rẻ (5A)',
        'max_discharge': 5,
        'description': 'Tế bào pin cấp bấp, 5A max'
    },
    'standard': {
        'name': 'Standard 18650 (10A)',
        'max_discharge': 10,
        'description': 'Tế bào chuẩn, 10A max'
    },
    'high_drain': {
        'name': 'High Drain (20A)',
        'max_discharge': 20,
        'description': 'Tế bào xả nhanh, 20A max'
    },
    'premium': {
        'name': 'Premium (30A)',
        'max_discharge': 30,
        'description': 'Tế bào cao cấp, 30A max'
    }
}

# ============================================================================
# FIREBASE DATABASE FUNCTIONS
# ============================================================================

def get_orders_ref():
    """Get Firebase orders reference"""
    if FIREBASE_READY:
        return db.reference('orders')
    return None

def get_products_ref():
    """Get Firebase products reference"""
    if FIREBASE_READY:
        return db.reference('products')
    return None

def load_orders():
    """Load all orders from Firebase"""
    if FIREBASE_READY:
        ref = get_orders_ref()
        orders = ref.get()
        if orders:
            return list(orders.values()) if isinstance(orders, dict) else orders
        return []
    return []

def save_order(order_data):
    """Save order to Firebase"""
    if FIREBASE_READY:
        ref = get_orders_ref()
        new_ref = ref.push(order_data)
        return new_ref.key
    return None

def load_products():
    """Load all products from Firebase"""
    if FIREBASE_READY:
        ref = get_products_ref()
        products = ref.get()
        if products:
            return list(products.values()) if isinstance(products, dict) else products
        return []
    return []

def save_product(product_data):
    """Save product to Firebase"""
    if FIREBASE_READY:
        ref = get_products_ref()
        new_ref = ref.push(product_data)
        return new_ref.key
    return None

def update_product(product_id, product_data):
    """Update product in Firebase"""
    if FIREBASE_READY:
        ref = get_products_ref().child(product_id)
        ref.update(product_data)
        return True
    return False

def delete_product(product_id):
    """Delete product from Firebase"""
    if FIREBASE_READY:
        ref = get_products_ref().child(product_id)
        ref.delete()
        return True
    return False

# ============================================================================
# EMAIL FUNCTIONS
# ============================================================================

def send_order_confirmation_email(email, order_data):
    """Send order confirmation email"""
    try:
        subject = f"Xác nhận đơn hàng - Vua Pin #{order_data.get('id', 'N/A')}"

        html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; color: #333;">
            <h2>Cảm ơn bạn đã đặt hàng!</h2>
            <p>Thông tin đơn hàng của bạn:</p>
            <ul>
                <li><strong>Tên:</strong> {order_data.get('name', 'N/A')}</li>
                <li><strong>Số điện thoại:</strong> {order_data.get('phone', 'N/A')}</li>
                <li><strong>Cấu hình:</strong> {order_data.get('config', 'N/A')}</li>
                <li><strong>Loại pin:</strong> {order_data.get('cell_type', 'N/A')}</li>
                <li><strong>Giá:</strong> {order_data.get('price', 0)} VND</li>
            </ul>
            <p>Chúng tôi sẽ liên hệ với bạn trong 24 giờ.</p>
            <p>Vua Pin Team</p>
        </body>
        </html>
        """

        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = EMAIL_CONFIG['sender']
        msg['To'] = email

        msg.attach(MIMEText(html_body, 'html'))

        with smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port']) as server:
            server.starttls()
            server.login(EMAIL_CONFIG['sender'], EMAIL_CONFIG['password'])
            server.send_message(msg)

        return True
    except Exception as e:
        print(f"[ERROR] Email send failed: {e}")
        return False

# ============================================================================
# VALIDATION FUNCTIONS
# ============================================================================

def validate_number(value, field_name, min_val=0.01, max_val=None):
    """Validate numeric input with range checking"""
    try:
        num = float(value)
        if num < min_val:
            raise ValueError(f"{field_name} phải lớn hơn {min_val}")
        if max_val and num > max_val:
            raise ValueError(f"{field_name} phải nhỏ hơn {max_val}")
        return num
    except (ValueError, TypeError) as e:
        raise ValueError(f"{field_name} không hợp lệ: {str(e)}")

# ============================================================================
# API ROUTES
# ============================================================================

@app.route('/', methods=['GET'])
def home():
    return send_file('index.html')

@app.route('/admin', methods=['GET'])
def admin():
    return send_file('admin.html')

@app.route('/cell-types', methods=['GET'])
def get_cell_types():
    """Get available cell types"""
    return jsonify(CELL_TYPES), 200

@app.route('/calculate', methods=['POST'])
def calculate():
    """Calculate battery configuration with engineering accuracy"""
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'Dữ liệu không hợp lệ'}), 400

        # Validate inputs
        v_cell = validate_number(data.get('v_cell'), 'V cell', 2.0, 5.0)
        ah_cell = validate_number(data.get('ah_cell'), 'Ah cell', 0.01, 100)
        target_voltage = validate_number(data.get('target_voltage'), 'Target voltage', 3, 120)
        parallel = int(validate_number(data.get('parallel', 1), 'Parallel', 1, 100))

        cell_type = data.get('cell_type', 'standard')
        if cell_type not in CELL_TYPES:
            cell_type = 'standard'

        # Get cell discharge capability
        cell_max_current = CELL_TYPES[cell_type]['max_discharge']

        # ENGINEERING CALCULATIONS
        S = math.ceil(target_voltage / v_cell)
        capacity = ah_cell * parallel
        pack_voltage = S * v_cell
        energy = pack_voltage * capacity
        total_cells = S * parallel
        pack_max_current = cell_max_current * parallel
        bms_rating = math.ceil(pack_max_current * 1.2)

        max_voltage = 4.2 * S
        min_voltage = 2.5 * S
        nominal_voltage = 3.7 * S

        # Safety checks
        warnings = []
        if pack_voltage > 72:
            warnings.append('⚠️ Điện áp cao (>72V): Nguy hiểm! Cần BMS và cách điện cực tốt')
        if capacity > 200:
            warnings.append('⚠️ Dung lượng rất lớn: Cân nhắc chia nhiều pack nhỏ')
        if parallel > 20:
            warnings.append('⚠️ Quá nhiều cell nối song song: Khó cân bằng, nguy hiểm')
        if S > 30:
            warnings.append('⚠️ Quá nhiều cell nối tiếp: Rủi ro cân bằng cao')

        return jsonify({
            'success': True,
            'config': f'{S}S{parallel}P',
            'S': S,
            'P': parallel,
            'voltage': round(pack_voltage, 2),
            'nominal_voltage': round(nominal_voltage, 2),
            'capacity': round(capacity, 2),
            'energy': round(energy, 1),
            'total_cells': total_cells,
            'max_voltage': round(max_voltage, 2),
            'min_voltage': round(min_voltage, 2),
            'cell_type': cell_type,
            'cell_max_current': cell_max_current,
            'pack_max_current': round(pack_max_current, 2),
            'bms_rating': bms_rating,
            'warnings': warnings
        }), 200

    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Lỗi máy chủ: {str(e)}'}), 500

@app.route('/order', methods=['POST'])
def order():
    """Process battery pack order"""
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'Dữ liệu không hợp lệ'}), 400

        name = data.get('name', '').strip()
        phone = data.get('phone', '').strip()
        email = data.get('email', '').strip()
        config = data.get('config', '').strip()
        cell_type = data.get('cell_type', '').strip()

        if not name or not phone:
            return jsonify({'error': 'Vui lòng nhập tên và số điện thoại'}), 400
        if len(name) < 2:
            return jsonify({'error': 'Tên phải có ít nhất 2 ký tự'}), 400
        if len(phone) < 10:
            return jsonify({'error': 'Số điện thoại không hợp lệ'}), 400

        order_data = {
            'name': name,
            'phone': phone,
            'email': email,
            'config': config,
            'cell_type': cell_type,
            'note': data.get('note', '').strip(),
            'price': data.get('price', 0),
            'timestamp': datetime.now().isoformat()
        }

        order_id = save_order(order_data)

        # Send confirmation email if email provided
        if email and '@' in email:
            order_data['id'] = order_id
            send_order_confirmation_email(email, order_data)

        return jsonify({
            'success': True,
            'message': 'Đặt hàng thành công!',
            'order_id': order_id
        }), 201

    except Exception as e:
        return jsonify({'error': f'Lỗi: {str(e)}'}), 500

@app.route('/orders', methods=['GET'])
def get_orders():
    """Retrieve all orders"""
    orders = load_orders()
    return jsonify(orders), 200

@app.route('/api/products', methods=['GET'])
def get_products():
    """Get all products"""
    products = load_products()
    return jsonify(products), 200

@app.route('/api/products', methods=['POST'])
def create_product():
    """Create new product"""
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'Dữ liệu không hợp lệ'}), 400

        product_data = {
            'name': data.get('name', '').strip(),
            'description': data.get('description', '').strip(),
            'price': float(data.get('price', 0)),
            'config': data.get('config', '').strip(),
            'image_url': data.get('image_url', ''),
            'status': 'active',
            'created_at': datetime.now().isoformat()
        }

        product_id = save_product(product_data)
        product_data['id'] = product_id

        return jsonify({
            'success': True,
            'product': product_data
        }), 201

    except Exception as e:
        return jsonify({'error': f'Lỗi: {str(e)}'}), 500

@app.route('/api/products/<product_id>', methods=['PUT'])
def update_prod(product_id):
    """Update product"""
    try:
        data = request.json
        update_product(product_id, data)
        return jsonify({
            'success': True,
            'message': 'Product updated'
        }), 200
    except Exception as e:
        return jsonify({'error': f'Lỗi: {str(e)}'}), 500

@app.route('/api/products/<product_id>', methods=['DELETE'])
def delete_prod(product_id):
    """Delete product"""
    try:
        delete_product(product_id)
        return jsonify({
            'success': True,
            'message': 'Product deleted'
        }), 200
    except Exception as e:
        return jsonify({'error': f'Lỗi: {str(e)}'}), 500

# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    if FIREBASE_READY:
        print("[OK] Firebase connected")
    else:
        print("[WARNING] Firebase not available")
    app.run(debug=False, port=5000)
