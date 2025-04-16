from typing import Final
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters
import io
from dotenv import load_dotenv
import os
 
load_dotenv()
TOKEN: Final = os.getenv('TELEGRAM_BOT_TOKEN')
BOT_USERNAME: Final = 'Roll_No_Sollu_bot'

# Updated result data per semester --> sample data for the demonstration
ROLL_DATA = ROLL_DATA = {
    '110523106001': {
        'sem1': 'Math: 89\nPhysics: 91\nCGPA: 8.5\nNote: not real grades, just for demonstration',
        'sem2': 'DSA: 84\nDBMS: 88\nCGPA: 8.6\nNote: not real grades, just for demonstration',
        'sem3': 'OS: 81\nCN: 83\nCGPA: 8.4\nNote: not real grades, just for demonstration',
        'sem4': 'AI: 90\nML: 87\nCGPA: 9.0\nNote: not real grades, just for demonstration',
    },
    '614523106002': {
        'sem1': 'Math: 80\nPhysics: 85\nCGPA: 8.0\nNote: not real grades, just for demonstration',
        'sem2': 'DSA: 76\nDBMS: 82\nCGPA: 8.1\nNote: not real grades, just for demonstration',
        'sem3': 'OS: 79\nCN: 82\nCGPA: 8.0\nNote: not real grades, just for demonstration',
        'sem4': 'AI: 88\nML: 84\nCGPA: 8.3\nNote: not real grades, just for demonstration',
    },
    '310523106003': {
        'sem1': 'Math: 75\nPhysics: 80\nCGPA: 7.9\nNote: not real grades, just for demonstration',
        'sem2': 'DSA: 78\nDBMS: 79\nCGPA: 7.8\nNote: not real grades, just for demonstration',
        'sem3': 'OS: 72\nCN: 74\nCGPA: 7.7\nNote: not real grades, just for demonstration',
        'sem4': 'AI: 85\nML: 82\nCGPA: 8.1\nNote: not real grades, just for demonstration',
    },
    '610523105004': {
        'sem1': 'Math: 90\nPhysics: 88\nCGPA: 8.7\nNote: not real grades, just for demonstration',
        'sem2': 'DSA: 92\nDBMS: 89\nCGPA: 8.8\nNote: not real grades, just for demonstration',
        'sem3': 'OS: 85\nCN: 87\nCGPA: 8.9\nNote: not real grades, just for demonstration',
        'sem4': 'AI: 93\nML: 91\nCGPA: 9.2\nNote: not real grades, just for demonstration',
    },
    '610524106005': {
        'sem1': 'Math: 88\nPhysics: 86\nCGPA: 8.4\nNote: not real grades, just for demonstration',
        'sem2': 'DSA: 80\nDBMS: 85\nCGPA: 8.5\nNote: not real grades, just for demonstration',
        'sem3': 'OS: 83\nCN: 85\nCGPA: 8.3\nNote: not real grades, just for demonstration',
        'sem4': 'AI: 91\nML: 89\nCGPA: 9.0\nNote: not real grades, just for demonstration',
    },
    '610523106066': {
        'sem1': 'Math: 78\nPhysics: 80\nCGPA: 7.8\nNote: not real grades, just for demonstration',
        'sem2': 'DSA: 75\nDBMS: 79\nCGPA: 7.7\nNote: not real grades, just for demonstration',
        'sem3': 'OS: 72\nCN: 75\nCGPA: 7.6\nNote: not real grades, just for demonstration',
        'sem4': 'AI: 82\nML: 80\nCGPA: 8.0\nNote: not real grades, just for demonstration',
    },
    '610553106097': {
        'sem1': 'Math: 85\nPhysics: 88\nCGPA: 8.3\nNote: not real grades, just for demonstration',
        'sem2': 'DSA: 81\nDBMS: 83\nCGPA: 8.4\nNote: not real grades, just for demonstration',
        'sem3': 'OS: 78\nCN: 81\nCGPA: 8.2\nNote: not real grades, just for demonstration',
        'sem4': 'AI: 86\nML: 85\nCGPA: 8.6\nNote: not real grades, just for demonstration',
    },
    '610523106041' : {
        'sem1': 'Math: 85\nPhysics: 88\nCGPA: 8.3\nNote: not real grades, just for demonstration',
        'sem2': 'DSA: 81\nDBMS: 83\nCGPA: 8.4\nNote: not real grades, just for demonstration',
        'sem3': 'OS: 78\nCN: 81\nCGPA: 8.2\nNote: not real grades, just for demonstration',
        'sem4': 'AI: 86\nML: 85\nCGPA: 8.6\nNote: not real grades, just for demonstration',
    }
}


