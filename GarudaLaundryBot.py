#install package - python-telegram-bot
import datetime
import telegram
import os
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
import logging
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler, ConversationHandler

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Stages
MENU = 1
QRDRYER = 0
QRWASHER = 0
COINDRYER = 0
COINWASHER = 0

QR_WASHER_JOB_INDEX ,QR_DRYER_JOB_INDEX ,COIN_DRYER_JOB_INDEX ,COIN_WASHER_JOB_INDEX = range(4)

TOKEN = "5197491172:AAGetT6QyuScd5mIi9XlKrGQurWVgeUWECc"
NAME = "garulaundrybot"

#Status
QR_DRYER = 'AVAILABLE'
QR_WASHER = 'AVAILABLE'
COIN_DRYER = 'AVAILABLE'
COIN_WASHER = 'AVAILABLE'

#Last Used
QR_DRYER_LAST_USED = ''
QR_WASHER_LAST_USED = ''
COIN_DRYER_LAST_USED = ''
COIN_WASHER_LAST_USED = ''

#List of Jobs
JOB = [0,0,0,0]

#Initialise TelegramBot
Tbot = telegram.Bot(TOKEN) # Fill in Token

def qr_washer_alarm(context: CallbackContext) -> None:
    """Send the alarm message."""
    job = context.job
    context.bot.send_message(job.context, text='Your clothes are ready for collection! Please collect them now so that others may use it')
    global QR_WASHER
    QR_WASHER = 'AVAILABLE'
    
def qr_dryer_alarm(context: CallbackContext) -> None:
    """Send the alarm message."""
    job = context.job
    context.bot.send_message(job.context, text='Your clothes are ready for collection! Please collect them now so that others may use it')
    global QR_DRYER
    QR_DRYER = 'AVAILABLE'

def coin_washer_alarm(context: CallbackContext) -> None:
    """Send the alarm message."""
    job = context.job
    context.bot.send_message(job.context, text='Your clothes are ready for collection! Please collect them now so that others may use it')
    global COIN_WASHER
    COIN_WASHER = 'AVAILABLE'
    
def coin_dryer_alarm(context: CallbackContext) -> None:
    """Send the alarm message."""
    job = context.job
    context.bot.send_message(job.context, text='Your clothes are ready for collection! Please collect them now so that others may use it')
    global COIN_DRYER
    COIN_DRYER = 'AVAILABLE'

