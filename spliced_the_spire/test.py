start = {
    "actor": {
        "gold": 99,
        "max_health": 88,
        "max_energy": 3,
        "current_energy": 3,
        "potions": [
            "Potion Slot",
            "Potion Slot",
            "Potion Slot"
        ],
        "master_deck": [
            {
                "upgraded": False,
                "id": "Strike_R"
            },
            {
                "upgraded": False,
                "id": "Strike_R"
            },
            {
                "upgraded": False,
                "id": "Strike_R"
            },
            {
                "upgraded": False,
                "id": "Strike_R"
            },
            {
                "upgraded": False,
                "id": "Strike_R"
            },
            {
                "upgraded": False,
                "id": "Defend_R"
            },
            {
                "upgraded": False,
                "id": "Defend_R"
            },
            {
                "upgraded": False,
                "id": "Defend_R"
            },
            {
                "upgraded": False,
                "id": "Defend_R"
            },
            {
                "upgraded": False,
                "id": "Bash"
            }
        ],
        "name": "Luke",
        "current_health": 88,
        "relics": ["Burning Blood"],
        "class": "IRONCLAD"
    },
    "start_time": "2023-12-17T23:57:28.998",
    "act": 1,
    "ascension": 0,
    "name": "Exordium",
    "monsters": [{
        "max_health": 52,
        "name": "Cultist",
        "current_health": 52,
        "id": "Cultist",
        "intent": "DEBUG"
    }],
    "id": "Exordium",
    "floor": 1
}

from new.enemies import enemies as enemy_cls_map

env = {}
ascension = start['ascension']
act = start['act']
enemies = []
for monster in start['monsters']:
    enemy_cls = enemy_cls_map.get(monster['id'], None)
    if not enemy_cls:
        raise Exception()
    enemies.append(
        enemy_cls(
            environment=env,
            ascension=ascension,
            act=act,
            max_health=monster['max_health'],
            testing=True))

print(enemies)
print(enemies[0].health)