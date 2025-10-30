#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Telegram-бот для воронки Протокол-Т
Двойная проверка клиентов перед выдачей личного контакта
"""

import logging
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
    ConversationHandler,
)

# Импорт модулей детекции кризисов
from crisis_detector import detect_crisis_in_message, CrisisType
from crisis_responses import get_crisis_response

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ВАЖНО: Замени на свой токен от BotFather
BOT_TOKEN = "8223809188:AAG3Q8BndfMZ_s9MmTjEodkC9ePo3J16BYI"

# ВАЖНО: Замени на свой личный Telegram username
YOUR_PERSONAL_CONTACT = "@VladimirHypno"

# Состояния для разговора
PROBLEM_DETAIL, POINT_B, READINESS = range(3)

# Хранилище данных пользователей (в продакшене используй БД)
user_data_storage = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Начало диалога после заполнения формы на сайте"""
    
    user = update.effective_user
    user_id = user.id
    
    # Инициализируем данные пользователя
    if user_id not in user_data_storage:
        user_data_storage[user_id] = {}
    
    welcome_text = (
        f"Здравствуйте, {user.first_name}! 👋\n\n"
        f"Вы оставили заявку на protocol-t.ru.\n\n"
        f"Для подтверждения серьёзности намерений и точной диагностики "
        f"ответьте на несколько вопросов.\n\n"
        f"Это займёт 2-3 минуты. После ответов получите контакт специалиста.\n\n"
        f"━━━━━━━━━━━━━━━━\n\n"
        f"<b>Вопрос 1 из 3:</b>\n\n"
        f"Опишите вашу проблему подробнее.\n\n"
        f"Что именно мешает? Какие симптомы ощущаете?\n"
        f"(Например: тревога перед созвонами, прокрастинация, страх оценки)"
    )
    
    await update.message.reply_text(
        welcome_text,
        parse_mode='HTML'
    )
    
    return PROBLEM_DETAIL


