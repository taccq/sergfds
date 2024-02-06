import logging
import os
import json
from colorama import Fore
from TwitchChannelPointsMiner import TwitchChannelPointsMiner
from TwitchChannelPointsMiner.logger import LoggerSettings, ColorPalette
from TwitchChannelPointsMiner.classes.Chat import ChatPresence
from TwitchChannelPointsMiner.classes.Discord import Discord
from TwitchChannelPointsMiner.classes.Matrix import Matrix
from TwitchChannelPointsMiner.classes.Pushover import Pushover
from TwitchChannelPointsMiner.classes.Settings import Priority, Events, FollowersOrder
from TwitchChannelPointsMiner.classes.entities.Streamer import Streamer, StreamerSettings

from keep_alive import keep_alive

keep_alive()

# Função para carregar as credenciais do arquivo config.json
def carregar_credenciais():
    with open("config.json", "r") as arquivo_config:
        config_data = json.load(arquivo_config)
        return config_data["passw"], config_data["user"], config_data["webhook"]

# Carrega as credenciais
senha, usuario, webhook_url = carregar_credenciais()

twitch_miner = TwitchChannelPointsMiner(
  username=usuario,
  password=senha,
  claim_drops_startup=False,
  priority=[
    Priority.STREAK,
    Priority.DROPS,
    Priority.ORDER
  ],
  enable_analytics=False,
  disable_ssl_cert_verification=False,
  disable_at_in_nickname=False,
  logger_settings=LoggerSettings(
    save=True,
    console_level=logging.INFO,
    console_username=False,
    auto_clear=True,
    time_zone="America/Sao_Paulo",
    file_level=logging.DEBUG,
    emoji=True,
    less=True,
    colored=True,
    color_palette=ColorPalette(
      STREAMER_online="GREEN",
      streamer_offline="red",
      BET_wiN=Fore.MAGENTA
    ),
    discord=Discord(
      webhook_api=webhook_url,
      events=[
        Events.STREAMER_ONLINE, Events.STREAMER_OFFLINE, Events.BONUS_CLAIM,
        Events.GAIN_FOR_WATCH, Events.GAIN_FOR_CLAIM, Events.CHAT_MENTION
      ]
    )
  ),
  streamer_settings=StreamerSettings(
    make_predictions=True,
    follow_raid=True,
    claim_drops=True,
    watch_streak=True,
    chat=ChatPresence.ONLINE,
  )
)

#twitch_miner.analytics(host="127.0.0.1", port=5000, refresh=5, days_ago=7)

twitch_miner.mine([
  Streamer("eimine77",
           settings=StreamerSettings(make_predictions=True,
                                     follow_raid=True,
                                     claim_drops=True,
                                     watch_streak=True)),
  Streamer("eimine24h",
           settings=StreamerSettings(
             make_predictions=True,
             follow_raid=True,
             claim_drops=True,
             watch_streak=True))
],
                  followers=False,
                  followers_order=FollowersOrder.ASC)
