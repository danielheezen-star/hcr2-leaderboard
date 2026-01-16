import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os

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
MAX_PLAYERS = 50
DAYS = 7
players = {}

def add_player(name):
    if name in players:
        return "Player already exists."
    if len(players) >= MAX_PLAYERS:
        return "Team is full (50 players)."
    players[name] = {"days": [0] * DAYS}
    return f"Player {name} added. {MAX_PLAYERS - len(players)}/50 left"

def add_score(player_name, day, kilometers):
    if player_name not in players:
        return "u misstyped or this guy changed his fucking name"
    if not 1 <= day <= DAYS:
        return "Day must be between 1 and 7."
    if not 0 <= kilometers <= 2500:
        return "Kilometers must be between 0 and 2500."
    players[player_name]["days"][day - 1] = kilometers
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
@bot.command(name='addplayer')
async def cmd_addplayer(ctx, name: str):
    result = add_player(name)
    await ctx.send(result)

@bot.command(name='score')
async def cmd_score(ctx, day: int, name: str, km: int):
    result = add_score(name, day, km)
    await ctx.send(result)

@bot.command(name='show')
async def cmd_show(ctx, name: str):
    data = get_player_data(name)
    await ctx.send(f"{name}'s data: {data}")

@bot.command(name='nuke')
async def cmd_nuke(ctx):
    global players
    players = {}  # reset database
    await ctx.send("💥 Database nuked... My bad bro")

# ===== Run bot =====
bot.run(token, log_handler=handler, log_level=logging.DEBUG)