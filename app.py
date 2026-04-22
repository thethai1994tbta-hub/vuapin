from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import json
from datetime import datetime
import os
import math

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

ORDERS_FILE = "orders.json"

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

def load_orders():
    if os.path.exists(ORDERS_FILE):
        with open(ORDERS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_orders(orders):
    with open(ORDERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(orders, f, ensure_ascii=False, indent=2)

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

@app.route('/', methods=['GET'])
def home():
    return send_file('index.html')

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
        # Series calculation: round up to meet target voltage
        S = math.ceil(target_voltage / v_cell)

        # Capacity: parallel cells add up
        capacity = ah_cell * parallel

        # Actual pack voltage
        pack_voltage = S * v_cell

        # Energy in Wh
        energy = pack_voltage * capacity

        # Total number of cells
        total_cells = S * parallel

        # CRITICAL: BMS Current Calculation (NOT based on Ah)
        # Max current = cell max discharge × number of parallel cells
        pack_max_current = cell_max_current * parallel

        # BMS recommendation: add 20% safety margin
        bms_rating = math.ceil(pack_max_current * 1.2)

        # Voltage extremes
        max_voltage = 4.2 * S  # Fully charged (dangerous)
        min_voltage = 2.5 * S  # Fully discharged (danger)
        nominal_voltage = 3.7 * S

        # Safety checks and warnings
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
        config = data.get('config', '').strip()
        cell_type = data.get('cell_type', '').strip()

        if not name or not phone:
            return jsonify({'error': 'Vui lòng nhập tên và số điện thoại'}), 400

        if len(name) < 2:
            return jsonify({'error': 'Tên phải có ít nhất 2 ký tự'}), 400

        if len(phone) < 10:
            return jsonify({'error': 'Số điện thoại không hợp lệ'}), 400

        order_data = {
            'id': len(load_orders()) + 1,
            'name': name,
            'phone': phone,
            'config': config,
            'cell_type': cell_type,
            'note': data.get('note', '').strip(),
            'price': data.get('price', 0),
            'timestamp': datetime.now().isoformat()
        }

        orders = load_orders()
        orders.append(order_data)
        save_orders(orders)

        return jsonify({
            'success': True,
            'message': 'Đặt hàng thành công!',
            'order_id': order_data['id']
        }), 201

    except Exception as e:
        return jsonify({'error': f'Lỗi: {str(e)}'}), 500

@app.route('/orders', methods=['GET'])
def get_orders():
    """Retrieve all orders"""
    return jsonify(load_orders()), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
