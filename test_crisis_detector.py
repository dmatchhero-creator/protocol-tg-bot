#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Тестовый скрипт для проверки детектора кризисов
"""

from crisis_detector import detect_crisis_in_message, CrisisType
from crisis_responses import get_crisis_response


def test_crisis_detection():
    """Тестирование детекции различных кризисов"""

    test_cases = [
        # ПСИХОЗ
        {
            "text": "Я слышу голоса в голове, они говорят мне что-то странное. Вижу вещи которых нет.",
            "expected_type": CrisisType.PSYCHOSIS,
            "description": "Психоз: голоса и галлюцинации"
        },
        {
            "text": "СЛЫШУ В ГОЛОВЕ ТЫ ЕЩЕ ВЫЕБЫВАЕШЬСЯ? КАРТИНА СМЕРТИ перед глазами",
            "expected_type": CrisisType.PSYCHOSIS,
            "description": "Психоз: голоса и видения смерти"
        },

        # СУИЦИД
        {
            "text": "Я больше не хочу жить. Жизнь не имеет смысла, лучше покончить с этим.",
            "expected_type": CrisisType.SUICIDE,
            "description": "Суицидальные мысли"
        },
        {
            "text": "хочу умереть, не вижу выхода из этой ситуации",
            "expected_type": CrisisType.SUICIDE,
            "description": "Суицидальные мысли прямые"
        },

        # УГРОЗЫ
        {
            "text": "Мне угрожают. Сказали что найдут меня и моих детей. Боюсь за свою жизнь.",
            "expected_type": CrisisType.THREATS,
            "description": "Угрозы жизни"
        },
        {
            "text": "сказали что найдут суки мой паспорт найдут меня и моих внуков",
            "expected_type": CrisisType.THREATS,
            "description": "Угрозы семье и близким"
        },

        # ПАНИКА
        {
            "text": "У меня паническая атака! Не могу дышать, сердце колотится, задыхаюсь помогите",
            "expected_type": CrisisType.PANIC,
            "description": "Паническая атака"
        },
        {
            "text": "экстремальный стресс не могу успокоиться всё рушится",
            "expected_type": CrisisType.PANIC,
            "description": "Крайний стресс"
        },

        # НЕТ КРИЗИСА
        {
            "text": "Здравствуйте, хочу решить проблему с тревогой перед выступлениями",
            "expected_type": CrisisType.NONE,
            "description": "Обычный запрос"
        },
        {
            "text": "У меня прокрастинация и низкая самооценка",
            "expected_type": CrisisType.NONE,
            "description": "Обычная проблема"
        },
    ]

    print("=" * 80)
    print("ТЕСТИРОВАНИЕ ДЕТЕКТОРА КРИЗИСОВ")
    print("=" * 80)
    print()

    passed = 0
    failed = 0

    for i, case in enumerate(test_cases, 1):
        text = case["text"]
        expected = case["expected_type"]
        description = case["description"]

        crisis_type, confidence = detect_crisis_in_message(text)

        # Проверяем результат
        status = "✅ PASS" if crisis_type == expected else "❌ FAIL"
        if crisis_type == expected:
            passed += 1
        else:
            failed += 1

        print(f"Тест {i}: {description}")
        print(f"Текст: {text[:70]}{'...' if len(text) > 70 else ''}")
        print(f"Ожидалось: {expected.value}")
        print(f"Получено: {crisis_type.value} (уверенность: {confidence:.0%})")
        print(f"Статус: {status}")
        print("-" * 80)
        print()

    print("=" * 80)
    print(f"РЕЗУЛЬТАТЫ: {passed} прошли, {failed} провалились из {len(test_cases)}")
    print("=" * 80)


def demo_crisis_responses():
    """Демонстрация ответов на кризисы"""

    print("\n\n")
    print("=" * 80)
    print("ДЕМОНСТРАЦИЯ ОТВЕТОВ НА КРИЗИСЫ")
    print("=" * 80)
    print()

    crisis_types = [
        CrisisType.PSYCHOSIS,
        CrisisType.SUICIDE,
        CrisisType.PANIC,
        CrisisType.THREATS,
    ]

    for crisis_type in crisis_types:
        print(f"\n{'=' * 80}")
        print(f"ОТВЕТ НА: {crisis_type.value.upper()}")
        print(f"{'=' * 80}\n")
        response = get_crisis_response(crisis_type, 0.9)
        print(response)
        print()


if __name__ == "__main__":
    # Запускаем тесты
    test_crisis_detection()

    # Показываем примеры ответов
    demo_crisis_responses()
