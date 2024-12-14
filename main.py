import discord
from discord.ext import commands, tasks
import datetime
import asyncio

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='$', intents=intents)

reminders = {} #Diccionario o algo asi

@bot.event
async def on_ready():
    print(f'Bot is ready. Logged in as {bot.user}')
    check.start()

@bot.command()
async def reminder(ctx, time: str, *, action: str):
    """Establece un recordatorio en el formato 'Hora:Minutos y tu acción'."""
    try:
        reminder_time = datetime.datetime.strptime(time, '%H:%M').time()
        user_id = ctx.author.id
        if user_id not in reminders:
            reminders[user_id] = []
        reminders[user_id].append((reminder_time, action))
        await ctx.send(f'Recordatorio para {time}: {action}')
    except ValueError:
        await ctx.send('Formato incorrecto, trata de poner Hora:Minutos y tu acción')

@tasks.loop(seconds=60)
async def check():
    now = datetime.datetime.now().time()
    for user_id, user_reminders in reminders.items():
        for reminder_time, action in user_reminders:
            if now.hour == reminder_time.hour and now.minute == reminder_time.minute:
                user = await bot.fetch_user(user_id)
                await user.send(f'Recuerda, {action}!')
                user_reminders.remove((reminder_time, action))


bot.run('TOKEN HERE/TOKEN AQUI')

#Credits to Yosemite Lizbeth and some random users from random forums LMAO 14-DEC-2024 11:02
