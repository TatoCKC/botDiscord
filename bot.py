import discord
from discord.ext import commands
import json
import os
import random

TOKEN = "AQUI_TU_TOKEN"

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ------------------------------
#   SISTEMA DE ARCHIVO JSON
# ------------------------------

RUTA = "datos_quiniela.json"

def cargar_datos():
    if not os.path.exists(RUTA):
        with open(RUTA, "w") as f:
            json.dump({
                "pronosticos": {},
                "resultados": {},
                "puntos": {},
                "clasificacion": {},
                "penalizaciones": {}
            }, f, indent=4)

    with open(RUTA, "r") as f:
        return json.load(f)

def guardar_datos(datos):
    with open(RUTA, "w") as f:
        json.dump(datos, f, indent=4)

# ------------------------------
#   EVENTO DE INICIO
# ------------------------------

@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")

# ------------------------------
#   COMANDO: !ping
# ------------------------------

@bot.command()
async def ping(ctx):
    await ctx.send

@bot.command()
async def verpronosticos(ctx):
    datos = cargar_datos()
    pronos = datos["pronosticos"]

    if not pronos:
        await ctx.send("Aún no hay pronósticos registrados.")
        return

    mensaje = "📋 **Pronósticos de la jornada**\n\n"

    for usuario_id, partidos in pronos.items():
        usuario = await bot.fetch_user(int(usuario_id))
        mensaje += f"**{usuario.display_name}:**\n"

        for partido, signo in partidos.items():
            mensaje += f"• Partido {partido}: {signo}\n"

        mensaje += "\n"

    await ctx.send(mensaje)
