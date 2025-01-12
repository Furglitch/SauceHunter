from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

token: Final = 'TOKEN HERE'
bot_username: Final = '@SauceHunter_Bot'

# Commands
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello! I am SauceHunter Bot. I can help you find the source of an image. Just send me an image and I will do the rest!')

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Help Message')

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('The test worked!')


# Responses
def getMessage(text: str) -> str:
    processed: str = text.lower()
    
    if 'hello' in processed:
        return 'Hello! How can I help you?'
    
    if 'bye' in processed:
        return 'Goodbye! Have a great day!'
    
    if 'help' in processed:
        return 'Help Message'
    
    return 'I am sorry, I did not understand that.'
    
async def sendMessage(update: Update, context: ContextTypes.DEFAULT_TYPE):
    messageType: str = update.message.chat.type
    messageText: str = update.message.text
    
    print(f'User {update.message.chat.username} ({update.message.chat.id}) in {messageType} sent: {messageText}')
    
    if messageType == 'group':
        if bot_username in messageText:
            response: str = getMessage(messageText.replace(bot_username, '').strip())
        else: return
    else:
        response: str = getMessage(messageText)
    
    print(f'Bot: {response}')
    await update.message.reply_text(response)
    
# Image Handling
async def getImage(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = await update.message.photo[-1].get_file()
    url = file.file_path
    print(f'Received Image {url} from User {update.message.chat.username} ({update.message.chat.id})')
    
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')
    
if __name__ == '__main__':
    print ('Bot is running...')
    app = Application.builder().token(token).build()
    
    # Commands
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('help', help))
    app.add_handler(CommandHandler('info', info))
    
    # Messages
    app.add_handler(MessageHandler(filters.TEXT, sendMessage))
    app.add_handler(MessageHandler(filters.PHOTO, getImage))
    
    # Errors
    app.add_error_handler(error)
    
    # Start polling
    print('Polling...')
    app.run_polling(poll_interval=2)