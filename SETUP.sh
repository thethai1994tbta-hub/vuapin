#!/bin/bash
# Quick setup script for development

echo "🔧 Vua Pin - Setup Script"
echo "========================="

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Install Python 3.8+ first."
    exit 1
fi
echo "✅ Python found: $(python3 --version)"

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate venv
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -q -r requirements.txt

# Create .env if not exists
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "📝 Created .env from .env.example - edit it with your settings"
fi

# Initialize database
echo "💾 Initializing database..."
python3 -c "from server import init_db; init_db()"

echo ""
echo "✅ Setup complete!"
echo ""
echo "To start the app:"
echo "  source venv/bin/activate"
echo "  python server.py"
echo ""
echo "Access at: http://127.0.0.1:5000"
