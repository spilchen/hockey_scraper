#!/usr/bin/python

import objectpath
import requests
import json
import pandas as pd


class EndpointAdapter:
    NHL_ENDPOINT = "https://statsapi.web.nhl.com/api/v1"

    def get(self, api):
        """Send an API request to the URI and return the response as JSON

        :param api: API to call
        :type uri: str
        :return: JSON document of the reponse
        :raises: RuntimeError if any response comes back with an error
        """
        response = requests.get("{}/{}".format(self.NHL_ENDPOINT, api),
                                params={'format': 'json'})
        jresp = response.json()
        if "error" in jresp:
            raise RuntimeError(json.dumps(jresp))
        return jresp

    def teams_endpoint(self):
        return self.get("teams")


class Scraper:
    def __init__(self):
        self.ea = EndpointAdapter()
        self.teams_cache = None

    def set_endpoint_adapter(self, ea):
        self.ea = ea

    def teams(self):
        """Get list of teams in the NHL

        :return: Team details
        :rtype: pandas.DataFrame

        >>> s.teams()
        id            name          city abbrev
        0    1          Devils    New Jersey    NJD
        1    2       Islanders      New York    NYI
        2    3         Rangers      New York    NYR
        3    4          Flyers  Philadelphia    PHI
        4    5        Penguins    Pittsburgh    PIT
        5    6          Bruins        Boston    BOS
        6    7          Sabres       Buffalo    BUF
        7    8       Canadiens      Montréal    MTL
        8    9        Senators        Ottawa    OTT
        9   10     Maple Leafs       Toronto    TOR
        10  12      Hurricanes      Carolina    CAR
        11  13        Panthers       Florida    FLA
        12  14       Lightning     Tampa Bay    TBL
        13  15        Capitals    Washington    WSH
        14  16      Blackhawks       Chicago    CHI
        15  17       Red Wings       Detroit    DET
        16  18       Predators     Nashville    NSH
        17  19           Blues     St. Louis    STL
        18  20          Flames       Calgary    CGY
        19  21       Avalanche      Colorado    COL
        20  22          Oilers      Edmonton    EDM
        21  23         Canucks     Vancouver    VAN
        22  24           Ducks       Anaheim    ANA
        23  25           Stars        Dallas    DAL
        24  26           Kings   Los Angeles    LAK
        25  28          Sharks      San Jose    SJS
        26  29    Blue Jackets      Columbus    CBJ
        27  30            Wild     Minnesota    MIN
        28  52            Jets      Winnipeg    WPG
        29  53         Coyotes       Arizona    ARI
        30  54  Golden Knights         Vegas    VGK
        """
        if self.teams_cache is None:
            r = self.ea.teams_endpoint()
            t = objectpath.Tree(r)
            colmap = {"id": "id", "teamName": "name", "locationName": "city",
                      "abbreviation": "abbrev"}
            path = "$..teams.({})".format(",".join(colmap.keys()))
            data = t.execute(path)
            self.teams_cache = pd.DataFrame(data=data, columns=colmap.keys())
            self.teams_cache = self.teams_cache.rename(columns=colmap)
        return self.teams_cache
