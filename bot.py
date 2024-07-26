from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os

def start(update, context):
    update.message.reply_text('Привіт! Надішліть мені файл електронної книги, і я конвертую його у формат MOBI.')

def convert_file(update, context):
    file = context.bot.getFile(update.message.document.file_id)
    file_extension = file.file_path.split('.')[-1]
    input_file = 'input.' + file_extension
    output_file = 'output.mobi'
    
    file.download(input_file)
    
    # Використовуйте Calibre для конвертації
    os.system(f'ebook-convert {input_file} {output_file}')

    context.bot.send_document(chat_id=update.message.chat_id, document=open(output_file, 'rb'))

def main():
    updater = Updater(os.getenv('TELEGRAM_TOKEN'), use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.document, convert_file))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
