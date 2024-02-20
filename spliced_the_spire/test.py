from main.abstractions import AbstractCard
from main.cards import card_classes

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

from main.enemies import enemies as enemy_cls_map

env = {}
ascension = start['ascension']
act = start['act']
enemies = []
for monster in start['monsters']:
    enemy_cls = enemy_cls_map.get(monster['id'], None)
    if not enemy_cls:
        # TODO: Auto-tag missing enemy exception
        raise Exception("Missing enemy")
    try:
        enemy = enemy_cls(
            environment=env,
            ascension=ascension,
            act=act,
            max_health=monster['max_health'],
            testing=True)
    except Exception as e:
        # TODO: Auto-tag unexpected max_health
        raise e
    enemies.append(enemy)

print(card_classes)
for card in start['actor']['master_deck']:
    sts_name = card['id']
    upgraded = card['upgraded']
    card_cls = card_classes[sts_name]
    new_card = card_cls(upgraded=upgraded)
    print(new_card)

