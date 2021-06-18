import requests
import json
import csv
import pandas as pd

request_url = "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=67C30AF59C099700EF17170E1F86CB95&steamid=76561198220639648&format=json"

r = requests.get(request_url)

applist_url = "https://api.steampowered.com/ISteamApps/GetAppList/v2/"
r2 = requests.get(applist_url)

# print(r.text)
y = json.loads(r.text)
y2 = json.loads(r2.text)

# print(y)
# print(type(y))

my_games = y['response']['games']
game_list = y2['applist']['apps']

games = []

for g in my_games:
    # print(type(g))
    # print(g)
    # print(f"{g['appid']}: {g['playtime_forever']}")
    games.append([g['appid'], float(g['playtime_forever'] / 60)])

appids = [x[0] for x in games]

# print(appids)

for g in game_list:
    # print(f"id: {g['appid']}, name: {g['name']}")
    if g['appid'] in appids:
        # print(f"id: {g['appid']}, name: {g['name']}")
        idx = [x for x, y in enumerate(games) if y[0] == g['appid']][0]
        # print(idx)
        games[idx].append(g['name'])

games = sorted(games, key=lambda x: x[1])

# for g in games:
#     if len(g) > 2:
#         print(f"title: {g[2]}\t\tid: {g[0]}\thours: {g[1]}")
#     else:
#         print(g)

total_hours = sum(x[1] for x in games)

print(f"total hours: {total_hours}")

print(f"total days: {total_hours / 24}")

games = pd.DataFrame(games)
games.to_csv("steam_games.csv", header=["id", "hours", "name"], index=False, na_rep="NA")

# print("how old are you?")

# years = float(input())

# print(f"that accounts for {round(total_hours / (years * 365 * 24), 3)}% of your life. If you spend 1/3 of your life sleeping, that is {round(total_hours / (years * 365 * 24 * (2/3)), 3)}% of your waking hours.")
