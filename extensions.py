import requests
import json
from config import TOKEN

# Исключение для обработки ошибок API
class APIException(Exception):
    pass

# Класс для конвертации валют
class CurrencyConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: float) -> float:
        try:
            base = base.upper()
            quote = quote.upper()
            amount = float(amount)

            if base == quote:
                raise APIException("Нельзя конвертировать одну и ту же валюту")

            url = f"https://min-api.cryptocompare.com/data/price?fsym={quote}&tsyms={base}"
            response = requests.get(url)
            data = json.loads(response.text)

            if base not in data:
                raise APIException(f"Убедитесь в правильности котировок!")

            exchange_rate = data[base]
            converted_amount = amount * exchange_rate
            return converted_amount

        except ValueError:
            raise APIException("Недопустимая сумма. Пожалуйста, нужное количество переводимой валюты.")
        except Exception as e:
            raise APIException(str(e))
