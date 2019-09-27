#!/usr/bin/python

import json
import os


class EndpointAdapter:
    def __init__(self):
        self.dir_path = os.path.dirname(os.path.realpath(__file__))

    def teams_endpoint(self):
        fn = "sample.teams.json"
        with open(self.dir_path + "/" + fn, "r") as f:
            return json.load(f)
