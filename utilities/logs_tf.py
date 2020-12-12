from dataclasses import dataclass

from types import SimpleNamespace
from typing import List

import requests


def get_match(matchid):
    if match_cached(matchid):
        return match_cache(matchid)
    return requests.get(f"http://logs.tf/json/{matchid}").json()


@dataclass
class Team:
    color: str
    score: int
    kills: int
    deaths: int
    dmg: int
    charges: int
    drops: int
    firstcaps: int
    caps: int


@dataclass
class Log:
    matchid: int
    version: str
    teams: List[Team]


def download_log_zip(matchid):
    from zipfile import ZipFile
    from io import BytesIO

    zip_request = requests.get(f"https://logs.tf/logs/log_{matchid}.log.zip")

    # with open(filepath, "wb") as f:
    #     f.write(zip_request.content)

    # matchzip = ZipFile(filepath)

    match_zip = ZipFile(BytesIO(zip_request.content))

    return match_zip


# TODO: Determine if a cache/storage mechanism is necessary/useful.
def match_cached(matchid):
    return False


def match_cache(matchid):
    raise NotImplementedError("Match cache not implemented.")
