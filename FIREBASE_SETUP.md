# Firebase Setup for Vua Pin

## What Changed
- ✅ Switched from SQLite to Firebase Realtime Database
- ✅ Orders now stored in Firebase (cloud, real-time)
- ✅ Products now stored in Firebase (cloud, real-time)
- ✅ All data syncs automatically
- ✅ Better scalability and reliability

## Setup Instructions

### 1. Enable Realtime Database in Firebase Console
1. Go to https://console.firebase.google.com
2. Select project "Spaa"
3. In left menu, click "Realtime Database"
4. Click "Create Database"
5. Choose region: `asia-southeast1` (or your closest region)
6. Start in "Test mode" (for now)

### 2. Get Firebase Credentials (Already Done!)
You have: `gen-lang-client-0661551951-firebase-ad...json`

### 3. Set Environment Variable on Railway

**Important:** Railway needs the Firebase credentials as a single environment variable.

**Steps:**
1. Open the JSON file you downloaded
2. Copy the ENTIRE JSON content (everything from `{` to `}`)
3. In Railway dashboard:
   - Go to your service "web"
   - Click "Variables" tab
   - Click "+ New Variable"
   - Name: `FIREBASE_CREDENTIALS`
   - Value: Paste the entire JSON content
   - Click Add

**Example format:**
```
{"type":"service_account","project_id":"gen-lang-client-0661551951","private_key_id":"ba473989b895efad7e58c864eb9809a8e5a4defe",...rest of json...}
```

### 4. Deploy
Push code to GitHub → Railway auto-deploys with Firebase support

```bash
git add .
git commit -m "Switch to Firebase Realtime Database"
git push origin main
```

## Firebase Database Structure

### `/orders` Collection
Stores all customer orders:
```json
{
  "orders": {
    "pushKey1": {
      "name": "Nguyễn Văn A",
      "phone": "0909111111",
      "email": "user@example.com",
      "config": "10S4P",
      "price": 50000,
      "timestamp": "2026-04-22T12:00:00"
    }
  }
}
```

### `/products` Collection
Stores product catalog:
```json
{
  "products": {
    "pushKey2": {
      "name": "Battery Pack 48V",
      "description": "High drain battery pack",
      "price": 2000000,
      "config": "12S4P",
      "image_url": "https://...",
      "status": "active"
    }
  }
}
```

## Testing Firebase Connection

### Check if Connected
Go to your live app URL and try:
1. Create new order → Check Firebase console to see it appear
2. View orders → Should load from Firebase
3. Check console logs for "[OK] Firebase connected"

### If Not Connected
Check:
1. `FIREBASE_CREDENTIALS` env var is set (Railway Variables)
2. Credentials JSON is valid (check if pasting corrupted it)
3. Realtime Database is enabled in Firebase console
4. Database URL matches: `asia-southeast1` region

## Database URL
```
https://gen-lang-client-0661551951-default-rtdb.asia-southeast1.firebaseio.com
```

## Security Rules (Test Mode)
Currently set to **Test Mode** - anyone can read/write

**For production, update rules:**
```json
{
  "rules": {
    "orders": {
      ".read": true,
      ".write": true
    },
    "products": {
      ".read": true,
      ".write": "auth != null"
    }
  }
}
```

## Monitoring Data
1. Firebase console → Realtime Database tab
2. View all orders and products in real-time
3. Edit/delete data directly (careful!)

## Fallback
If Firebase not available, app uses fallback (in-memory storage - data lost on restart)

## Questions?
Contact: thethai1994tbta@gmail.com
