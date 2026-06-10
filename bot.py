import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
import yt_dlp
from moviepy.editor import VideoFileClip

# GANTI DENGAN TOKEN ANDA
TOKEN = "8649277344:AAHTrSfraFWuJLB2aIVeoLUfu3HtYHF1a8I"

async def start(update, context):
    await update.message.reply_text("Halo! Kirim link YouTube, nanti saya potong jadi Shorts.")

async def button_click(update, context):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(f"Terima kasih atas rating {query.data} bintangnya! ✨")

async def process_video(update, context):
    url = update.message.text
    await update.message.reply_text("Sedang memproses... mohon tunggu sebentar.")
    
    # 1. Download & Potong (Logika Sederhana)
    ydl_opts = {'format': 'best', 'outtmpl': 'vid.mp4'}
    yt_dlp.YoutubeDL(ydl_opts).download([url])
    
    clip = VideoFileClip("vid.mp4")
    sub = clip.subclip(0, 50) # Ambil 50 detik pertama
    w, h = sub.size
    new_w = int(h * 9 / 16)
    cropped = sub.crop(x_center=w/2, width=new_w, height=h)
    cropped.write_videofile("hasil.mp4")
    
    # 2. Kirim dengan tombol Rating
    keyboard = [
        [InlineKeyboardButton("⭐ 1", callback_data='1'), InlineKeyboardButton("⭐⭐ 2", callback_data='2'), InlineKeyboardButton("⭐⭐⭐ 3", callback_data='3')],
        [InlineKeyboardButton("⭐⭐⭐⭐ 4", callback_data='4'), InlineKeyboardButton("⭐⭐⭐⭐⭐ 5", callback_data='5')]
    ]
    await update.message.reply_video(video=open("hasil.mp4", "rb"), reply_markup=InlineKeyboardMarkup(keyboard))
    
    # Bersihkan file
    os.remove("vid.mp4"); os.remove("hasil.mp4")

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, process_video))
app.add_handler(CallbackQueryHandler(button_click))
app.run_polling()