# /start command
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to the *Roll No Sollu Bot*!\n\n"
        "Please enter your **12-digit Roll Number** to access your semester results.\n\n"
        "🛡️ All results are private and will only be shown to you.",
        parse_mode='Markdown'
    )

# /help command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 *Need help? I got you!*\n\n"
        "Here's how to use this bot:\n"
        "1. Enter your **12-digit Roll Number**.\n"
        "2. Select the semester you want to view.\n"
        "3. Download or view your result instantly.\n\n"
        "📝 *Created for our department students.*",
        parse_mode='Markdown'
    )

# Roll number handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip().upper()
    chat_type = update.message.chat.type

    if chat_type != 'private':
        await update.message.reply_text("❗ DM me privately to check your result.")
        return

    if len(text) != 12 or not text.isalnum():
        await update.message.reply_text("⚠️ Please enter a valid 10-digit alphanumeric roll number.")
        return

    if text in ROLL_DATA:
        context.user_data['roll_no'] = text
        keyboard = [
            [InlineKeyboardButton("Semester 1 📘", callback_data='sem1')],
            [InlineKeyboardButton("Semester 2 📗", callback_data='sem2')],
            [InlineKeyboardButton("Semester 3 📕", callback_data='sem3')],
            [InlineKeyboardButton("Semester 4 📙", callback_data='sem4')],
        ]
        await update.message.reply_text(
            "📚 Select a semester to view your result:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    else:
        await update.message.reply_text("❌ Roll number not found in the database. Please check and try again.")
    user = update.effective_user
    print(f'📩 User Message - ID: {user.id}, Name: {user.full_name}, Username: @{user.username}, Roll No: {text}')


# Button handler
async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    semester = query.data
    roll_no = context.user_data.get('roll_no')

    if not roll_no or roll_no not in ROLL_DATA:
        await query.edit_message_text("⚠️ Session expired. Please send your roll number again.")
        return

    result = ROLL_DATA[roll_no].get(semester)
    if not result:
        await query.edit_message_text("❌ Result not available for this semester.")
        return
    
    user = update.effective_user       
    print(f'🎯 Button Click - ID: {user.id}, Name: {user.full_name}, Selected: {semester}, Roll No: {roll_no}')

    async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
        text = update.message.text.strip().upper()
        user = update.effective_user
        print(f'📩 User Message - ID: {user.id}, Name: {user.full_name}, Username: @{user.username}, Roll No: {text}')



    # Create text file for download
    file_content = f"Result for {roll_no} - {semester.upper()}\n\n{result}"
    file_like = io.BytesIO(file_content.encode('utf-8'))
    file_like.name = f"{roll_no}_{semester}.txt"

    await query.edit_message_text(f"📄 Here’s your result for `{semester.upper()}`:", parse_mode='Markdown')
    await query.message.reply_document(InputFile(file_like))

# Error logging
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    print(f"⚠️ Error: {context.error}")

# Admin update command
async def update_results(update: Update, context: ContextTypes.DEFAULT_TYPE):
    admin_id = 6354409284  # your Telegram ID
    if update.message.chat.id != admin_id:
        await update.message.reply_text("❌ You do not have permission to update results.")
        return
    try:
        roll_no = context.args[0].upper()
        semester = context.args[1].lower()
        result = " ".join(context.args[2:])
        if roll_no not in ROLL_DATA:
            ROLL_DATA[roll_no] = {}
        ROLL_DATA[roll_no][semester] = result
        await update.message.reply_text(f"✅ Result updated for {roll_no} - {semester}:\n\n{result}")
    except IndexError:
        await update.message.reply_text("⚠️ Usage: /update <ROLL_NO> <SEMESTER> <RESULT>")

# Main runner
if __name__ == '__main__':
    print("🤖 Bot is starting...")

    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('update', update_results))

    # Message handler for roll number
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    

    # Button callback handler
    app.add_handler(CallbackQueryHandler(button_click))

    # Error handler
    app.add_error_handler(error_handler)

    print("🚀 Bot is polling...")
    app.run_polling(poll_interval=3)
