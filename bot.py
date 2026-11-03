import os
from pyrogram import Client, filters
from pyrogram.types import Message
import yt_dlp

# بيانات البوت الخاصة بك
API_ID = 32792948
API_HASH = "ea261c5fe76661637762a69f794792fd"
BOT_TOKEN = "9266395999:AAGSNlTKpB4th7_TZweFizcxDbaucy-8IMY"

# تشغيل البوت
app = Client(
    "video_downloader_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

@app.on_message(filters.command("start"))
async def start_command(client, message: Message):
    await message.reply_text(
        "👋 أهلاً بك! أرسل لي أي رابط فيديو (من يوتيوب، تيك توك، وغيرها) وسأقوم بتحميله وإرساله لك فوراً."
    )

@app.on_message(filters.text & ~filters.command(["start"]))
async def download_video(client, message: Message):
    url = message.text.strip()
    if not url.startswith("http"):
        await message.reply_text("❌ الرجاء إرسال رابط صالح يبدأ بـ http أو https.")
        return
        
    status_msg = await message.reply_text("⏳ جاري التحميل، يرجى الانتظار...")
    
    output_dir = "downloads"
    os.makedirs(output_dir, exist_ok=True)
    
    ydl_opts = {
        'outtmpl': f'{output_dir}/%(title)s.%(ext)s',
        'format': 'best',
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)
            
        await status_msg.edit_text("📤 جاري رفع الفيديو إلى تيليجرام...")
        await message.reply_video(video=file_path, caption=info.get('title', 'Video'))
        
        # تنظيف الملفات بعد الإرسال
        if os.path.exists(file_path):
            os.remove(file_path)
            
        await status_msg.delete()
    except Exception as e:
        await status_msg.edit_text(f"❌ حدث خطأ أثناء التحميل: {str(e)}")

print("🤖 البوت يعمل الآن بنجاح...")
app.run()
