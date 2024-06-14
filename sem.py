from tokens_tg import TG_TOKEN
from bs4 import BeautifulSoup as BSoup
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, ContextTypes

import requests
import aiohttp
import numpy as np


reply_keyboard = [['/help', '/start'],
                      ['/spell', '/class'],
                      ['/race', '/roll']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

async def get_response(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return await resp.json()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Здравствуйте, чем я могу вам помочь?", reply_markup=markup)


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Use /start to test this bot.", reply_markup=markup)


async def spell(update, context):
    url = "https://www.dnd5eapi.co/api/spells"
    text = ' '.join(context.args)
    if text:
        text_response = url + '/' + '-'.join(context.args)
        response = await get_response(text_response)
        result = [f"{key}: {response[key]}" for key in response.keys()]
        await update.message.reply_text('\n'.join(result))
    else:
        random_id = np.random.randint(319)
        response = await get_response(url)
        spell = response['results'][random_id]
        result = [f"{key}: {spell[key]}" for key in spell.keys()]
        await update.message.reply_text('\n'.join(result))

async def race(update, context):
    url = "https://www.dnd5eapi.co/api/races"
    text = ' '.join(context.args)
    if text:
        text_response = url + '/' + '-'.join(context.args)
        response = await get_response(text_response)
        result = [f"{key}: {response[key]}" for key in response.keys()]
        await update.message.reply_text('\n'.join(result))
    else:
        random_id = np.random.randint(9)
        response = await get_response(url)
        race = response['results'][random_id]
        result = [f"{key}: {race[key]}" for key in race.keys()]
        await update.message.reply_text('\n'.join(result))


async def comand_class(update, context):
    url = "https://www.dnd5eapi.co/api/classes"
    text = ' '.join(context.args)
    if text:
        text_response = url + '/' + '-'.join(context.args)
        response = await get_response(text_response)
        result = [f"{key}: {response[key]}" for key in list(response.keys())[:3]] \
            + [response['proficiency_choices'][0]['desc']]
        await update.message.reply_text('\n'.join(result))
    else:
        random_id = np.random.randint(12)
        response = await get_response(url)
        clas = response['results'][random_id]
        result = [f"{key}: {clas[key]}" for key in clas.keys()]
        await update.message.reply_text('\n'.join(result))


async def roll(update, context):
    d = ' '.join(context.args)
    match d:
        case 'd4':
            await update.message.reply_text(np.random.randint(1, 5))
        case 'd6':
            await update.message.reply_text(np.random.randint(1, 7))
        case 'd8':
            await update.message.reply_text(np.random.randint(1, 9))
        case 'd10':
            await update.message.reply_text(np.random.randint(1, 11))
        case 'd12':
            await update.message.reply_text(np.random.randint(1, 13))
        case 'd20':
            await update.message.reply_text(np.random.randint(1, 21))
        case 'd100' | 'd%':
            await update.message.reply_text(np.random.randint(1, 101))
        case _:
            await update.message.reply_text(np.random.randint(2))


async def how_start(update, context):
    src = requests.get("https://www.dnd.su/articles/mechanics/536-how_to_start_playing_d_d/")
    soup = BSoup(src.text, "lxml")
    article = ''.join([x.text.strip() for x in soup.find_all("p")])
    msgs = [article[i:i + 4096] for i in range(0, len(article), 4096)]
    for msg in msgs:
        await update.message.reply_text(msg)


def main() -> None:
    application = Application.builder().token(TG_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("spell", spell))
    application.add_handler(CommandHandler("race", race))
    application.add_handler(CommandHandler("class", comand_class))
    application.add_handler(CommandHandler("roll", roll))
    application.add_handler(CommandHandler("howstart", how_start))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()