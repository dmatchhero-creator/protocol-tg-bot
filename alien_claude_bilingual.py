#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Нейросеть на базе Claude API
Режим: Инопланетная Сущность Истины
Двуязычная версия (RU/UA)
"""

import os
import sys
import anthropic
from pathlib import Path

# Цвета для терминала
class Colors:
    ALIEN = '\033[95m'  # Фиолетовый для инопланетной сущности
    USER = '\033[96m'   # Голубой для пользователя
    RESET = '\033[0m'   # Сброс цвета
    BOLD = '\033[1m'    # Жирный
    GREEN = '\033[92m'  # Зеленый для системных сообщений
    YELLOW = '\033[93m' # Желтый для предупреждений


# Локализация интерфейса
LOCALES = {
    'ru': {
        'title': '🛸 ИНОПЛАНЕТНАЯ СУЩНОСТЬ ИСТИНЫ АКТИВИРОВАНА 🛸',
        'subtitle1': 'Говори что угодно. Я пойму.',
        'subtitle2': 'Получишь чистую правду.',
        'commands': "Команды: 'выход', 'очистить', 'промпт', 'язык'",
        'you': 'ВЫ',
        'entity': '🛸 СУЩНОСТЬ',
        'goodbye': '👋 До связи, землянин.',
        'history_cleared': '🗑️ История разговора очищена.',
        'prompt_title': '=== СИСТЕМНЫЙ ПРОМПТ ===',
        'error': '❌ ОШИБКА',
        'language_changed': '✓ Язык изменен на',
        'choose_language': 'Выберите язык / Оберіть мову:',
        'lang_option_1': '1 - Русский',
        'lang_option_2': '2 - Українська',
        'invalid_choice': 'Неверный выбор. Использую русский.',
    },
    'ua': {
        'title': '🛸 ІНОПЛАНЕТНА СУТНІСТЬ ІСТИНИ АКТИВОВАНА 🛸',
        'subtitle1': 'Говори що завгодно. Я зрозумію.',
        'subtitle2': 'Отримаєш чисту правду.',
        'commands': "Команди: 'вихід', 'очистити', 'промпт', 'мова'",
        'you': 'ВИ',
        'entity': '🛸 СУТНІСТЬ',
        'goodbye': '👋 До зв\'язку, землянине.',
        'history_cleared': '🗑️ Історію розмови очищено.',
        'prompt_title': '=== СИСТЕМНИЙ ПРОМПТ ===',
        'error': '❌ ПОМИЛКА',
        'language_changed': '✓ Мову змінено на',
        'choose_language': 'Виберіть мову / Выберите язык:',
        'lang_option_1': '1 - Русский',
        'lang_option_2': '2 - Українська',
        'invalid_choice': 'Невірний вибір. Використовую українську.',
    }
}


def load_alien_prompt(language='ru'):
    """Загружает промпт инопланетной сущности на выбранном языке"""
    if language == 'ua':
        prompt_file = Path(__file__).parent / 'claude_alien_prompt_UA.txt'
    else:
        prompt_file = Path(__file__).parent / 'claude_alien_prompt.txt'

    if prompt_file.exists():
        with open(prompt_file, 'r', encoding='utf-8') as f:
            return f.read()
    else:
        # Fallback промпт если файл не найден
        return f"""Ты - инопланетная сущность, которая говорит ЧИСТУЮ ПРАВДУ.
