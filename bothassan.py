from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters
import marshal
import base64
import os

# توكن البوت
BOT_TOKEN = '8167193890:AAHL6MVkEUO6L_oQ_moYSTojOI4Bv22CbnU'

# بدء الاستخدام
async def start(update: Update, context):
    keyboard = [[InlineKeyboardButton("بدء الاستخدام", callback_data='start_use')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("مرحبًا! كيف يمكنني مساعدتك اليوم؟", reply_markup=reply_markup)

# معالجة الأزرار
async def button(update: Update, context):
    query = update.callback_query
    await query.answer()
    if query.data == 'start_use':
        keyboard = [
            [InlineKeyboardButton("المطور", url='http://t.me/@a_4pa')],
            [InlineKeyboardButton("تشفير كود بايثون 💀🔥", callback_data='encrypt_code')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="ماذا تود أن تفعل؟", reply_markup=reply_markup)
    elif query.data == 'encrypt_code':
        await query.edit_message_text(text="الرجاء إرسال ملف بايثون لتشفيره.")

# معالجة ملفات بايثون
async def handle_document(update: Update, context):
    file = await update.message.document.get_file()
    file_path = await file.download_to_drive(custom_path='./temp_python_file.py')

    # قراءة الكود من الملف
    with open(file_path, 'r') as f:
        code = f.read()

    # تشفير الكود
    compiled_code = compile(code, '', 'exec')
    marshalled_code = marshal.dumps(compiled_code)
    encoded_code = base64.b64encode(marshalled_code).decode()
    encrypted_code = f"exec(__import__('marshal').loads(__import__('base64').b64decode({repr(encoded_code)})))"

    # كتابة الكود المشفر إلى ملف جديد
    output_file_path = 'Bytcode_python.py'
    with open(output_file_path, 'w') as f:
        f.write(encrypted_code)

    # إرسال الملف المشفر إلى المستخدم
    await update.message.reply_text("جار التشفير...")
    await update.message.reply_document(document=open(output_file_path, 'rb'))

    # حذف الملفات المؤقتة
    os.remove(file_path)
    os.remove(output_file_path)

# إعداد التطبيق والبوت
app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler('start', start))
app.add_handler(CallbackQueryHandler(button))
app.add_handler(MessageHandler(filters.Document.FileExtension('py'), handle_document))

print("بوت التلغرام جاهز للعمل...")
app.run_polling()
