from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from pysaucenao import SauceNao
from config import token, snao_key

#token: Final = 'Telegram Bot Token Here' # within config.py
bot_username: Final = '@SauceHunter_Bot'
#snao_key: str = "SauceNAO API Key Here" # within config.py
snao_sim: int = 70
sauce = SauceNao(api_key=snao_key, min_similarity=snao_sim)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello! I am SauceHunter Bot. I can help you find the source of an image. Just send me an image and I will do the rest!')

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Help Message')

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('The test worked!')

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
    
async def getImage(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = await update.message.photo[-1].get_file()
    url = file.file_path
    print(f'Received Image {url} from User {update.message.chat.username} ({update.message.chat.id})')
    results = await sauce.from_url(url)
    if results:
        results = sorted(results, key = lambda x: x.similarity, reverse=True)
        print(f'Found {len(results)} results for {url}')
        for result in results:
            if result.source_url is not None: 
                preview = None
                if hasattr(result, 'thumbnail'): preview = result.thumbnail
                response = f'<b>{result.title}</b>\n'
                response += f'<i>{result.similarity}% Match!</i>'
                if result.authors:
                    response += '\n'
                    if len(result.authors) == 1: response += '\nAuthor:\n'
                    elif len(result.authors) > 1: response += '\nAuthors:\n'
                    for author in result.authors: response += f'<i>{author}</i>'
                if hasattr(result, 'characters'):
                    response += '\n'
                    charNum: int = 0
                    if len(result.characters) == 1: response += '\nCharacter:\n'
                    elif len(result.characters) > 1: response += '\nCharacters:\n'
                    for character in result.characters:
                        charNum += 1
                        response += f'<i>{character}</i>'
                        if len(result.characters) > 1 and charNum != len(result.characters): response += ', '
                response += '\n\nSource:'
                response += f'\n{result.source_url}'
                if result.urls: 
                    for url in result.urls:
                        if url != result.source_url:
                            response += f'\n{url}'
                if preview is not None: 
                    await update.message.reply_photo(photo=preview, caption=response, parse_mode='HTML')
                else: await update.message.reply_text(response, parse_mode='HTML', disable_web_page_preview=True)
                print(f'Bot: {response}')
            else: pass
    else: await update.message.reply_text(f'No results found for the image. At least, not above {snao_sim}% similarity.')
    
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')
    
if __name__ == '__main__':
    print ('Bot is running...')
    app = Application.builder().token(token).build()
    
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('help', help))
    app.add_handler(CommandHandler('info', info))
    
    app.add_handler(MessageHandler(filters.TEXT, sendMessage))
    app.add_handler(MessageHandler(filters.PHOTO, getImage))
    
    app.add_error_handler(error)
    
    print('Polling...')
    app.run_polling(poll_interval=2)