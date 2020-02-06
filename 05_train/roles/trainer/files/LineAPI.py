#!/usr/bin/env python3

import sys
import requests
import os

class LineAPI:
    API_URL = 'https://notify-api.line.me/api/notify'
    def __init__(self, access_token):
        self.__headers = {'Authorization': 'Bearer ' + access_token}

    def send(self, message, image=None, sticker_package_id=None, sticker_id=None,):
        payload = {
            'message': message,
            'stickerPackageId': sticker_package_id,
            'stickerId': sticker_id,
            }

        files = {}
        if image != None:
            files = {'imageFile': open(image, 'rb')}

        r = requests.post(
            LineAPI.API_URL,
            headers=self.__headers,
            data=payload,
            files=files,
            )

if __name__ == "__main__":
    args = sys.argv

    if len(args) != 2:
        print("usage: LineAPI.py <message>")
        exit()

    line = LineAPI(access_token=os.environ.get('UMA_LINE_ACCESSTOKEN'))
    line.send(args[1])
