"""美术馆核心逻辑：展品、展厅、讲解和租金。"""

import json

SETUP_COST = 20
GUIDES = ("G1",)


def new_game():
    return {
        "exhibits": {},
        "hall_load": 0,
        "hall_capacity": 2,
        "deposit": 100,
        "day": 1,
        "exhibit_id": 0,
        "guides": {guide: {"leave": False} for guide in GUIDES},
    }


def save_state(state):
    return json.dumps(state, ensure_ascii=False)


def load_state(text):
    state = json.loads(text)
    return state


def register(state, exhibit_id):
    if exhibit_id in state["exhibits"]:
        return False
    state["exhibits"][exhibit_id] = {"health": 100}
    return True


def place(state, exhibit_id):
    if state["hall_load"] >= state["hall_capacity"]:
        return False
    if state["exhibits"].get(exhibit_id, {}).get("placed"):
        return False
    state["hall_load"] += 1
    state["exhibits"].setdefault(exhibit_id, {"health": 100})["placed"] = True
    return True


def fee(state, exhibit_id, end_day):
    return end_day - state["day"]


def cancel(state, exhibit_id):
    state["deposit"] += SETUP_COST
    exhibit = state["exhibits"].get(exhibit_id)
    if exhibit is not None and exhibit.get("placed"):
        state["hall_load"] -= 1
        exhibit["placed"] = False
        if "guide" in exhibit:
            guide = state["guides"].get(exhibit["guide"])
            if guide is not None:
                guide["busy"] = False
            del exhibit["guide"]
    return True


def assign(state, exhibit_id, guide):
    guide_info = state["guides"].get(guide)
    if guide_info is None or guide_info.get("leave") or guide_info.get("busy"):
        return False
    state["exhibits"][exhibit_id]["guide"] = guide
    guide_info["busy"] = True
    return True


def setup(state, exhibit_id):
    if state["exhibits"][exhibit_id].get("failed"):
        return False
    state["deposit"] -= SETUP_COST
    return True


def damage(state, exhibit_id):
    state["exhibits"][exhibit_id]["health"] -= 10
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
