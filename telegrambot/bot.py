from gettext import gettext as _
import os
import logging
import configparser

from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import Updater, CommandHandler, InlineQueryHandler, MessageHandler, Filters
from telegram.error import TelegramError

CONFIGFILE_PATH = "data/config.cfg"
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("bot_log")

class Bot(object):
    translations = {}
    bot = None

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read( CONFIGFILE_PATH )

        self.updater = Updater(token=self.get_bot_conf("TOKEN"))
        self.dispatcher = self.updater.dispatcher
        self.add_handlers()

    def get_bot_conf(self, value):
        return self.config["bot"][value]

    def get_env_conf(self, value, default_value=None):
        if default_value:
            return os.environ.get(self.config["env"][value], default_value)
        else:
            return os.environ.get(self.config["env"][value])

    def start_polling_loop(self):
        self.disable_webhook()
        self.update_queue = self.updater.start_polling()
        self.updater.idle()
        self.cleaning()

    def start_webhook_server(self):
        self.set_webhook()
        self.update_queue = self.updater.start_webhook(self.get_env_conf("IP","127.0.0.1"),
                                                       int(self.get_env_conf("PORT","8080")),
                                                       self.get_bot_conf("TOKEN"))
        self.updater.idle()
        self.cleaning()

    def cleaning(self):
        logger.info("Finished program.")

    def set_webhook(self):
        s = self.updater.bot.setWebhook(self.get_bot_conf("WEBHOOK_URL") + "/" + self.get_bot_conf("TOKEN"))
        if s:
            logger.info("webhook setup worked")
        else:
            logger.warning("webhook setup failed")
        return s

    def disable_webhook(self):
        s = self.updater.bot.setWebhook("")
        if s:
            logger.info("webhook was disabled")
        else:
            logger.warning("webhook couldn't be disabled")
        return s

    def add_handlers(self):
        self.dispatcher.add_handler(CommandHandler("start", self.command_help))
        self.dispatcher.add_handler(CommandHandler("help", self.command_help))
        self.dispatcher.add_handler(MessageHandler([Filters.text], self.command_help))
        self.dispatcher.add_handler(InlineQueryHandler(self.inlinequery))
        #self.dispatcher.addErrorHandler(self.error_handle)


    def inlinequery(self, bot, update):
        query = update.inline_query.query
        results = list()

        results.append(InlineQueryResultArticle(id="this id is retrieved from EDICT",
                                                title=query,
                                                input_message_content=InputTextMessageContent(
                                                "%s was not found in the dictionary" % query)))

        bot.answerInlineQuery(update.inline_query.id, results=results)

    def command_help(self, bot, update):
        self.send_message(bot, update.message.chat, _("Welcome to the Japanese-English Dictionary Bot.\n"
                                                      "This bot is created for being used inline and it is global. \n"
                                                      "You can call him in any chat with @jdict_bot\n"
                                                      "Examples: \n"
                                                      "\t\t\t@jdict_bot dog\n"
                                                      "\t\t\t@jdict_bot 犬"))

    def send_message(self, bot, chat, text):
        try:
            bot.sendMessage(chat_id=chat.id, text=text)
            return True
        except TelegramError as e:
            logger.warning("Message sending error to %s [%d] [%s] (TelegramError: %s)" % (chat.name, chat.id, chat.type, e))
            return False
        except:
            logger.warning("Message sending error to %s [%d] [%s]" % (chat.name, chat.id, chat.type))
            return False
