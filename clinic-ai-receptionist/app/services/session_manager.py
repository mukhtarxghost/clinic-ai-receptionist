sessions = {}


def get_session(user_id: str):
    if user_id not in sessions:
        sessions[user_id] = {}

    return sessions[user_id]


def update_session(user_id: str, key: str, value):
    session = get_session(user_id)
    session[key] = value


def clear_session(user_id: str):
    if user_id in sessions:
        del sessions[user_id]