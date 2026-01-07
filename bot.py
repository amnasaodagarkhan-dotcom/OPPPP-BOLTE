import os
import json
import sqlite3
from dotenv import load_dotenv
import discord
from discord.ext import commands
from modules.utils import is_admin, run_cmd
from modules.lxc_manager import create_lxc, delete_lxc, restart_lxc, list_lxc
from modules.ai_healer import check_and_fix_all

# Load .env
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
PREFIX = os.getenv("PREFIX", "!")
ADMIN_IDS = [int(x) for x in os.getenv("ADMIN_IDS","").split(",") if x]

bot = commands.Bot(command_prefix=PREFIX, intents=discord.Intents.all())

# Load nodes
nodes = json.load(open("nodes.json"))

# SQLite DB
conn = sqlite3.connect("database.sqlite")
cursor = conn.cursor()

@bot.event
async def on_ready():
    print(f"{bot.user} is online")
    await bot.change_presence(activity=discord.Game(name="BloodNodes Hosting"))

# ---------- Commands ----------
@bot.command()
async def status(ctx):
    if not is_admin(ctx.author.id, ADMIN_IDS):
        return await ctx.send("❌ No access")
    msg = f"🤖 **BloodNodes Bot Status**\nBot is Online ✅\nConnected Nodes:\n"
    for node_name, node in nodes.items():
        try:
            ping = run_cmd(node, "echo alive")
            status_node = "🟢 Online" if ping else "🔴 Offline"
        except:
            status_node = "🔴 Offline"
        msg += f"• {node_name}: {status_node}\n"
    await ctx.send(msg)

@bot.command()
async def help(ctx):
    help_text = f"""
💀 **BloodNodes Bot Help Menu**
Prefix: {PREFIX}

**VPS Commands**
• !create <node> <name> <RAM> <CPU> → Create VPS
• !delete <node> <name> → Delete VPS
• !restart <node> <name> → Restart VPS
• !list <node> → List VPS on node
• !port <node> <IP> <host_port> <lxc_port> → Forward port

**Bot Commands**
• !status → Check bot & node status
• !screenshot <vps_name> → Get watermarked screenshot
• !help → Show this menu
"""
    await ctx.send(help_text)

@bot.command()
async def vps(ctx):
    if not is_admin(ctx.author.id, ADMIN_IDS):
        return await ctx.send("❌ No access")
    menu = """
🖥️ **BloodNodes VPS Management Menu**
1️⃣ !create <node> <name> <RAM> <CPU> → Create VPS
2️⃣ !delete <node> <name> → Delete VPS
3️⃣ !restart <node> <name> → Restart VPS
4️⃣ !list <node> → List all VPS on node
5️⃣ !port <node> <IP> <host_port> <lxc_port> → Forward port
"""
    await ctx.send(menu)

@bot.command()
async def create(ctx, node_name, name, ram, cpu):
    if not is_admin(ctx.author.id, ADMIN_IDS):
        return await ctx.send("❌ No access")
    result = create_lxc(node_name, name, ram, cpu)
    await ctx.send(result)

bot.run(TOKEN)
