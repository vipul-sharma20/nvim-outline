import os
import sys


file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

import pynvim
import requests


@pynvim.plugin
class Outline(object):
    def __init__(self, nvim):
        self.nvim = nvim
        self.outline_host = os.getenv("OUTLINE_HOST")
        self.outline_token = os.getenv("OUTLINE_TOKEN")
        self.cache = {}

    @pynvim.function("OutlineSearch", sync=True)
    def outline_search(self, args):
        url = self.outline_host + "/api/documents.search"
        headers = {"Authorization": f"Bearer {self.outline_token}"}
        payload = {"query": args[0]}

        response = requests.post(url, json=payload, headers=headers)

        if response.ok:
            data = response.json()
            titles = []
            for item in data["data"]:
                self.cache[item["document"]["id"]] = item["document"]["text"]
                titles.append(item["document"]["title"] + " | " + item["document"]["id"])

            return titles
        return ["test"]

    @pynvim.function("OutlineSelect", sync=True)
    def outline_select(self, args):
        doc_id = args[0].split("|")[1].strip()

        buf = self.nvim.current.buffer
        lines = self.cache[doc_id].split('\n')
        buf[:] = lines

