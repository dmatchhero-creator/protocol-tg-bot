#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль детекции кризисных ситуаций в сообщениях
Определяет психоз, суицидальные мысли, панику, угрозы
"""

import re
from enum import Enum
from typing import List, Optional, Tuple


class CrisisType(Enum):
    """Типы кризисных ситуаций"""
    PSYCHOSIS = "psychosis"  # Психоз: голоса, видения, галлюцинации
    SUICIDE = "suicide"  # Суицидальные мысли
    PANIC = "panic"  # Паническая атака, крайний стресс
    THREATS = "threats"  # Угрозы жизни от других людей
    NONE = "none"  # Кризис не обнаружен


class CrisisDetector:
    """Детектор кризисных ситуаций в текстах"""

    def __init__(self):
        # Паттерны для детекции психоза
        self.psychosis_patterns = [
            r'голос[аы]?\s+(в|внутри)\s+голов[еы]',
            r'слыш[уа]\s+(голос[аы]|в\s+голове)',
            r'виж[уа]\s+(труп|смерть|видени[ея])',
            r'(галлюцинаци[ия]|бред)',
            r'говор[ия]т\s+(мне|со\s+мной).+голос',
            r'(нереальн|не\s+понима[ю])\s+что\s+реальн',
            r'(параноя|преследу[ю]т)',
            r'картина\s+смерти',
            r'голос[аы]?\s+(приказыва|говор)',
            r'не\s+(реальн|существу)',
            r'бог\s+(говорит|сказал)',
        ]

        # Паттерны для детекции суицидальных мыслей
        self.suicide_patterns = [
            r'хоч[уа]\s+(умереть|покончить|убить\s+себя)',
            r'не\s+хоч[уа]\s+жить',
            r'лучше\s+(бы\s+)?умереть',
            r'жизнь\s+не\s+имеет\s+смысл',
            r'(суицид|самоубийств)',
            r'уйти\s+из\s+жизни',
            r'(свести\s+счёты|сведу\s+счёты)\s+с\s+жизнь[ю]',
        ]

        # Паттерны для детекции панической атаки / экстремального стресса
        self.panic_patterns = [
            r'не\s+могу\s+дышать',
            r'серд[цо]е\s+(бьётся|колотится)',
            r'паническ[ая]\s+атак',
            r'задыха[ю]сь',
            r'(крайни[йе]|экстремальн[ыйое])\s+стресс',
            r'не\s+могу\s+успокоиться',
            r'всё\s+(рушится|падает)',
        ]

        # Паттерны для детекции угроз
        self.threats_patterns = [
            r'угрожа[ю]т.+(убить|найти|расправиться)',
            r'сказали\s+что\s+(найдут|убь[ю]т)',
            r'бо[ю]сь\s+за\s+(жизнь|детей|семь[ю])',
            r'ищ[уа]т\s+меня',
            r'хот[ия]т\s+убить',
            r'угрозы.+(жизни|смерть[ю])',
        ]

        # Ключевые слова усиления (увеличивают уверенность в детекции)
        self.intensity_markers = [
            r'помог[ий]те',
            r'срочно',
            r'спасите',
            r'не\s+знаю\s+что\s+делать',
            r'прямо\s+сейчас',
            r'очень\s+страшно',
        ]

    def detect_crisis(self, text: str) -> Tuple[CrisisType, float]:
        """
        Определяет тип кризиса в тексте

        Args:
            text: текст сообщения

        Returns:
            Tuple[CrisisType, float]: (тип кризиса, уверенность 0.0-1.0)
        """
        if not text:
            return (CrisisType.NONE, 0.0)

        text_lower = text.lower()

        # Считаем совпадения для каждого типа кризиса
        psychosis_score = self._count_matches(text_lower, self.psychosis_patterns)
        suicide_score = self._count_matches(text_lower, self.suicide_patterns)
        panic_score = self._count_matches(text_lower, self.panic_patterns)
        threats_score = self._count_matches(text_lower, self.threats_patterns)

        # Добавляем вес от маркеров интенсивности
        intensity_bonus = self._count_matches(text_lower, self.intensity_markers) * 0.2

        # Определяем максимальный score
        scores = {
            CrisisType.PSYCHOSIS: psychosis_score + intensity_bonus,
            CrisisType.SUICIDE: suicide_score + intensity_bonus,
            CrisisType.PANIC: panic_score + intensity_bonus,
            CrisisType.THREATS: threats_score + intensity_bonus,
        }

        max_crisis_type = max(scores, key=scores.get)
        max_score = scores[max_crisis_type]

        # Нормализуем score в уверенность (0.0 - 1.0)
        confidence = min(max_score / 3.0, 1.0)  # 3+ совпадений = 100% уверенность

        # Порог для детекции кризиса
        CRISIS_THRESHOLD = 0.3

        if confidence >= CRISIS_THRESHOLD:
            return (max_crisis_type, confidence)
        else:
            return (CrisisType.NONE, confidence)

    def _count_matches(self, text: str, patterns: List[str]) -> float:
        """
        Считает количество совпадений паттернов в тексте

        Args:
            text: текст для проверки
            patterns: список regex паттернов

        Returns:
            float: количество совпадений
        """
        count = 0
        for pattern in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                count += 1
        return float(count)

    def get_multiple_crises(self, text: str, threshold: float = 0.3) -> List[Tuple[CrisisType, float]]:
        """
        Определяет все типы кризисов в тексте (может быть несколько одновременно)

        Args:
            text: текст сообщения
            threshold: порог уверенности для включения в результат

        Returns:
            List[Tuple[CrisisType, float]]: список (тип кризиса, уверенность)
        """
        if not text:
            return []

        text_lower = text.lower()

        psychosis_score = self._count_matches(text_lower, self.psychosis_patterns)
        suicide_score = self._count_matches(text_lower, self.suicide_patterns)
        panic_score = self._count_matches(text_lower, self.panic_patterns)
        threats_score = self._count_matches(text_lower, self.threats_patterns)

        intensity_bonus = self._count_matches(text_lower, self.intensity_markers) * 0.2

        scores = {
            CrisisType.PSYCHOSIS: psychosis_score + intensity_bonus,
            CrisisType.SUICIDE: suicide_score + intensity_bonus,
            CrisisType.PANIC: panic_score + intensity_bonus,
            CrisisType.THREATS: threats_score + intensity_bonus,
        }

        results = []
        for crisis_type, score in scores.items():
            confidence = min(score / 3.0, 1.0)
            if confidence >= threshold:
                results.append((crisis_type, confidence))

        # Сортируем по уверенности (убывание)
        results.sort(key=lambda x: x[1], reverse=True)

        return results


# Глобальный экземпляр детектора
detector = CrisisDetector()


def detect_crisis_in_message(text: str) -> Tuple[CrisisType, float]:
    """
    Удобная функция для детекции кризиса в сообщении

    Args:
        text: текст сообщения

    Returns:
        Tuple[CrisisType, float]: (тип кризиса, уверенность)
    """
    return detector.detect_crisis(text)
