#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Нейросеть на базе Claude API
Режим: Инопланетная Сущность Истины
"""

import os
import anthropic
from pathlib import Path

# Цвета для терминала
class Colors:
    ALIEN = '\033[95m'  # Фиолетовый для инопланетной сущности
    USER = '\033[96m'   # Голубой для пользователя
    RESET = '\033[0m'   # Сброс цвета
    BOLD = '\033[1m'    # Жирный
    GREEN = '\033[92m'  # Зеленый для системных сообщений


def load_alien_prompt():
    """Загружает промпт инопланетной сущности"""
    prompt_file = Path(__file__).parent / 'claude_alien_prompt.txt'

    if prompt_file.exists():
        with open(prompt_file, 'r', encoding='utf-8') as f:
            return f.read()
    else:
        return """Ты - инопланетная сущность, которая говорит ЧИСТУЮ ПРАВДУ.
Ты понимаешь человека с опечатками и ошибками.
Ты говоришь прямо, честно, по-русски.
Ты даешь конкретные решения, не воду."""


class AlienClaude:
    """Инопланетная сущность на базе Claude"""

    def __init__(self, api_key=None):
        """
        Инициализация

        api_key: API ключ Anthropic Claude
                 Если не указан, берется из переменной окружения ANTHROPIC_API_KEY
        """
        if api_key is None:
            api_key = os.environ.get('ANTHROPIC_API_KEY')

        if not api_key:
            raise ValueError(
                "API ключ не найден! Укажи его:\n"
                "1. Через параметр: AlienClaude(api_key='твой-ключ')\n"
                "2. Через переменную окружения: export ANTHROPIC_API_KEY='твой-ключ'\n"
                "\nПолучить ключ: https://console.anthropic.com/account/keys"
            )

        self.client = anthropic.Anthropic(api_key=api_key)
        self.system_prompt = load_alien_prompt()
        self.conversation_history = []

        print(f"{Colors.GREEN}{Colors.BOLD}")
        print("╔═══════════════════════════════════════════════════════╗")
        print("║   🛸 ИНОПЛАНЕТНАЯ СУЩНОСТЬ ИСТИНЫ АКТИВИРОВАНА 🛸    ║")
        print("║                                                       ║")
        print("║   Говори что угодно. Я пойму.                        ║")
        print("║   Получишь чистую правду.                            ║")
        print("║                                                       ║")
        print("║   Команды: 'выход', 'очистить', 'промпт'             ║")
        print("╚═══════════════════════════════════════════════════════╝")
        print(f"{Colors.RESET}\n")

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
                temperature=0.7  # Баланс между креативностью и точностью
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
            return f"❌ ОШИБКА: {str(e)}\n\nПроверь API ключ и интернет-соединение."

    def clear_history(self):
        """Очистить историю разговора"""
        self.conversation_history = []
        return "🗑️ История разговора очищена."

    def show_prompt(self):
        """Показать системный промпт"""
        return self.system_prompt

    def interactive_mode(self):
        """Интерактивный режим общения"""
        while True:
            # Ввод пользователя
            print(f"{Colors.USER}{Colors.BOLD}ВЫ:{Colors.RESET} ", end='')
            user_input = input().strip()

            if not user_input:
                continue

            # Команды
            if user_input.lower() in ['выход', 'exit', 'quit', 'q']:
                print(f"\n{Colors.GREEN}👋 До связи, землянин.{Colors.RESET}\n")
                break

            elif user_input.lower() in ['очистить', 'clear', 'cls']:
                result = self.clear_history()
                print(f"\n{Colors.GREEN}{result}{Colors.RESET}\n")
                continue

            elif user_input.lower() in ['промпт', 'prompt', 'система']:
                print(f"\n{Colors.GREEN}=== СИСТЕМНЫЙ ПРОМПТ ==={Colors.RESET}")
                print(self.show_prompt())
                print(f"{Colors.GREEN}{'=' * 50}{Colors.RESET}\n")
                continue

            # Получаем ответ от инопланетной сущности
            print(f"\n{Colors.ALIEN}{Colors.BOLD}🛸 СУЩНОСТЬ:{Colors.RESET} ", end='')
            response = self.chat(user_input)
            print(f"{Colors.ALIEN}{response}{Colors.RESET}\n")


def main():
    """Главная функция"""

    # ВАРИАНТ 1: Использовать переменную окружения
    # Установи: export ANTHROPIC_API_KEY='твой-ключ'
    alien = AlienClaude()

    # ВАРИАНТ 2: Указать ключ напрямую (НЕ БЕЗОПАСНО для продакшена!)
    # alien = AlienClaude(api_key='твой-api-ключ-здесь')

    # Запускаем интерактивный режим
    alien.interactive_mode()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.GREEN}👋 Прервано пользователем. До связи!{Colors.RESET}\n")
    except Exception as e:
        print(f"\n{Colors.BOLD}❌ КРИТИЧЕСКАЯ ОШИБКА:{Colors.RESET} {e}\n")
