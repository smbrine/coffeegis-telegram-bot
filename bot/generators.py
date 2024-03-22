import json
from html import escape


async def return_emoji(distance):
    if distance < 1:
        return "🚶"
    elif distance < 5:
        return "🛴"
    elif distance < 10:
        return "🚲"
    elif distance < 100:
        return "🚗"
    elif distance < 750:
        return "🚃"
    else:
        return "🛫"


async def generate_cafe_card(cafe, from_me=False):
    msg = f"<b>{escape(cafe.name)}</b>\n\n"
    msg += f"{escape(cafe.description.location_description)}"
    msg += f"{escape(cafe.description.interior_description)}"
    msg += f"{escape(cafe.description.menu_description)}"
    msg += f"{escape(cafe.description.place_history)}"
    msg += f"{escape(cafe.description.arbitrary_description)}"
    msg += '\n\n'
    if cafe.roaster.name:
        msg += f'Обжарщик: {escape(cafe.roaster.name)}\n'
        msg += f'Сайт: {escape(cafe.roaster.website)}\n' if cafe.roaster.website else '\n'
    msg += (
        f"📍<code>{escape(cafe.address)}</code>\n"
        + f"{await return_emoji(cafe.distance)}в "
        + f"{escape(str(round(cafe.distance, 2)))}км {'от меня' if from_me else 'от тебя'}"
    )
    return msg


async def generate_profile_card(user):
    months = {
        "Jan": "января",
        "Feb": "февраля",
        "Mar": "марта",
        "Apr": "апреля",
        "May": "мая",
        "Jun": "июня",
        "Jul": "июля",
        "Aug": "августа",
        "Sep": "сентября",
        "Oct": "октября",
        "Nov": "ноября",
        "Dec": "декабря",
    }

    reg_date = user.created_at.strftime(
        "%d %b, %Y"
    )
    for eng, rus in months.items():
        reg_date = reg_date.replace(eng, rus)

    msg = f"Телефон: {user.phone or 'нет'}\n\n"
    msg += f"Уведомлять о новых кафе: {'да' if user.new_cafes_notify else 'нет'}\n\n"
    msg += f"Всего общих поисковых запросов: {user.general_search_requests or 0}\n"
    msg += f"Всего инлайн запросов: {user.inline_search_requests or 0}\n\n"
    msg += f"Дата регистрации: {reg_date}\n\n"
    msg += "Мои запросы:\n"
    if user.requests:
        for req in user.requests:
            for k, v in req.__dict__.items():
                if k == "contents":
                    msg += (f'\nНазвание: {v.get("name")}\n' +
                            f'Адрес: {v.get("address")}\n')
                elif k == "created_at":
                    msg += f'Добавлен: {v}\n'
    else:
        msg += "Тут пока пусто..."

    return msg
