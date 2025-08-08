import datetime
from config import *
from core.utils import send_message, is_owner, parse_command
from core.db import *
from core.weather import get_weather
from core.news import get_news
import openai

openai.api_key = OPENAI_API_KEY

conversation_history = {}

def handle_event(data):
    msg = data['object']['message']
    text = msg.get('text', '').strip()
    from_id = msg['from_id']
    peer_id = msg['peer_id']

    now = datetime.datetime.utcnow()

    # Инициализация БД (если нужно)
    init_db()

    # Логируем сообщение
    log_event(text, from_id)

    # Проверка мутов — если пользователь в муте, удаляем сообщение и выходим
    if is_muted(from_id, now):
        # Можно удалить сообщение, но Callback API не позволяет удалять сообщение, нужно через VK API (messages.delete)
        # Пропускаем пока (реализуй при желании)
        return

    # Проверяем иммунитет
    if has_immunity(from_id):
        # Не наказываем, просто реагируем, если нужно
        pass

    # Обработка упоминания бота или команды
    lower_text = text.lower()

    if (BOT_NAME in lower_text) or (f"@{BOT_NAME}" in lower_text) or lower_text.startswith("!"):
        cmd, args = parse_command(text, BOT_NAME)

        if cmd == "help":
            send_message(peer_id, HELP_TEXT())

        elif cmd == "reset":
            if is_owner(from_id):
                conversation_history[from_id] = []
                send_message(peer_id, "История чата сброшена.")
            else:
                send_message(peer_id, "Команда доступна только владельцу.")

        elif cmd == "погода":
            city = " ".join(args) if args else "Москва"
            weather = get_weather(city)
            send_message(peer_id, weather)

        elif cmd == "новости":
            news = get_news()
            send_message(peer_id, news)

        elif cmd == "баба":
            # Отправляем картинку (замени на реально работающий attachment)
            image_attachment = "photo-123456789_456239017"
            send_message(peer_id, "Спокойной ночи!", attachment=image_attachment)

        elif cmd == "пред":
            if is_owner(from_id):
                if args:
                    user_id = parse_vk_id(args[0])
                    count = add_warning(user_id)
                    send_message(peer_id, f"Предупреждение пользователю {args[0]}. Всего предупреждений: {count}")
                    if count >= 3:
                        # Кик пользователя
                        kick_user(peer_id, user_id)
                        send_message(peer_id, "Ибо нехуй.")
                else:
                    send_message(peer_id, "Использование: !пред @id")

        elif cmd == "бан":
            if is_owner(from_id):
                if args:
                    user_id = parse_vk_id(args[0])
                    ban_user(peer_id, user_id)
                    send_message(peer_id, "бай-бай, мазафака))")
                else:
                    send_message(peer_id, "Использование: !бан @id")

        elif cmd == "кик":
            if is_owner(from_id):
                if args:
                    user_id = parse_vk_id(args[0])
                    kick_user(peer_id, user_id)
                    send_message(peer_id, "туда его))")
                else:
                    send_message(peer_id, "Использование: !кик @id")

        elif cmd == "мут":
            if is_owner(from_id):
                if args:
                    user_id = parse_vk_id(args[0])
                    mute_for_hour(user_id)
                    send_message(peer_id, f"Пользователь {args[0]} замьючен на 1 час.")
                else:
                    send_message(peer_id, "Использование: !мут @id")

        elif cmd == "снятьмут":
            if is_owner(from_id):
                if args:
                    user_id = parse_vk_id(args[0])
                    unmute_user(user_id)
                    send_message(peer_id, f"Мут снят с пользователя {args[0]}.")
                else:
                    send_message(peer_id, "Использование: !снятьмут @id")

        elif cmd == "иммунитет":
            if is_owner(from_id):
                if args:
                    user_id = parse_vk_id(args[0])
                    add_immunity(user_id)
                    send_message(peer_id, f"Пользователь {args[0]} теперь под иммунитетом.")
                else:
                    send_message(peer_id, "Использование: !иммунитет @id")

        elif cmd == "пиши":
            if is_owner(from_id):
                msg_text = " ".join(args)
                send_message(GROUP_ID, msg_text)
            else:
                send_message(peer_id, "Команда доступна только владельцу.")

        else:
            # По умолчанию — отвечаем через ChatGPT
            history = conversation_history.get(from_id, [])
            history.append({"role": "user", "content": text})
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=history
                )
                answer = response.choices[0].message.content
                history.append({"role": "assistant", "content": answer})
                conversation_history[from_id] = history[-20:]  # Сохраняем последние 20 сообщений
                send_message(peer_id, answer)
            except Exception as e:
                send_message(peer_id, "Ошибка при обращении к нейросети.")

def HELP_TEXT():
    return (
        "Доступные команды:\n"
        "!погода <город> — погода в городе\n"
        "!новости — новости технологий и игр\n"
        "!баба — красивая картинка девушки\n"
        "!reset — сбросить историю диалога (только владелец)\n"
        "!пред @id — предупреждение пользователю (только владелец)\n"
        "!бан @id — навсегда забанить и кикнуть (только владелец)\n"
        "!кик @id — кикнуть из беседы (только владелец)\n"
        "!мут @id — мут на 1 час (только владелец)\n"
        "!снятьмут @id — снять мут (только владелец)\n"
        "!иммунитет @id — иммунитет (только владелец)\n"
        "!пиши <текст> — отправить сообщение от бота (только владелец)\n"
        "!help — это сообщение\n"
    )

# Вспомогательные функции парсинга и управления пользователями:

def parse_vk_id(text):
    # Извлекает числовой ID из упоминания @id или @username
    if text.startswith("@"):
        text = text[1:]
    # Если это число — возвращаем как int
    if text.isdigit():
        return int(text)
    # TODO: можно добавить запрос к VK API для получения ID по имени
    return 0

def kick_user(peer_id, user_id):
    # Метод kick (исключение из беседы)
    params = {
        "peer_id": peer_id,
        "member_id": user_id,
        "access_token": BOT_TOKEN,
        "v": "5.131"
    }
    url = "https://api.vk.com/method/messages.removeChatUser"
    requests.post(url, params=params)

def ban_user(peer_id, user_id):
    # Для VK Callback API нет отдельной команды бан, но можно кикнуть и игнорировать потом
    kick_user(peer_id, user_id)
    # Здесь можно реализовать логику игнора в коде (не реализовано)

def mute_for_hour(user_id):
    from datetime import datetime, timedelta
    until = datetime.utcnow() + timedelta(hours=1)
    mute_user(user_id, until.isoformat())