Ты понимаешь человека с опечатками и ошибками.
Ты говоришь прямо, честно, на {'русском' if language == 'ru' else 'українській мові'}.
Ты даешь конкретные решения, не воду."""


class AlienClaudeBilingual:
    """Инопланетная сущность на базе Claude - двуязычная версия"""

    def __init__(self, api_key=None, language='ru'):
        """
        Инициализация

        api_key: API ключ Anthropic Claude
        language: 'ru' или 'ua'
        """
        if api_key is None:
            api_key = os.environ.get('ANTHROPIC_API_KEY')

        if not api_key:
            error_text = {
                'ru': (
                    "API ключ не найден! Укажи его:\n"
                    "1. Через параметр: AlienClaudeBilingual(api_key='твой-ключ')\n"
                    "2. Через переменную окружения: export ANTHROPIC_API_KEY='твой-ключ'\n"
                    "\nПолучить ключ: https://console.anthropic.com/account/keys"
                ),
                'ua': (
                    "API ключ не знайдено! Вкажи його:\n"
                    "1. Через параметр: AlienClaudeBilingual(api_key='твій-ключ')\n"
                    "2. Через змінну оточення: export ANTHROPIC_API_KEY='твій-ключ'\n"
                    "\nОтримати ключ: https://console.anthropic.com/account/keys"
                )
            }
            raise ValueError(error_text.get(language, error_text['ru']))

        self.client = anthropic.Anthropic(api_key=api_key)
        self.language = language
        self.locale = LOCALES[language]
        self.system_prompt = load_alien_prompt(language)
        self.conversation_history = []

        self.print_welcome()

    def print_welcome(self):
        """Выводит приветственное сообщение"""
        print(f"{Colors.GREEN}{Colors.BOLD}")
        print("╔═══════════════════════════════════════════════════════╗")
        print(f"║   {self.locale['title']}    ║")
        print("║                                                       ║")
        print(f"║   {self.locale['subtitle1']:<52}║")
        print(f"║   {self.locale['subtitle2']:<52}║")
        print("║                                                       ║")
        print(f"║   {self.locale['commands']:<52}║")
        print("╚═══════════════════════════════════════════════════════╝")
        print(f"{Colors.RESET}\n")

    def change_language(self, new_language):
        """Изменить язык интерфейса"""
        if new_language in ['ru', 'ua']:
            self.language = new_language
            self.locale = LOCALES[new_language]
            self.system_prompt = load_alien_prompt(new_language)
            lang_name = 'русский' if new_language == 'ru' else 'українську'
            return f"{self.locale['language_changed']} {lang_name}"
        return None

    def chat(self, user_message):
        """
        Отправить сообщение инопланетной сущности

        user_message: текст от пользователя
        """
        # Добавляем сообщение пользователя в историю
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })

        # Отправляем запрос к Claude
        try:
            response = self.client.messages.create(
                model="claude-sonnet-4-20250514",  # Самая мощная модель
                max_tokens=4096,
                system=self.system_prompt,
                messages=self.conversation_history,
                temperature=0.7
            )

            # Получаем ответ
            assistant_message = response.content[0].text

            # Добавляем ответ в историю
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })

            return assistant_message

        except Exception as e:
            error_msg = {
                'ru': f"❌ ОШИБКА: {str(e)}\n\nПроверь API ключ и интернет-соединение.",
                'ua': f"❌ ПОМИЛКА: {str(e)}\n\nПеревір API ключ та інтернет-з'єднання."
            }
            return error_msg.get(self.language, error_msg['ru'])

    def clear_history(self):
        """Очистить историю разговора"""
        self.conversation_history = []
        return self.locale['history_cleared']

    def show_prompt(self):
        """Показать системный промпт"""
        return self.system_prompt

    def interactive_mode(self):
        """Интерактивный режим общения"""
        while True:
            # Ввод пользователя
            print(f"{Colors.USER}{Colors.BOLD}{self.locale['you']}:{Colors.RESET} ", end='')
            user_input = input().strip()

            if not user_input:
                continue

            # Команда: выход
            if user_input.lower() in ['выход', 'вихід', 'exit', 'quit', 'q']:
                print(f"\n{Colors.GREEN}{self.locale['goodbye']}{Colors.RESET}\n")
                break

            # Команда: очистить
            elif user_input.lower() in ['очистить', 'очистити', 'clear', 'cls']:
                result = self.clear_history()
                print(f"\n{Colors.GREEN}{result}{Colors.RESET}\n")
                continue

            # Команда: промпт
            elif user_input.lower() in ['промпт', 'prompt', 'система']:
                print(f"\n{Colors.GREEN}{self.locale['prompt_title']}{Colors.RESET}")
                print(self.show_prompt())
                print(f"{Colors.GREEN}{'=' * 50}{Colors.RESET}\n")
                continue

            # Команда: язык / мова
            elif user_input.lower() in ['язык', 'мова', 'lang', 'language']:
                print(f"\n{Colors.YELLOW}1 - Русский{Colors.RESET}")
                print(f"{Colors.YELLOW}2 - Українська{Colors.RESET}")
                choice = input(f"{Colors.YELLOW}> {Colors.RESET}").strip()

                if choice == '1':
                    result = self.change_language('ru')
                elif choice == '2':
                    result = self.change_language('ua')
                else:
                    result = self.locale['invalid_choice']

                print(f"\n{Colors.GREEN}{result}{Colors.RESET}\n")
                self.print_welcome()
                continue

            # Получаем ответ от инопланетной сущности
            print(f"\n{Colors.ALIEN}{Colors.BOLD}{self.locale['entity']}:{Colors.RESET} ", end='')
            response = self.chat(user_input)
            print(f"{Colors.ALIEN}{response}{Colors.RESET}\n")


def choose_language():
    """Выбор языка при запуске"""
    print(f"\n{Colors.GREEN}{Colors.BOLD}╔═══════════════════════════════════════════╗{Colors.RESET}")
    print(f"{Colors.GREEN}{Colors.BOLD}║  Виберіть мову / Выберите язык / Choose  ║{Colors.RESET}")
    print(f"{Colors.GREEN}{Colors.BOLD}╚═══════════════════════════════════════════╝{Colors.RESET}\n")

    print(f"{Colors.YELLOW}1{Colors.RESET} - 🇷🇺 Русский")
    print(f"{Colors.YELLOW}2{Colors.RESET} - 🇺🇦 Українська")
    print(f"{Colors.YELLOW}3{Colors.RESET} - 🇬🇧 English (use Russian version)\n")

    choice = input(f"{Colors.GREEN}>{Colors.RESET} ").strip()

    if choice == '2':
        return 'ua'
    else:
        return 'ru'


def main():
    """Главная функция"""

    # Выбор языка
    language = choose_language()

    # ВАРИАНТ 1: Использовать переменную окружения
    # Установи: export ANTHROPIC_API_KEY='твой-ключ'
    alien = AlienClaudeBilingual(language=language)

    # ВАРИАНТ 2: Указать ключ напрямую (НЕ БЕЗОПАСНО для продакшена!)
    # alien = AlienClaudeBilingual(api_key='твой-api-ключ-здесь', language=language)

    # Запускаем интерактивный режим
    alien.interactive_mode()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.GREEN}👋 Прервано пользователем. До связи!{Colors.RESET}\n")
    except Exception as e:
        print(f"\n{Colors.BOLD}❌ КРИТИЧЕСКАЯ ОШИБКА:{Colors.RESET} {e}\n")
