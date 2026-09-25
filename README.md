# Cekbio-tele
I Created a Telegram Button Bot by Looking at Wa's Checkbio

# Setup Bot Telegram WhatsApp Log Filter di Termux

## 📋 Prasyarat
- Termux terinstal
- Internet aktif
- Bot Token dari BotFather (@BotFather di Telegram)

## 🚀 Langkah Instalasi

### 1. Pastikan semua file ada
Pastikan file di folder yang sama:
- `bot.py`
- `requirements.txt`
- `install.sh`
- `run.sh`

### 2. Memberikan Permission ke Script
```bash
chmod +x install.sh
chmod +x run.sh
```

### 3. Jalankan Instalasi
```bash
bash install.sh
```

### 4. Setup Bot Token
Buka `bot.py` dan ubah baris ini:
```python
TOKEN = 'YOUR_BOT_TOKEN_HERE'
```
Dengan token bot Anda yang sebenarnya dari BotFather.

### 5. Jalankan Bot
Pilih salah satu cara:

**Cara 1: Langsung (testing)**
```bash
python bot.py
```

**Cara 2: Dengan Auto-restart**
```bash
bash run.sh
```

## 📱 Cara Menggunakan Bot

1. Cari bot Anda di Telegram
2. Kirimkan `/start` untuk memulai
3. Kirimkan file `.txt` berisi log WhatsApp
4. Bot akan memfilter dan mengirimkan 3 file hasil

## 📊 Format Output

Bot akan mengirim 3 file:
- `low_meta.txt` - Daftar nomor Low Meta Business
- `dengan_bio.txt` - Nomor WA dengan Bio
- `tanpa_bio.txt` - Nomor WA tanpa Bio

## 🔧 Troubleshooting

### Error: `ModuleNotFoundError: No module named 'telebot'`
```bash
pip install pyTelegramBotAPI
```

### Bot tidak merespons
1. Cek token bot
2. Pastikan internet aktif
3. Lihat `bot.log` untuk error details

## 📝 Log File
Semua aktivitas dicatat di `bot.log`.
Untuk melihat log real-time:
```bash
tail -f bot.log
```
