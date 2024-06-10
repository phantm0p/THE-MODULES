# BOT/features/telegraph.py

from telegraph import Telegraph
import os

class TeleClient:
    def __init__(self):
        self.telegraph = Telegraph()
        self.telegraph.create_account(short_name='1337')

    def upload_image(self, file_path):
        response = self.telegraph.upload_file(file_path)
        return "https://telegra.ph" + response[0]["src"]

# Initialize Telegraph Client
telegraph_client = TeleClient()
