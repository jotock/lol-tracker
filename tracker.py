import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("RIOT_API_KEY")

JUGADORES = [
    {"nombre": "GERUG Jotcok", "tag": "EUW"},
]

def get_puuid(nombre, tag):
    url = f"https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{nombre}/{tag}"
    r = requests.get(url, headers={"X-Riot-Token": API_KEY})
    return r.json().get("puuid")

def get_summoner(puuid):
    url = f"https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid}"
    r = requests.get(url, headers={"X-Riot-Token": API_KEY})
    return r.json()

def get_ranked(puuid):
    url = f"https://euw1.api.riotgames.com/lol/league/v4/entries/by-puuid/{puuid}"
    r = requests.get(url, headers={"X-Riot-Token": API_KEY})
    datos = r.json()
    for entrada in datos:
        if entrada["queueType"] == "RANKED_SOLO_5x5":
            wins = entrada["wins"]
            losses = entrada["losses"]
            winrate = round(wins / (wins + losses) * 100, 1)
            return {
                "tier": entrada["tier"],
                "rank": entrada["rank"],
                "lp": entrada["leaguePoints"],
                "wins": wins,
                "losses": losses,
                "winrate": winrate,
            }
    return None

def actualizar():
    resultados = []
    for jugador in JUGADORES:
        print(f"Obteniendo datos de {jugador['nombre']}...")
        puuid = get_puuid(jugador["nombre"], jugador["tag"])
        print("PUUID:", puuid)
        summoner = get_summoner(puuid)
        print("Summoner:", summoner)
        ranked = get_ranked(puuid)
        if ranked:
            resultados.append({
                "nombre": jugador["nombre"],
                **ranked
            })
            print(f"  {ranked['tier']} {ranked['rank']} {ranked['lp']}LP — {ranked['winrate']}% WR")
        else:
            print(f"  Sin ranked este split")
    
    with open("datos.json", "w") as f:
        json.dump(resultados, f, indent=2)
    print("\nDatos guardados en datos.json")

if __name__ == "__main__":
    actualizar()