#!/usr/bin/env python

import logging
from typing import Dict, List
import typing
from uuid import uuid4
from thefuzz import process
from json import load
from random import choices

from telegram import InlineQueryResultArticle, InputTextMessageContent, Update
from telegram.ext import Updater, InlineQueryHandler, CommandHandler, CallbackContext
from telegram.utils.helpers import escape_markdown

import scraper

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hey there!')


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')

def inlinequeryhandlergenerator(kaomoji: Dict) -> typing.Callable:
    def inlinequery(update: Update, context: CallbackContext) -> None:
        query = update.inline_query.query

        if query == "":
            return
            # return [InlineQueryResultArticle(
            #     id=str(uuid4()),
            #     title=' '+key,
            #     input_message_content=' ',
            # ) for key in kaomoji.keys()]

        category = process.extractOne(query, kaomoji.keys())[0]

        results = [InlineQueryResultArticle(
                id=str(uuid4()),
                title=' '+category,
                input_message_content=InputTextMessageContent(category),
            )]

        kaomoji_in_category = kaomoji[category] if len(kaomoji[category]) < 50 else \
            choices(kaomoji[category], k=49)

        results = results + [
            InlineQueryResultArticle(
                id=str(uuid4()),
                title=' '+item,
                input_message_content=InputTextMessageContent(item),
            ) for item in kaomoji_in_category
        ]

        update.inline_query.answer(results)

    return inlinequery

def main() -> None:
    with open('secret.json', 'r') as secret:
        creds = load(secret)

    kaomoji = scraper.enrich_downloaded_dict('kaomoji.json', scraper.scrape())

    updater = Updater(creds['key'])
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    dispatcher.add_handler(InlineQueryHandler(inlinequeryhandlergenerator(kaomoji)))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()