async def problem_detail(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработка подробного описания проблемы"""

    user_id = update.effective_user.id
    problem_text = update.message.text

    # ПРОВЕРКА НА КРИЗИСНУЮ СИТУАЦИЮ
    crisis_type, confidence = detect_crisis_in_message(problem_text)

    if crisis_type != CrisisType.NONE and confidence >= 0.5:
        # Обнаружен кризис - отправляем экстренный ответ
        crisis_response = get_crisis_response(crisis_type, confidence)
        await update.message.reply_text(
            crisis_response,
            parse_mode='HTML'
        )

        # Логируем кризисную ситуацию
        logger.warning(
            f"CRISIS DETECTED - User {user_id}: {crisis_type.value} "
            f"(confidence: {confidence:.2f})"
        )

        # Уведомляем специалиста
        YOUR_TELEGRAM_ID = 123456789  # Замени на свой
        try:
            await context.bot.send_message(
                chat_id=YOUR_TELEGRAM_ID,
                text=f"🚨 <b>КРИЗИС ОБНАРУЖЕН</b>\n\n"
                     f"User: {update.effective_user.first_name} (@{update.effective_user.username})\n"
                     f"ID: {user_id}\n"
                     f"Тип: {crisis_type.value}\n"
                     f"Уверенность: {confidence:.0%}\n\n"
                     f"Сообщение:\n{problem_text}",
                parse_mode='HTML'
            )
        except Exception as e:
            logger.error(f"Ошибка отправки кризисного уведомления: {e}")

        # Завершаем диалог - человеку нужна срочная помощь
        return ConversationHandler.END

    # Сохраняем ответ
    user_data_storage[user_id]['problem_detail'] = problem_text
    
    # Переходим к следующему вопросу
    question_2 = (
        f"Принял. Вижу проблему.\n\n"
        f"━━━━━━━━━━━━━━━━\n\n"
        f"<b>Вопрос 2 из 3:</b>\n\n"
        f"Опишите вашу точку Б максимально детально.\n\n"
        f"Где хотите оказаться через 2-3 месяца?\n"
        f"Что будет по-другому в вашей жизни?\n\n"
        f"(Например: спокойно веду созвоны, зарабатываю 200к, есть девушка, "
        f"уверенность внутри)"
    )
    
    await update.message.reply_text(
        question_2,
        parse_mode='HTML'
    )
    
    return POINT_B


async def point_b(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработка описания точки Б"""

    user_id = update.effective_user.id
    point_b_text = update.message.text

    # ПРОВЕРКА НА КРИЗИСНУЮ СИТУАЦИЮ
    crisis_type, confidence = detect_crisis_in_message(point_b_text)

    if crisis_type != CrisisType.NONE and confidence >= 0.5:
        # Обнаружен кризис - отправляем экстренный ответ
        crisis_response = get_crisis_response(crisis_type, confidence)
        await update.message.reply_text(
            crisis_response,
            parse_mode='HTML'
        )

        logger.warning(
            f"CRISIS DETECTED - User {user_id}: {crisis_type.value} "
            f"(confidence: {confidence:.2f})"
        )

        # Уведомляем специалиста
        YOUR_TELEGRAM_ID = 123456789  # Замени на свой
        try:
            await context.bot.send_message(
                chat_id=YOUR_TELEGRAM_ID,
                text=f"🚨 <b>КРИЗИС ОБНАРУЖЕН</b>\n\n"
                     f"User: {update.effective_user.first_name} (@{update.effective_user.username})\n"
                     f"ID: {user_id}\n"
                     f"Тип: {crisis_type.value}\n"
                     f"Уверенность: {confidence:.0%}\n\n"
                     f"Сообщение:\n{point_b_text}",
                parse_mode='HTML'
            )
        except Exception as e:
            logger.error(f"Ошибка отправки кризисного уведомления: {e}")

        return ConversationHandler.END

    # Сохраняем ответ
    user_data_storage[user_id]['point_b'] = point_b_text
    
    # Переходим к последнему вопросу
    question_3 = (
        f"Отлично. Вижу цель.\n\n"
        f"━━━━━━━━━━━━━━━━\n\n"
        f"<b>Вопрос 3 из 3:</b>\n\n"
        f"Готовы ли вы работать глубоко с подсознанием?\n\n"
        f"Это не лёгкий путь. Придётся:\n"
        f"• Погружаться в детские травмы\n"
        f"• Выражать застрявшие эмоции физически (крик, движение)\n"
        f"• Честно смотреть на себя\n"
        f"• Делать домашние задания между сеансами\n\n"
        f"Это работает. Но требует вашего участия на 100%.\n\n"
        f"Ответьте: готовы или нет? (напишите своими словами)"
    )
    
    await update.message.reply_text(
        question_3,
        parse_mode='HTML'
    )
    
    return READINESS


async def readiness(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработка готовности и выдача контакта"""

    user_id = update.effective_user.id
    user = update.effective_user
    readiness_text = update.message.text.lower()

    # ПРОВЕРКА НА КРИЗИСНУЮ СИТУАЦИЮ
    crisis_type, confidence = detect_crisis_in_message(update.message.text)

    if crisis_type != CrisisType.NONE and confidence >= 0.5:
        # Обнаружен кризис - отправляем экстренный ответ
        crisis_response = get_crisis_response(crisis_type, confidence)
        await update.message.reply_text(
            crisis_response,
            parse_mode='HTML'
        )

        logger.warning(
            f"CRISIS DETECTED - User {user_id}: {crisis_type.value} "
            f"(confidence: {confidence:.2f})"
        )

        # Уведомляем специалиста
        YOUR_TELEGRAM_ID = 123456789  # Замени на свой
        try:
            await context.bot.send_message(
                chat_id=YOUR_TELEGRAM_ID,
                text=f"🚨 <b>КРИЗИС ОБНАРУЖЕН</b>\n\n"
                     f"User: {user.first_name} (@{user.username})\n"
                     f"ID: {user_id}\n"
                     f"Тип: {crisis_type.value}\n"
                     f"Уверенность: {confidence:.0%}\n\n"
                     f"Сообщение:\n{update.message.text}",
                parse_mode='HTML'
            )
        except Exception as e:
            logger.error(f"Ошибка отправки кризисного уведомления: {e}")

        return ConversationHandler.END

    # Сохраняем ответ
    user_data_storage[user_id]['readiness'] = update.message.text
    
    # Анализируем готовность (простая проверка)
    if any(word in readiness_text for word in ['да', 'готов', 'готова', 'конечно', 'yes']):
        # Положительный ответ - выдаём контакт
        final_message = (
            f"✅ <b>Заявка подтверждена</b>\n\n"
            f"Спасибо за честные ответы. Вижу серьёзность намерений.\n\n"
            f"━━━━━━━━━━━━━━━━\n\n"
            f"<b>Следующий шаг:</b>\n\n"
            f"Напишите специалисту: {YOUR_PERSONAL_CONTACT}\n\n"
            f"В сообщении укажите:\n"
            f"1. Ваше имя: {user.first_name}\n"
            f"2. Что прошли бота и готовы к диагностике\n\n"
            f"━━━━━━━━━━━━━━━━\n\n"
            f"<b>Условия:</b>\n\n"
            f"Первый шаг — диагностика 1000₽\n"
            f"На созвоне определим сможем ли работать вместе.\n\n"
            f"Если да — протокол трансформации 100 000₽\n"
            f"4 сеанса + сопровождение до результата.\n\n"
            f"Гарантия: если не помогло — возврат 50%.\n\n"
            f"━━━━━━━━━━━━━━━━\n\n"
            f"До встречи в диалоге со специалистом.\n"
            f"Вы на верном пути. 🎯"
        )
        
        # Отправляем уведомление тебе (специалисту)
        # ВАЖНО: замени YOUR_TELEGRAM_ID на свой числовой ID
        # Узнать свой ID можно через @userinfobot
        YOUR_TELEGRAM_ID = 123456789  # Замени на свой
        
        notification = (
            f"🔔 <b>НОВАЯ ЗАЯВКА</b>\n\n"
            f"<b>Пользователь:</b> {user.first_name} {user.last_name or ''}\n"
            f"<b>Username:</b> @{user.username or 'не указан'}\n"
            f"<b>User ID:</b> {user_id}\n\n"
            f"━━━━━━━━━━━━━━━━\n\n"
            f"<b>Проблема:</b>\n{user_data_storage[user_id]['problem_detail']}\n\n"
            f"<b>Точка Б:</b>\n{user_data_storage[user_id]['point_b']}\n\n"
            f"<b>Готовность:</b>\n{user_data_storage[user_id]['readiness']}\n\n"
            f"━━━━━━━━━━━━━━━━\n\n"
            f"Человек получил твой контакт и сейчас напишет."
        )
        
        try:
            await context.bot.send_message(
                chat_id=YOUR_TELEGRAM_ID,
                text=notification,
                parse_mode='HTML'
            )
        except Exception as e:
            logger.error(f"Ошибка отправки уведомления: {e}")
        
    else:
        # Сомнения в готовности
        final_message = (
            f"Понял ваши сомнения.\n\n"
            f"Работа с подсознанием — это серьёзный шаг.\n"
            f"Важно быть готовым.\n\n"
            f"Если решитесь — напишите /start заново,\n"
            f"я проведу вас через вопросы снова.\n\n"
            f"Или можете сразу написать специалисту:\n"
            f"{YOUR_PERSONAL_CONTACT}\n\n"
            f"Он ответит на все вопросы и развеет сомнения.\n\n"
            f"Удачи на пути! 🙏"
        )
    
    await update.message.reply_text(
        final_message,
        parse_mode='HTML'
    )
    
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Отмена диалога"""
    
    await update.message.reply_text(
        'Диалог отменён. Если передумаете — напишите /start',
        reply_markup=ReplyKeyboardRemove()
    )
    
    return ConversationHandler.END


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Команда помощи"""
    
    help_text = (
        f"<b>Бот Протокол-Т</b>\n\n"
        f"Я помогаю отфильтровать серьёзных клиентов "
        f"перед выдачей контакта специалиста.\n\n"
        f"<b>Команды:</b>\n"
        f"/start - Начать диалог\n"
        f"/cancel - Отменить диалог\n"
        f"/help - Эта справка\n\n"
        f"После ответов на 3 вопроса получите контакт специалиста."
    )
    
    await update.message.reply_text(help_text, parse_mode='HTML')


def main() -> None:
    """Запуск бота"""
    
    # Создаём приложение
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Настраиваем диалог
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            PROBLEM_DETAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, problem_detail)],
            POINT_B: [MessageHandler(filters.TEXT & ~filters.COMMAND, point_b)],
            READINESS: [MessageHandler(filters.TEXT & ~filters.COMMAND, readiness)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    
    # Добавляем обработчики
    application.add_handler(conv_handler)
    application.add_handler(CommandHandler("help", help_command))
    
    # Запускаем бота
    logger.info("Бот запущен...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
