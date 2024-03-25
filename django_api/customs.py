import builtins  # Импортируем модуль builtins, который содержит встроенные функции, такие как print
import traceback  # Импортируем модуль traceback для получения информации о стеке вызовов


def custom_print(*args, **kwargs):
    # Получаем информацию о месте вызова с использованием traceback
    stack = traceback.extract_stack(limit=2)
    calling_module = stack[0].filename
    calling_line = stack[0].lineno

    # Добавляем информацию о месте вызова к сообщению
    message = f"{calling_module}:{calling_line} - " + ' '.join(map(str, args))

    # Используем встроенную функцию print для вывода измененного сообщения
    print(message, **kwargs)
