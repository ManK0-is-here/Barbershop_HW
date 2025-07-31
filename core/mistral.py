from pprint import pprint
from mistralai import Mistral

from barbershop.settings import MISTRAL_API_KEY, MISTRAL_MODERATIONS_GRADES

# Предполагается, что MISTRAL_API_KEY и MISTRAL_MODERATIONS_GRADES 
# загружены из settings.py

def is_bad_review(
    review_text: str,
    api_key: str = MISTRAL_API_KEY,
    grades: dict = MISTRAL_MODERATIONS_GRADES,
) -> bool:
    # Создаем клиента Mistral с переданным API ключом
    client = Mistral(api_key=api_key)

    # Формируем запрос
    response = client.classifiers.moderate_chat(
        model="mistral-moderation-latest",
        inputs=[{"role": "user", "content": review_text}],
    )
    # Вытаскиваем данные с оценкой
    result = response.results[0].category_scores

    # Округляем значения до двух знаков после запятой
    result = {key: round(value, 2) for key, value in result.items()}

    pprint(result)

    # Словарь под результаты проверки
    checked_result = {}

    for key, value in result.items():
        if key in grades:
            checked_result[key] = value >= grades[key]

    # Если одно из значений True, то отзыв не проходит модерацию
    return any(checked_result.values())