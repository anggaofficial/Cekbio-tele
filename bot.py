# Simpan kode ini dengan nama bot.py
import telebot
import re
import os
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Masukkan Token Bot Telegram Anda di sini
TOKEN = '8638762282:AAGi2_rs4IYXGZyg2Y4fzfxVCS2CV07t-vQ'
bot = telebot.TeleBot(TOKEN)


def parse_whatsapp_log(content):
    """
    Parse WhatsApp log dan pisahkan berdasarkan kategori
    """
    try:
        # Regex untuk mencari blok Low Meta Business
        meta_business_matches = re.findall(
            r'\[\d+\] Nomor:\s+(\+\d+)\s+\(Low Meta Business\).*?Business Details:(.*?)(?=\n\[\d+\]|==+|$)',
            content, re.DOTALL
        )

        low_meta_business = []
        for num, details in meta_business_matches:
            detail_dict = {"Nomor": num}
            for line in details.strip().split('\n'):
                line = line.replace('├', '').replace('└', '').strip()
                if ':' in line:
                    key, val = line.split(':', 1)
                    detail_dict[key.strip()] = val.strip()
            low_meta_business.append(detail_dict)

        # Regex untuk WA Biasa Dengan Bio
        wa_bio_section = re.search(r'\[ WA BIASA DENGAN BIO \].*?(?===+|$)', content, re.DOTALL)
        wa_biasa_dengan_bio = []
        if wa_bio_section:
            bio_matches = re.findall(r'\[\d+\] Nomor:\s+(\+\d+)\s*\nBio:\s*(.*?)(?=\n\[\d+\]|\nSet:|$)', wa_bio_section.group(0))
            for num, bio in bio_matches:
                wa_biasa_dengan_bio.append({"Nomor": num, "Bio": bio.strip()})

        # Regex untuk WA Biasa Tanpa Bio
        wa_tanpa_bio_section = re.search(r'\[ WA BIASA TANPA BIO \].*?$', content, re.DOTALL)
        wa_biasa_tanpa_bio = []
        if wa_tanpa_bio_section:
            tanpa_bio_matches = re.findall(r'\[\d+\] Nomor:\s+(\+\d+)', wa_tanpa_bio_section.group(0))
            wa_biasa_tanpa_bio = list(set(tanpa_bio_matches))

        logger.info(f"Parsed: {len(low_meta_business)} Low Meta, {len(wa_biasa_dengan_bio)} dengan Bio, {len(wa_biasa_tanpa_bio)} tanpa Bio")
        return low_meta_business, wa_biasa_dengan_bio, wa_biasa_tanpa_bio

    except Exception as e:
        logger.error(f"Error parsing WhatsApp log: {str(e)}")
        raise


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    """Handler untuk command /start dan /help"""
    welcome_text = """
👋 *Selamat Datang di WhatsApp Log Filter Bot!*

📝 *Cara Penggunaan:*
1. Kirimkan file log WhatsApp (.txt)
2. Atau kirim teks log langsung
3. Bot akan memfilter dan memisahkan nomor berdasarkan kategori

📊 *Kategori Output:*
• 🔹 Low Meta Business
• 🔹 WA Biasa dengan Bio
• 🔹 WA Biasa tanpa Bio

💡 *Tips:*
- Pastikan format log sesuai dengan standar
- File akan dihapus setelah diproses
- Proses mungkin membutuhkan beberapa detik untuk file besar
    """
    bot.reply_to(message, welcome_text, parse_mode='Markdown')
    logger.info(f"User {message.chat.id} memulai bot")


@bot.message_handler(commands=['status'])
def send_status(message):
    """Handler untuk command /status"""
    status_text = "✅ Bot sedang berjalan dengan baik dan siap memproses data."
    bot.reply_to(message, status_text)
    logger.info(f"User {message.chat.id} mengecek status")


