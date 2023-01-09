from aiogram.dispatcher.filters.state import StatesGroup, State

class users(StatesGroup):
    Q_users = State()

class orgs(StatesGroup):
    Q_orgs = State()

class repos(StatesGroup):
    Q_repos = State()