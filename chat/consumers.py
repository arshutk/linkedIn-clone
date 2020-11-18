
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json

from asgiref.sync import async_to_sync
from channels.consumer import SyncConsumer
from json.decoder import JSONDecodeError as e


class ChatConsumer(WebsocketConsumer):
    pass