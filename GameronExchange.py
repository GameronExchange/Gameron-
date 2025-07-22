
import telebot
from PIL import Image, ImageDraw, ImageFont
import datetime
import io

# ==== تنظیمات اصلی ====
BOT_TOKEN = "7466286463:AAE3KHAvPZIImO8wOWnDYPNhvfXhu6cR-Dk"
CHANNEL_ID = -1001437727950  # Chat ID کانال شما

bot = telebot.TeleBot(BOT_TOKEN)

# ==== تابع ساخت تصویر ====
def generate_rate_image(rates: dict):
    width, height = 1080, 1350
    image = Image.new("RGB", (width, height), (15, 15, 15))
    draw = ImageDraw.Draw(image)

    font_large = ImageFont.truetype("arial.ttf", 60)
    font_medium = ImageFont.truetype("arial.ttf", 44)
    font_small = ImageFont.truetype("arial.ttf", 36)

    # Header
    title = "💱 نرخ لحظه‌ای امروز ترکیه 🇹🇷"
    draw.text((width//2 - draw.textlength(title, font=font_large)//2, 80), title, fill="white", font=font_large)

    # Rates
    start_y = 200
    spacing = 95
    for idx, (cur, val) in enumerate(rates.items()):
        line = f"{cur}: {val} تومان"
        draw.text((100, start_y + idx * spacing), line, fill="#00ffcc", font=font_medium)

    # Slogans
    slogan1 = "✅ راحتی و سرعت در معاملات شما اولویت ماست"
    slogan2 = "✅ راه حلی ساده و مطمئن برای تبدیل ارزهای دیجیتالی"
    draw.text((100, start_y + len(rates)*spacing + 30), slogan1, fill="#bbbbbb", font=font_small)
    draw.text((100, start_y + len(rates)*spacing + 90), slogan2, fill="#bbbbbb", font=font_small)

    # Footer
    footer = "@Exchange_Gameron   |   +90 541 603 4749"
    draw.text((width//2 - draw.textlength(footer, font=font_small)//2, height - 100), footer, fill="#999999", font=font_small)

    # Save to Bytes
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='JPEG')
    img_byte_arr.seek(0)
    return img_byte_arr

# ==== پردازش دستور /setrates ====
@bot.message_handler(commands=['setrates'])
def handle_setrates(message):
    lines = message.text.split('\n')[1:]
    rates = {}
    for line in lines:
        try:
            key, val = line.split(":")
            rates[key.strip().upper()] = val.strip()
        except:
            continue

    if not rates:
        bot.reply_to(message, "❗️فرمت نرخ‌ها صحیح نیست. مثال:
/setrates\nUSD: 88000")
        return

    img = generate_rate_image(rates)
    bot.send_photo(CHANNEL_ID, img, caption="📊 نرخ لحظه‌ای ارسال شد توسط @Gameron_Exchangebot")

# ==== شروع ربات ====
print("🤖 GameronBot is running...")
bot.infinity_polling()
