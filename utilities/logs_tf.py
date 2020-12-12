from dataclasses import dataclass

from types import SimpleNamespace
from typing import List

import requests


def get_match(matchid):
    if match_cached(matchid):
        return match_cache(matchid)
    return requests.get(f"http://logs.tf/json/{matchid}").json(
        object_hook=lambda d: [] if "players" in d else SimpleNamespace(**d)
    )


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
    version: str
    teams: List[Team]


# TODO: Determine if a cache/storage mechanism is necessary/useful.
def match_cached(matchid):
    return False


def match_cache(matchid):
    raise NotImplementedError("Match cache not implemented.")
