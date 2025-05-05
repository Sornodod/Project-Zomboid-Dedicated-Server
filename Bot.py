import logging
import subprocess
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, CallbackContext

API_TOKEN = "" # Токен от телеграм бота
SERVICE_NAME = "pzserver.service" # Имя службы сервера
ADMIN_CHAT_ID =  # Чат куда будет писать бот о пользовании ботом.


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

def main_menu_keyboard():
    return InlineKeyboardMarkup([ 
        [
            InlineKeyboardButton("Включить", callback_data='start'),
            InlineKeyboardButton("Выключить", callback_data='stop'),
        ],
        [
            InlineKeyboardButton("Перезагрузить", callback_data='restart'),
            InlineKeyboardButton("Статус сервера", callback_data='status'),
        ]
    ])

def back_button_keyboard():
    return InlineKeyboardMarkup([ 
        [InlineKeyboardButton("🔙 Назад", callback_data='back')]
    ])

async def start(update: Update, context: CallbackContext):
    """Стартовое меню"""
    await update.message.reply_text('Бот для управления сервером', reply_markup=main_menu_keyboard())

async def control_server(action: str):
    """Управление systemctl"""
    try:
        subprocess.run(f"sudo systemctl {action} {SERVICE_NAME}", shell=True, check=True)
        return {
            "start": "Сервер PZ запущен.",
            "stop": "Сервер остановлен.",
            "restart": "Сервер перезагружен."
        }.get(action, "Действие выполнено.")
    except subprocess.CalledProcessError:
        return f"Ошибка при выполнении команды {action}."

async def status_server():
    """Статус службы"""
    try:
        result = subprocess.run(f"systemctl is-active {SERVICE_NAME}", shell=True, check=True, stdout=subprocess.PIPE)
        status = result.stdout.decode('utf-8').strip()
        return "🟢 Сервер PZ активен." if status == "active" else f"Сервер {status}."
    except subprocess.CalledProcessError:
        return "🔴 Сервер PZ не активен."

async def notify_admin(user, action, context):
    """Уведомление администратора"""
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    message = (
        f"#Лог_PZServer\n"
        f"👤 Пользователь: {user.full_name} (ID: {user.id})\n"
        f"🔘 Действие: {action}\n"
        f"🕒 Время: {now}"
    )
    await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=message)

async def button(update: Update, context: CallbackContext):
    """Обработка кнопок"""
    query = update.callback_query
    action = query.data
    user = query.from_user

    
    if action != 'back':
        await notify_admin(user, action, context)

    if action == 'start':
        response = await control_server("start")
        markup = back_button_keyboard()
    elif action == 'stop':
        response = await control_server("stop")
        markup = back_button_keyboard()
    elif action == 'restart':
        response = await control_server("restart")
        markup = back_button_keyboard()
    elif action == 'status':
        response = await status_server()
        markup = back_button_keyboard()
    elif action == 'back':
        response = "Вы вернулись в главное меню:"
        markup = main_menu_keyboard()
    else:
        response = "Неизвестная команда"
        markup = main_menu_keyboard()

    await query.answer()
    await query.edit_message_text(text=response, reply_markup=markup)

async def main():
    """Запуск бота"""
    application = Application.builder().token(API_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))

    await application.run_polling()

if __name__ == '__main__':
    
    application = Application.builder().token(API_TOKEN).build()

    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))

    
    application.run_polling()