@bot.message_handler(content_types=['document'])
def handle_document(message):
    """Handler untuk file dokumen"""
    try:
        if message.document.mime_type != 'text/plain':
            bot.reply_to(message, "❌ Hanya file .txt yang diterima!")
            return

        logger.info(f"File diterima dari user {message.chat.id}: {message.document.file_name}")

        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        content = downloaded_file.decode('utf-8', errors='ignore')

        process_log_data(message, content)

    except Exception as e:
        logger.error(f"Error handling document: {str(e)}")
        bot.reply_to(message, f"❌ Terjadi kesalahan saat membaca file: {str(e)}")


@bot.message_handler(content_types=['text'])
def handle_text(message):
    """Handler untuk teks langsung"""
    try:
        logger.info(f"Teks diterima dari user {message.chat.id}")
        content = message.text
        process_log_data(message, content)

    except Exception as e:
        logger.error(f"Error handling text: {str(e)}")
        bot.reply_to(message, f"❌ Terjadi kesalahan: {str(e)}")


def process_log_data(message, content):
    """Process log data dan kirim hasil ke user"""
    try:
        bot.reply_to(message, "⏳ Sedang memproses data, mohon tunggu...")

        low_meta, dengan_bio, tanpa_bio = parse_whatsapp_log(content)

        # Buat nama file dengan timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Buat file hasil
        low_meta_file = f'low_meta_{timestamp}.txt'
        dengan_bio_file = f'dengan_bio_{timestamp}.txt'
        tanpa_bio_file = f'tanpa_bio_{timestamp}.txt'

        with open(low_meta_file, 'w') as f:
            f.write('\n'.join([x['Nomor'] for x in low_meta]))

        with open(dengan_bio_file, 'w') as f:
            f.write('\n'.join([f"{x['Nomor']} | Bio: {x['Bio']}" for x in dengan_bio]))

        with open(tanpa_bio_file, 'w') as f:
            f.write('\n'.join(tanpa_bio))

        response_text = (
            f"📊 *Hasil Ekstraksi Log:*\n\n"
            f"🔹 *Low Meta Business:* {len(low_meta)} nomor\n"
            f"🔹 *WA Biasa dengan Bio:* {len(dengan_bio)} nomor\n"
            f"🔹 *WA Biasa tanpa Bio:* {len(tanpa_bio)} nomor\n\n"
            f"File hasil pemisahan dikirim di bawah ini 👇"
        )
        bot.send_message(message.chat.id, response_text, parse_mode='Markdown')

        if low_meta:
            with open(low_meta_file, 'rb') as f:
                bot.send_document(message.chat.id, f, caption=f"Daftar Low Meta Business ({len(low_meta)} nomor)")

        if dengan_bio:
            with open(dengan_bio_file, 'rb') as f:
                bot.send_document(message.chat.id, f, caption=f"Daftar WA Biasa Dengan Bio ({len(dengan_bio)} nomor)")

        if tanpa_bio:
            with open(tanpa_bio_file, 'rb') as f:
                bot.send_document(message.chat.id, f, caption=f"Daftar WA Biasa Tanpa Bio ({len(tanpa_bio)} nomor)")

        for temp_file in [low_meta_file, dengan_bio_file, tanpa_bio_file]:
            if os.path.exists(temp_file):
                os.remove(temp_file)

        logger.info(f"Data berhasil diproses untuk user {message.chat.id}")

    except Exception as e:
        logger.error(f"Error processing log data: {str(e)}")
        bot.reply_to(message, f"❌ Terjadi kesalahan saat memproses data: {str(e)}")


@bot.message_handler(func=lambda message: True)
def handle_all(message):
    """Handler untuk pesan yang tidak dikenali"""
    bot.reply_to(message, "Maaf, saya tidak mengerti. Gunakan /help untuk informasi lebih lanjut.")


def main():
    """Main function untuk menjalankan bot"""
    logger.info("=" * 50)
    logger.info("Bot WhatsApp Log Filter dimulai...")
    logger.info("=" * 50)

    try:
        bot.infinity_polling(timeout=10, long_polling_timeout=5)
    except Exception as e:
        logger.error(f"Bot error: {str(e)}")
        logger.info("Bot akan restart dalam 5 detik...")
        import time
        time.sleep(5)
        main()


if __name__ == "__main__":
    main()

