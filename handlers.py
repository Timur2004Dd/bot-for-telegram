from aiogram.dispatcher.filters import Command
from aiogram.types import Message
from main import dp
from states import users, orgs, repos
from aiogram.dispatcher import FSMContext
import requests
from github import Github
from data import write, read

##Стартовая команда##

@dp.message_handler(Command("start"))
async def show_hello(message: Message):
   await message.answer("Здраствуйте для работы ознакомьтесь с меню.")

##Статистика пользователя##

@dp.message_handler(Command("user_stat"), state=None)
async def get_username(message: Message):
    await message.answer("Хорошо, введите имя пользователя.")
    await users.Q_users.set()

@dp.message_handler(state=users.Q_users)
async def username(message: Message, state: FSMContext):

    # ответ пользователя #

    answer = message.text
    async with state.proxy() as data:
        data["username"] = answer
    data = await state.get_data()
    username = data.get("username")

    await message.answer("Спасибо, вот данные о вашем пользователе.")
    url = f"https://api.github.com/users/{username}"
    user_data = requests.get(url).json()
    print(user_data)
    if f"{requests.get(url)}" != "<Response [200]>":
        await message.answer("Пользователь не найден :(")
    else:
        await message.answer(
            f"Логин пользователя: {user_data['login']} \n"
            f"Id пользователя: {user_data['id']} \n"
            f"Ссылка на профиль: {user_data['html_url']} \n"
            f"Ссылка на репозитории пользователя: https://github.com/{user_data['login']}?tab=repositories \n"
            f"Страна: {user_data['location']} \n"
            f"Электронная почта: {user_data['email']} \n"
            f"Количество публичных репозиториев: {user_data['public_repos']} \n"
            f"Количество подписчиков: {user_data['followers']} \n"
            f"Профиль создан: {user_data['created_at']} \n"
            f"Последние обновление: {user_data['updated_at']} \n"
        )

        # запись в json файл #

        s = read("data.json")
        with open("data.json", "w") as f:
            pass
        if f"{user_data['login']}" in s.keys():
            s.update({user_data['login']: s.get(user_data['login'])+1})
        else:
            s[user_data['login']] = 1
        write(s, "data.json")

    await state.finish()

##Статистика организации##

@dp.message_handler(Command("org_stat"), state=None)
async def get_organisation(message: Message):
    await message.answer("Хорошо, введите название организации.")
    await orgs.Q_orgs.set()

@dp.message_handler(state=orgs.Q_orgs)
async def login(message: Message, state: FSMContext):

    # ответ пользователя #

    answer = message.text
    async with state.proxy() as data:
        data["login"] = answer
    data = await state.get_data()
    login = data.get("login")

    await message.answer("Спасибо, вот данные о организации.")
    url = f"https://api.github.com/users/{login}"
    if f"{requests.get(url)}" != "<Response [200]>":
        await message.answer("Организация не найдена :(")
    else:
        org_data = Github().get_organization(login)
        await message.answer(
            f"Логин организации: {org_data.login} \n"
            f"Id организации: {org_data.id} \n"
            f"Ссылка на профиль: {org_data.html_url} \n"
            f"Страна: {org_data.location} \n"
            f"Электронная почта: {org_data.email} \n"
            f"Количество публичных репозиториев: {org_data.public_repos} \n"
            f"Количество подписчиков: {org_data.followers} \n"
            f"Организация создана: {org_data.created_at} \n"
            f"Последние обновление: {org_data.updated_at} \n"
        )

        # запись в json файл #

        s = read("data.json")
        with open("data.json", "w") as f:
            pass
        if f"{org_data.login}" in s.keys():
            s.update({org_data.login: s.get(org_data.login) + 1})
        else:
            s[org_data.login] = 1
        write(s, "data.json")

    await state.finish()

##Статистика бота##

@dp.message_handler(Command("bot_stat"))
async def get_info(message: Message):
    s = read("data.json")
    str = ""
    sorted_dict = {}
    sorted_keys = sorted(s, key=s.get, reverse=True)
    for k in sorted_keys:
        sorted_dict[k] = s[k]

    if len(sorted_dict) < 20:
        for i in sorted_dict:
            str += f"{i} : {sorted_dict[i]} запросов \n"
    else:
        i = 0
        v = list(sorted_dict.keys())
        while i < 20:
            str += f"{v[i]} : {sorted_dict[v[i]]} запросов \n"
            i += 1

    await message.answer("Список наиболее запрашиваемых аккаунтов \n"
                         f"{str}"
                         )

##Статистика репозиториев##

@dp.message_handler(Command("repos_stat"), state=None)
async def get_repos(message: Message):
    await message.answer("Введите название пользователя или организации.")
    await repos.Q_repos.set()

@dp.message_handler(state=repos.Q_repos)
async def name(message: Message, state: FSMContext):
    answer = message.text
    async with state.proxy() as data:
        data["name"] = answer
    data = await state.get_data()
    name = data.get("name")
    await message.answer("Спасибо, вот список репозиториев пользователя/организации")
    url = f"https://api.github.com/users/{name}"
    try:
        name_data = Github().get_user(name)
    except:
        name_data = Github().get_organization(name)
    if f"{requests.get(url)}" != "<Response [200]>":
        await message.answer("Пользователь или организация не найдены :(")
    else:
        for repo in name_data.get_repos():
            await message.answer(
                f'Полное имя: {repo.full_name} \n '
                f'Описание: {repo.description} \n '
                f'Ссылка на репозиторий: https://github.com/{repo.full_name} \n'
                f'Дата создания: {repo.created_at} \n '
                f'Язык програмирования: {repo.language} \n ',
                reply_markup=None
            )
    await state.finish()
