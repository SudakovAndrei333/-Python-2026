# Ошибки

| Где             | Ошибка | Было | Исправлено |
|-----------------|--------|------|-----------|
| `get_age()`     | Инверсия вычитания | `self.yob - now.year` | `now.year - self.yob` |
| `set_name()`    | Присваивание самому себе | `self.name = self.name` | `self.name = name` |
| `set_address()` | Сравнение вместо присваивания | `self.address == address` | `self.address = address` |
| `is_homeless()` | NameError + неверная логика | `return address is None` | `return not self.address` |
| модуль datetime | Отсутствует импорт | — | `import datetime` |

## Суть ошибок

1. **`get_age`**: возраст был отрицательным (из года рождения вычитали текущий).
2. **`set_name`**: имя не менялось, так как значение присваивалось само себе.
3. **`set_address`**: адрес не менялся — оператор `==` не изменяет данные.
4. **`is_homeless`**: 
   - `NameError`: переменная `address` без `self`
   - Логика: адрес по умолчанию `''`, а не `None`, поэтому проверка `is None` всегда `False`
5. **Импорт**: без `import datetime` метод `get_age()` выбрасывает ошибку.

## Как обнаружено

- Тесты на `get_age()` > ожидали положительный возраст, получали отрицательный
- Тесты на `set_name()`/`set_address()` > значения не менялись после вызова сеттеров
- Тест на `is_homeless()` > `NameError` при выполнении
- Запуск модуля → `NameError: name 'datetime' is not defined`
