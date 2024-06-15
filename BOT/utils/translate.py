# BOT/utils/translate.py

import json
import random
import re
from urllib.parse import quote
import requests
import urllib3

# Disable warnings about insecure requests
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Define the list of Google Translate service URLs and a default suffix
DEFAULT_SERVICE_URLS = ["translate.google.com"]
URL_SUFFIX_DEFAULT = "com"

# Google Translate class
class GoogleTranslator:
    def __init__(self, url_suffix="com", timeout=5, proxies=None):
        self.proxies = proxies
        if url_suffix not in [re.search("translate.google.(.*)", url.strip()).group(1) for url in DEFAULT_SERVICE_URLS]:
            self.url_suffix = URL_SUFFIX_DEFAULT
        else:
            self.url_suffix = url_suffix
        self.url = f"https://translate.google.{self.url_suffix}/_/TranslateWebserverUi/data/batchexecute"
        self.timeout = timeout

    def _package_rpc(self, text, lang_src="auto", lang_tgt="auto"):
        GOOGLE_TTS_RPC = ["MkEWBc"]
        parameter = [[text.strip(), lang_src, lang_tgt, True], [1]]
        escaped_parameter = json.dumps(parameter, separators=(",", ":"))
        rpc = [[[random.choice(GOOGLE_TTS_RPC), escaped_parameter, None, "generic"]]]
        escaped_rpc = json.dumps(rpc, separators=(",", ":"))
        return f"f.req={quote(escaped_rpc)}&"

    def translate(self, text, lang_tgt="auto", lang_src="auto"):
        if len(text) >= 5000:
            return "Warning: Can only detect less than 5000 characters"
        if len(text) == 0:
            return ""
        
        headers = {
            "Referer": f"http://translate.google.{self.url_suffix}/",
            "User-Agent": "Mozilla/5.0",
            "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
        }
        freq = self._package_rpc(text, lang_src, lang_tgt)
        
        response = requests.Request(method="POST", url=self.url, data=freq, headers=headers)
        try:
            with requests.Session() as s:
                s.proxies = self.proxies if self.proxies else {}
                r = s.send(request=response.prepare(), verify=False, timeout=self.timeout)
                
            for line in r.iter_lines(chunk_size=1024):
                decoded_line = line.decode("utf-8")
                if "MkEWBc" in decoded_line:
                    response = json.loads(decoded_line)
                    response = json.loads(response[0][2])
                    sentences = response[1][0][0][5]
                    translated_text = " ".join([sentence[0] for sentence in sentences])
                    return translated_text
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error during translation request: {e}")

    def detect(self, text):
        headers = {
            "Referer": f"http://translate.google.{self.url_suffix}/",
            "User-Agent": "Mozilla/5.0",
            "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
        }
        freq = self._package_rpc(text)
        
        response = requests.Request(method="POST", url=self.url, data=freq, headers=headers)
        try:
            with requests.Session() as s:
                s.proxies = self.proxies if self.proxies else {}
                r = s.send(request=response.prepare(), verify=False, timeout=self.timeout)
                
            for line in r.iter_lines(chunk_size=1024):
                decoded_line = line.decode("utf-8")
                if "MkEWBc" in decoded_line:
                    response = json.loads(decoded_line)
                    response = json.loads(response[0][2])
                    detect_lang = response[0][2]
                    return detect_lang
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error during language detection: {e}")
