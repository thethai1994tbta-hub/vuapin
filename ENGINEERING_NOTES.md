# Pin Lithium Thái Nguyên - Công cụ thiết kế kỹ thuật

## 🔧 Sửa chữa kỹ thuật

### 1. BMS Calculation - FIXED ✅

**Problem:**
- Cách tính cũ: `BMS = Ah × 1.2` (SAI)
- Dẫn đến: BMS đề xuất không chính xác

**Giải pháp mới (ĐÚNG):**
```
1. Mỗi tế bào có khả năng xả dòng tối đa (A):
   - Loại rẻ: 5A/cell
   - Standard 18650: 10A/cell
   - High Drain: 20A/cell
   - Premium: 30A/cell

2. Pack max current = cell_max_current × P (số cell song song)

3. BMS rating = pack_max_current × 1.2 (an toàn)
```

**Ví dụ:**
```
Cấu hình: 13S10P (Standard 18650)
- Cell max discharge: 10A
- Pack max = 10A × 10P = 100A
- BMS recommend = 100A × 1.2 = 120A ✅

Vs cách cũ:
- Capacity = 30Ah
- BMS = 30 × 1.2 = 36A ❌ (SAI!)
```

### 2. Voltage Calculations - VERIFIED ✅

**Series (S):** `ceil(target_voltage / nominal_voltage)`
```
48V / 3.7V = 12.97 → S = 13 ✅
```

**Actual voltage:** `S × v_cell = 13 × 3.7 = 48.1V` ✅

**Max voltage:** `4.2V/cell × S = 4.2 × 13 = 54.6V`
(Max safe voltage when fully charged)

**Min voltage:** `2.5V/cell × S = 2.5 × 13 = 32.5V`
(Cutoff voltage for safety)

### 3. Capacity & Energy - CORRECT ✅

**Capacity:** `cell_capacity × P = 3Ah × 10P = 30Ah`

**Energy:** `voltage × capacity = 48.1V × 30Ah = 1443Wh`

### 4. Safety Warnings - IMPLEMENTED ✅

Tự động cảnh báo khi:
- ⚠️ Điện áp > 72V (nguy hiểm cao)
- ⚠️ Dung lượng > 200Ah (khó quản lý)
- ⚠️ P > 20 (khó cân bằng)
- ⚠️ S > 30 (rủi ro điện áp cao)

---

## 📊 Test Results

### Test 1: Standard 13S10P
```
Input: v_cell=3.7, ah=3, target=48V, parallel=10, type=Standard
Output:
  Config: 13S10P
  Voltage: 48.1V
  Capacity: 30Ah
  Energy: 1443Wh
  Cell max: 10A
  Pack max: 100A
  BMS: 120A ✅
```

### Test 2: High Voltage (100V) - Warning System
```
Input: v_cell=3.7, ah=3, target=100V, parallel=10, type=Cheap
Output:
  Config: 28S10P
  Voltage: 103.6V
  Warnings: ⚠️ Điện áp cao (>72V)
  Cell max: 5A
  Pack max: 50A
  BMS: 60A ✅
```

### Test 3: BMS by Cell Type
```
Cell Type → Max/cell × 10P → BMS (×1.2)
─────────────────────────────────────
Cheap       5A × 10 = 50A   → 60A
Standard   10A × 10 = 100A  → 120A
High Drain 20A × 10 = 200A  → 240A
Premium    30A × 10 = 300A  → 360A
```

---

## 🎯 Tính năng mới

### 1. Cell Type Selector
- Loại rẻ (5A) - Giá rẻ, dòng thấp
- Standard (10A) - Cân bằng
- High Drain (20A) - Xe điện, công cụ
- Premium (30A) - Ứng dụng cao cấp

### 2. Safety Notes
```
⚠️ Lưu ý an toàn:
- Không trộn cell cũ/mới
- Cần BMS chất lượng cao
- Cân bằng cells trước lắp ráp
- Đặt tường cháy giữa cells
- Kiểm tra điện áp thường xuyên
```

### 3. Current/BMS Display
- Cell max current (A/cell)
- Pack max current (dòng xả tối đa)
- BMS rating (đề xuất + an toàn)

### 4. Advanced Specs
- Total cells (S × P)
- Max/Min voltage
- Nominal voltage
- Energy (Wh)

---

## 🛠️ Code Quality

### Backend (Flask)
✅ Input validation (min/max ranges)
✅ Cell type database
✅ Engineering-correct calculations
✅ Safety warning system
✅ Proper HTTP status codes
✅ Error handling
✅ Vietnamese localization

### Frontend (HTML/JS)
✅ Cell type selector with descriptions
✅ Real-time validation
✅ Loading states
✅ Error messages
✅ Result cards (not plain text)
✅ Safety notes display
✅ Auto-fill order form
✅ Responsive design

---

## 📐 Engineering Standards

✓ Voltage calculation: Series cells in series (not parallel)
✓ Capacity calculation: Parallel cells add capacity
✓ BMS rating: Based on cell discharge capability
✓ Safety margins: 20% for BMS (1.2x)
✓ Voltage limits: 4.2V max, 2.5V min per cell
✓ Warnings: Automatic for high voltage/capacity

---

## 🚀 Production Ready

This tool is now suitable for:
- Real battery pack design
- Customer consultations
- Order management
- Engineering calculations
- Safety compliance

Keep this tool accurate and safe for customer battery packs!
