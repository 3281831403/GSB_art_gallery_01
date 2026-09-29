"""美术馆核心逻辑：展品、展厅、讲解和租金。"""

import json

DEPOSIT_PER_EXHIBIT = 20
HALL_CAPACITY = 2


def new_game():
    return {
        "exhibits": {},
        "hall_load": 0,
        "hall_capacity": HALL_CAPACITY,
        "deposit": 100,
        "day": 1,
        "exhibit_id": 0,
        "guides": {"G1": True},
    }


def save_state(state):
    return json.dumps(state, ensure_ascii=False)


def load_state(text):
    return json.loads(text)


def register(state, exhibit_id):
    if exhibit_id in state["exhibits"]:
        return False
    state["exhibits"][exhibit_id] = {"health": 100}
    return True


def place(state, exhibit_id):
    exhibit = state["exhibits"].get(exhibit_id)
    if exhibit is None:
        return False
    if exhibit.get("placed"):
        return False
    if state["hall_load"] >= state["hall_capacity"]:
        return False
    exhibit["placed"] = True
    state["hall_load"] += 1
    return True


def fee(state, exhibit_id, end_day):
    return end_day - state["day"]


def cancel(state, exhibit_id):
    exhibit = state["exhibits"].get(exhibit_id)
    if exhibit is not None and exhibit.get("placed"):
        exhibit["placed"] = False
        state["hall_load"] -= 1
    state["deposit"] += DEPOSIT_PER_EXHIBIT
    return True


def assign(state, exhibit_id, guide):
    exhibit = state["exhibits"].get(exhibit_id)
    if exhibit is None:
        return False
    if not state.get("guides", {}).get(guide, False):
        return False
    exhibit["guide"] = guide
    return True


def setup(state, exhibit_id):
    exhibit = state["exhibits"].get(exhibit_id)
    if exhibit is None:
        return False
    if exhibit.get("failed"):
        return False
    state["deposit"] -= 1
    return True


def damage(state, exhibit_id):
    exhibit = state["exhibits"].get(exhibit_id)
    if exhibit is None:
        return False
    exhibit["health"] -= 10
    return True


def main():
    print("美术馆 - 命令: register/place/fee/cancel/assign/setup/damage/quit")
    while True:
        try:
            raw = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not raw or raw == "quit":
            break
        print("ok")


if __name__ == "__main__":
    main()
