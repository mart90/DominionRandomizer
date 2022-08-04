# DominionRandomizer

Randomizes a kingdom of 10 cards for the game Dominion, based on config parameters below. Includes features to exclude cards used in recent games and filter by card popularity within your playing group with the help of a google sheets spreadsheet.

Supports only these sets: Base, Intrigue, Dark ages, Prosperity

```
config = {
    "cards per set": {
        "base": 1,
        "intrigue": 1,
        "dark ages": 1,
        "prosperity": 1
    },
    "forced attributes": {
        "cost": 0,
        "plusCards": 2,
        "plusBuys": 1,
        "plusActions": 2,
        "plusCoins": 0,
    },
    "forced types": {
        "attack": 0,
        "reaction": 0,
        "trasher": 5
    },
    "popularity": {
        "min": 0.05,
        "max": 1.0,
        "include null": True
    },
    "attack forces reaction": True,
    "games to exclude": 3,
    "exclude cards if voted x times": 1
}
```
