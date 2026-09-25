#!/bin/bash

echo "🤖 WhatsApp Log Filter Bot"
echo "=========================="
echo ""

while true; do
    echo "▶️ Bot sedang berjalan... ($(date))"
    python bot.py

    echo ""
    echo "❌ Bot crashed atau dihentikan"
    echo "🔄 Akan restart dalam 10 detik..."
    sleep 10
done
