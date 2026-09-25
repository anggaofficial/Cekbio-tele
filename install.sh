#!/bin/bash

echo "🔄 Mengupdate package manager..."
pkg update -y

echo "📦 Menginstall Python..."
pkg install python -y

echo "📦 Menginstall pip..."
pkg install python-pip -y

echo "📦 Menginstall dependencies..."
pip install -r requirements.txt

echo "✅ Instalasi selesai!"
echo ""
echo "📝 Langkah selanjutnya:"
echo "1. Buka bot.py dengan editor"
echo "2. Ganti TOKEN dengan bot token Anda"
echo "3. Jalankan: python bot.py"
