import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import json

# ===== Load token =====
load_dotenv()
token = os.getenv("DISCORD_TOKEN")

# ===== Logging =====
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

# ===== Intents =====
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# ===== Player database =====
DATA_FILE = "players.json"

def load_players():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_players():
    with open(DATA_FILE, "w") as f:
        json.dump(players, f, indent=4)


MAX_PLAYERS = 50
DAYS = 7
players = load_players()

def add_player(name):
    if name in players:
        return "Player already exists."
    if len(players) >= MAX_PLAYERS:
        return "Team is full (50 players)."

    players[name] = {"days": [0] * DAYS}
    save_players()

    return f"Player {name} added. {MAX_PLAYERS - len(players)}/50 left"


def add_score(player_name, day, kilometers):
    if player_name not in players:
        return "Player not found."
    if not 1 <= day <= DAYS:
        return "Day must be between 1 and 7."
    if not 0 <= kilometers <= 2500:
        return "Kilometers must be between 0 and 2500."

    players[player_name]["days"][day - 1] = kilometers
    save_players()

    return f"Score updated: {player_name} - Day {day} = {kilometers} km"


def get_player_data(player_name):
    if player_name not in players:
        return "Player not found."
    return players[player_name]["days"]

# ===== Bot setup =====
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} ({bot.user.id})')
    print('------')

# ===== Commands =====
@bot.command(name='add')
async def cmd_addplayer(ctx, name: str):
    result = add_player(name)
    await ctx.send(result)

@bot.command(name='score')
async def cmd_score(ctx, day: int, name: str, km: int):
    result = add_score(name, day, km)
    await ctx.send(result)

@bot.command(name='show')
async def cmd_show(ctx, name: str, day: int = None):
    if name not in players:
        await ctx.send("Player not found.")
        return

    days_data = players[name]["days"]

    if day is None:
        # Show all days
        await ctx.send(f"{name}'s data: {days_data}")
    else:
        if not 1 <= day <= DAYS:
            await ctx.send(f"Day must be between 1 and {DAYS}.")
            return
        await ctx.send(f"{name} - Day {day}: {days_data[day - 1]} km")


@bot.command(name='nuke')
async def cmd_nuke(ctx):
    global players
    players = {}
    save_players()
    await ctx.send("💥 Database nuked.... my bad bro")


# ===== Run bot =====
bot.run(token, log_handler=handler, log_level=logging.DEBUG)