def start(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [
            InlineKeyboardButton('Exit', callback_data= 'exit')
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Welcome to Garuda Laundry Bot!\n\nUse the following commands to use this bot:\n/select: Select the washer/dryer that you want to use\n/status: Check the status of Washers and Dryers\n\nThank you for using the bot and do drop me any feedback to make this bot more efficient! @jitterz or @jamesyak', reply_markup=reply_markup)
    return MENU
    
def status(update: Update, context: CallbackContext) -> None:
    global JOB
    global QR_WASHER_JOB_INDEX ,QR_DRYER_JOB_INDEX ,COIN_WASHER_JOB_INDEX ,COIN_WASHER_JOB_INDEX
    global QR_DRYER_LAST_USED ,QR_WASHER_LAST_USED ,COIN_DRYER_LAST_USED ,COIN_WASHER_LAST_USED

    QR_WASHER_TIMER = ''
    if QR_WASHER == 'UNAVAILABLE':
        qr_washer_time = datetime.datetime.now() - JOB[QR_WASHER_JOB_INDEX]
        qr_washer_min = round((1800 - qr_washer_time.total_seconds())//60)
        qr_washer_sec = round((1800 - qr_washer_time.total_seconds())%60)
        QR_WASHER_TIMER = f'{QR_WASHER} for {qr_washer_min}mins and {qr_washer_sec}s by @{QR_WASHER_LAST_USED}'
    if QR_WASHER == 'AVAILABLE':
        QR_WASHER_TIMER = f'{QR_WASHER}. Last used by @{QR_WASHER_LAST_USED}'

    QR_DRYER_TIMER = ''
    if QR_DRYER == 'UNAVAILABLE':
        qr_dryer_time = datetime.datetime.now() - JOB[QR_DRYER_JOB_INDEX]
        qr_dryer_min = round((2400 - qr_dryer_time.total_seconds())//60)
        qr_dryer_sec = round((2400 - qr_dryer_time.total_seconds())%60)
        QR_DRYER_TIMER = f'{QR_DRYER} for {qr_dryer_min}mins and {qr_dryer_sec}s by @{QR_DRYER_LAST_USED}'
    if QR_DRYER == 'AVAILABLE':
        QR_DRYER_TIMER = f'{QR_DRYER}. Last used by @{QR_DRYER_LAST_USED}'

    COIN_DRYER_TIMER = ''
    if COIN_DRYER == 'UNAVAILABLE':     
        coin_dryer_time = datetime.datetime.now() - JOB[COIN_DRYER_JOB_INDEX]
        coin_dryer_min = round((2400 - coin_dryer_time.total_seconds())//60)
        coin_dryer_sec = round((2400 - coin_dryer_time.total_seconds())%60)
        COIN_DRYER_TIMER = f'{COIN_DRYER} for {coin_dryer_min}mins and {coin_dryer_sec}s by @{COIN_DRYER_LAST_USED}'
    if COIN_DRYER == 'AVAILABLE':
        COIN_DRYER_TIMER = f'{COIN_DRYER}. Last used by @{COIN_DRYER_LAST_USED}'

    COIN_WASHER_TIMER = ''
    if COIN_WASHER == 'UNAVAILABLE':
        coin_washer_time = datetime.datetime.now() - JOB[COIN_WASHER_JOB_INDEX]
        coin_washer_min = round((1800 - coin_washer_time.total_seconds())//60)
        coin_washer_sec = round((1800 - coin_washer_time.total_seconds())%60)
        COIN_WASHER_TIMER = f'{COIN_WASHER} for {coin_washer_min}mins and {coin_washer_sec}s by @{COIN_WASHER_LAST_USED}'
    if COIN_WASHER == 'AVAILABLE':
        COIN_WASHER_TIMER = f'{COIN_WASHER}. Last used by @{COIN_WASHER_LAST_USED}'
    
    update.message.reply_text(f'Status of Laundry Machines L11:\n\nQR Washer: {QR_WASHER_TIMER}\n\nQR Dryer: {QR_DRYER_TIMER}\n\nCoin Washer: {COIN_WASHER_TIMER}\n\nCoin Dryer: {COIN_DRYER_TIMER}')

def backtomenu(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton('Exit', callback_data='exits')
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text('Welcome to Garuda Laundry Bot!\n\nUse the following commands to use this bot:\n/select: Select the washer/dryer that you want to use\n/status: Check the status of Washers and Dryers\n\nThank you for using the bot and do drop me any feedback to make this bot more efficient! @jitterz or @jamesyak', reply_markup = reply_markup)
    
def select(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [
            InlineKeyboardButton('QR Washer', callback_data='qr_washer'),
            InlineKeyboardButton('QR Dryer', callback_data='qr_dryer'),
        ],
        [InlineKeyboardButton('Coin Washer', callback_data='coin_washer'),
         InlineKeyboardButton('Coin Dryer', callback_data='coin_dryer')
         ],
        [InlineKeyboardButton('Exit', callback_data='exit')]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Please choose a service:', reply_markup=reply_markup)
    return MENU

def cancel(update: Update, context: CallbackContext) -> int:
    """Returns `ConversationHandler.END`, which tells the
    ConversationHandler that the conversation is over"""
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="Haiyaaa then you call me for what\n\nUse /start again to call me")
    return ConversationHandler.END

def double_confirm(update: Update, context: CallbackContext) -> int:
    """Returns `ConversationHandler.END`, which tells the
    ConversationHandler that the conversation is over"""
    query = update.callback_query
    query.answer()
    #query.edit_message_text(text="See you next time!")

def remove_job_if_exists(name: str, context: CallbackContext) -> bool:
    """Remove job with given name. Returns whether job was removed."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True

def cancel_job (update: Update, context: CallbackContext) -> None:
    """Remove the job if the user changed their mind."""
    chat_id = update.effective_message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    text = 'Timer successfully cancelled!' if job_removed else 'You have no active timer.'
    update.effective_message.reply_text(text)


def double_confirm_qr_dryer_callback(update: Update, _: CallbackContext) -> int:
        query = update.callback_query
        query.answer()
        keyboard = [
        [InlineKeyboardButton('Yes', callback_data='yes_qr_dryer'),
        ],
        [InlineKeyboardButton('No', callback_data='no_qr_dryer')
         ]
        ]
        markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(text = "Timer for QR DRYER will begin?", reply_markup=markup)
        return MENU
    
def double_confirm_qr_washer_callback(update: Update, _: CallbackContext) -> int:
        query = update.callback_query
        query.answer()
        keyboard = [
        [InlineKeyboardButton('Yes', callback_data='yes_qr_washer'),
        ],
        [InlineKeyboardButton('No', callback_data='no_qr_washer')
         ]
        ]
        markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(text = "Timer for QR WASHER will begin?", reply_markup=markup)
        return MENU
    
def double_confirm_coin_dryer_callback(update: Update, _: CallbackContext) -> int:
        query = update.callback_query
        query.answer()
        keyboard = [
        [InlineKeyboardButton('Yes', callback_data='yes_coin_dryer'),
        ],
        [InlineKeyboardButton('No', callback_data='no_coin_dryer')
         ]
        ]
        markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(text = "Timer for COIN DRYER will begin?", reply_markup=markup)
        return MENU

def double_confirm_coin_washer_callback(update: Update, _: CallbackContext) -> int:
        query = update.callback_query
        query.answer()
        keyboard = [
        [InlineKeyboardButton('Yes', callback_data='yes_coin_washer'),
        ],
        [InlineKeyboardButton('No', callback_data='no_coin_washer')
         ]
        ]
        markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(text = "Timer for COIN WASHER will begin?", reply_markup=markup)
        return MENU

def set_timer_qr_dryer(update: Update, context: CallbackContext) -> None:
    """Add a job to the queue."""
    chat_id = update.effective_message.chat_id
    query = update.callback_query
    query.answer()
    
    washerdue = int(1800)
    dryerdue = int(2400)

    job_removed = remove_job_if_exists(str(chat_id), context)
    global QR_DRYER
    if QR_DRYER == 'UNAVAILABLE':
        text = "QR DRYER is currently in use. Please come back again later!"
        query.message.delete()
        Tbot.send_message(chat_id = chat_id, text = text)
    if QR_DRYER == 'AVAILABLE':
        QRDRYER = context.job_queue.run_once(qr_dryer_alarm, dryerdue, context=chat_id, name='qr_dryer')
        QRDRYER
        QR_DRYER = 'UNAVAILABLE'
##        QR_DRYER_TIME = context.args.index(context.args[-1])
        global QR_DRYER_JOB_INDEX
        global QR_DRYER_LAST_USED
        global JOB
        JOB[QR_DRYER_JOB_INDEX] = datetime.datetime.now()
        QR_DRYER_LAST_USED = update.effective_message.chat.username
        text = "Timer Set for 40mins for QR DRYER. Please come back again!"
    #if job_removed:
    #    text = 'Status Update: QR DRYER is available'
        query.message.delete()
        Tbot.send_message(chat_id = chat_id, text = text)
    return MENU

def set_timer_qr_washer(update: Update, context: CallbackContext) -> None:
    """Add a job to the queue."""
    chat_id = update.effective_message.chat_id
    query = update.callback_query
    query.answer()
    
    washerdue = int(1800)
    dryerdue = int(2400)

    job_removed = remove_job_if_exists(str(chat_id), context)
    global QR_WASHER
    if QR_WASHER == 'UNAVAILABLE':
        text = "QR WASHER is currently in use. Please come back again later!"
        query.message.delete()
        Tbot.send_message(chat_id = chat_id, text = text)
    if QR_WASHER == 'AVAILABLE':
        QRWASHER = context.job_queue.run_once(qr_washer_alarm, washerdue, context=chat_id, name='qr_washer')
        QRWASHER
        global QR_WASHER_JOB_INDEX
        global JOB
        global QR_WASHER_LAST_USED 
        JOB[QR_WASHER_JOB_INDEX] = datetime.datetime.now()
        QR_WASHER_LAST_USED = update.effective_message.chat.username
        QR_WASHER = 'UNAVAILABLE'
        text = "Timer Set for 30mins for QR WASHER. Please come back again!"
    #if job_removed:
    #    text = 'Status Update: QR DRYER is available'
        query.message.delete()
        Tbot.send_message(chat_id = chat_id, text = text)
    return MENU

def set_timer_coin_dryer(update: Update, context: CallbackContext) -> None:
    """Add a job to the queue."""
    chat_id = update.effective_message.chat_id
    query = update.callback_query
    query.answer()
    
    washerdue = int(1800)
    dryerdue = int(2400)

    job_removed = remove_job_if_exists(str(chat_id), context)
    global COIN_DRYER
    if COIN_DRYER == 'UNAVAILABLE':
        text = "COIN DRYER is currently in use. Please come back again later!"
        query.message.delete()
        Tbot.send_message(chat_id = chat_id, text = text)
    if COIN_DRYER == 'AVAILABLE':
        COINDRYER = context.job_queue.run_once(coin_dryer_alarm, dryerdue, context=chat_id, name='coin_dryer')
        COINDRYER
        global COIN_DRYER_JOB_INDEX
        global JOB
        global COIN_DRYER_LAST_USED
        JOB[COIN_DRYER_JOB_INDEX] = datetime.datetime.now()
        COIN_DRYER_LAST_USED = update.effective_message.chat.username
        COIN_DRYER = 'UNAVAILABLE'
        text = "Timer Set for 40mins for COIN DRYER. Please come back again!"
    #if job_removed:
    #    text = 'Status Update: QR DRYER is available'
        query.message.delete()
        Tbot.send_message(chat_id = chat_id, text = text)
    return MENU

def set_timer_coin_washer(update: Update, context: CallbackContext) -> None:
    """Add a job to the queue."""
    chat_id = update.effective_message.chat_id #use .effective_message to receive a message or edited message. .message only receives message
    query = update.callback_query
    query.answer()
    
    washerdue = int(1800)
    dryerdue = int(2400)

    job_removed = remove_job_if_exists(str(chat_id), context)
    global COIN_WASHER  
    if COIN_WASHER == 'UNAVAILABLE':
        text = "COIN WASHER is currently in use. Please come back again later!"
        query.message.delete()
        Tbot.send_message(chat_id = chat_id, text = text)
    if COIN_WASHER == 'AVAILABLE':
        COINWASHER = context.job_queue.run_once(coin_washer_alarm, washerdue, context=chat_id, name='coin_washer')
        COINWASHER
        global COIN_WASHER_JOB_INDEX
        global JOB
        global COIN_WASHER_LAST_USED
        JOB[COIN_WASHER_JOB_INDEX] = datetime.datetime.now()
        COIN_WASHER = 'UNAVAILABLE'
        COIN_WASHER_LAST_USED = update.effective_message.chat.username
        text = "Timer Set for 30mins for COIN WASHER. Please come back again!"
    #if job_removed:
    #    text = 'Status Update: QR DRYER is available'
        query.message.delete()
        Tbot.send_message(chat_id = chat_id, text = text)
    return MENU

def main() -> None:
    """Run bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN)# Fill in Token

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Use the pattern parameter to pass CallbackQueries with specific
    # data pattern to the corresponding handlers.
    # ^ means "start of line/string"
    # $ means "end of line/string"
    # So ^ABC$ will only allow 'ABC'
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start),
                    CommandHandler("select", select),
                      CommandHandler("status", status)],
        states={
            MENU: [
                CallbackQueryHandler(cancel, pattern='^' + 'exit' + '$'),
                CallbackQueryHandler(cancel, pattern='^' + 'exits' + '$'),
                
                CallbackQueryHandler(double_confirm_qr_dryer_callback, pattern='^' + 'qr_dryer' + '$'), #whhich callback_data does start get call
                CallbackQueryHandler(double_confirm_qr_washer_callback, pattern='^' + 'qr_washer' + '$'),
                CallbackQueryHandler(double_confirm_coin_dryer_callback, pattern='^' + 'coin_dryer' + '$'),
                CallbackQueryHandler(double_confirm_coin_washer_callback, pattern='^' + 'coin_washer' + '$'),

                CallbackQueryHandler(backtomenu, pattern='^' + 'no_qr_dryer' + '$'),
                CallbackQueryHandler(backtomenu, pattern='^' + 'no_qr_washer' + '$'),
                CallbackQueryHandler(backtomenu, pattern='^' + 'no_coin_dryer' + '$'),
                CallbackQueryHandler(backtomenu, pattern='^' + 'no_coin_washer' + '$'),

                CallbackQueryHandler(set_timer_qr_dryer, pattern='^' + 'yes_qr_dryer' + '$'),
                CallbackQueryHandler(set_timer_qr_washer, pattern='^' + 'yes_qr_washer' + '$'),
                CallbackQueryHandler(set_timer_coin_dryer, pattern='^' + 'yes_coin_dryer' + '$'),
                CallbackQueryHandler(set_timer_coin_washer, pattern='^' + 'yes_coin_washer' + '$'),
            ]
            
        },
        fallbacks=[CommandHandler('start', start),
                   CommandHandler("select", select),
                   CommandHandler("status", status)],
    )

    # Add ConversationHandler to dispatcher that will be used for handling updates
    dispatcher.add_handler(conv_handler)

    # Port is given by Heroku
    PORT = os.environ.get('PORT', 5000)

    # Start the Bot
    #updater.start_polling()
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN,
                          webhook_url=f"https://{NAME}.herokuapp.com/{TOKEN}")

    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    updater.idle()

##        except (IndexError, ValueError):
##        update.message.reply_text('Oh no, this is not one of the commands I recognise, use /start to check out the list')


if __name__ == '__main__':
    main()
