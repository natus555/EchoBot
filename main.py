import discord
import asyncio
from discord.ext import commands
import openai

openai.api_key = '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'


intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)
gpt3_channel_id = 1096068620754366464

@bot.event
async def on_message(message):
    global gpt3_channel_id
    if gpt3_channel_id:
        if message.channel.id == int(gpt3_channel_id) and message.author !=bot.user:
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=message.content,
                temperature=0.33,
                max_tokens=1000,
                presence_penalty=0,
                frequency_penalty=0,
                best_of=2,
            )
            bot_response = response.choices[0].text.strip()
            await message.channel.send(bot_response)

  
    if message.content.startswith("!remindme"):

        command_parts = message.content.split(" ")
        if len(command_parts) < 3:
            await message.channel.send("Invalid format! Please use !remindme (duration) (reminder)")
            return
        duration = command_parts[1]
        reminder = " ".join(command_parts[2:])
        
        unit = duration[-1]
        if unit == "s":
            time_seconds = int(duration[:-1])
        elif unit == "m":
            time_seconds = int(duration[:-1]) * 60
        elif unit == "h":
            time_seconds = int(duration[:-1]) * 3600
        elif unit == "d":
            time_seconds = int(duration[:-1]) * 86400
        else:
            await message.channel.send("Invalid time unit. Please use s (seconds), m (minutes), h (hours), or d (days).")
            return
          
        await message.channel.send(f"{message.author.mention}, your reminder has been set!")
        await asyncio.sleep(time_seconds)
        await message.channel.send(f"**Reminder:** {reminder} - {message.author.mention}")
    await bot.process_commands(message)

        
bot.run('token')