from dataclasses import dataclass

from types import SimpleNamespace
from typing import List, Dict, Union

import requests


def get_match(matchid):
    if match_cached(matchid):
        return match_cache(matchid)
    return requests.get(f"http://logs.tf/json/{matchid}").json()


@dataclass
class Event:
    type_: str


@dataclass
class Pointcap(Event):
    time: int
    team: str
    point: int


@dataclass
class Charge(Event):
    medigun: str
    time: int
    steamid: str
    team: str


@dataclass
class MedicDeath(Event):
    time: int
    team: str
    steamid: str
    killer: str


@dataclass
class RoundWin(Event):
    time: int
    team: str


event_types = {
    "pointcap": Pointcap,
    "charge": Charge,
    "medic_death": MedicDeath,
    "round_win": RoundWin,
}


@dataclass
class Team:
    color: str
    score: int
    kills: int
    dmg: int
    ubers: int = None
    deaths: int = None
    charges: int = None
    drops: int = None
    firstcaps: int = None
    caps: int = None


@dataclass
class Player:
    steamid: str
    team: str
    kills: int
    dmg: int
    class_stats: Team = None
    deaths: int = None
    assists: int = None
    suicides: int = None
    kapd: float = None
    kpd: float = None
    dmg_real: int = None
    dt: int = None
    dt_real: int = None
    hr: int = None
    lks: int = None
    as_: int = None
    dapd: int = None
    medkits: int = None
    medkints_hp: int = None
    backstabs: int = None
    headshots: int = None
    headshots_hit: int = None
    sentries: int = None
    heal: int = None
    cpc: int = None
    ic: int = None


@dataclass
class Teams:
    red: Team
    blu: Team

    def __iter__(self):
        return [self.red, self.blu]


@dataclass
class Round:
    start_time: int
    winner: Team
    team: Teams
    events: List[Union[Event, Pointcap, Charge, MedicDeath, RoundWin]]
    players: Dict[str, Player]
    firstcap: str
    length: int


@dataclass
class Weapon:
    name: str
    kills: int
    dmg: int
    avg_dmg: float
    shots: int
    hits: int


@dataclass
class class_stats:
    type_: str
    kills: int
    assists: int
    deaths: int
    dmg: int
    weapon: Dict[str, Weapon]
    total_time: int


@dataclass
class Message:
    steamid: str
    name: str
    msg: str


@dataclass
class Uploader:
    id_: int
    name: str
    info: str


@dataclass
class Info:
    map_: str
    supplemental: bool
    total_length: int
    hasRealDamage: bool
    hasWeaponDamage: bool
    hasAccuracy: bool
    hasHP: bool
    hasHP_real: bool
    hasHS: bool
    hasHS_hit: bool
    hasBS: bool
    hasCP: bool
    hasSB: bool
    hasDT: bool
    hasAR: bool
    hasIntel: bool
    AD_scoring: bool
    notifications: List
    title: str
    date: int
    uploader: Uploader


@dataclass
class Killstreak:
    steamid: str
    streak: int
    time: int


@dataclass
class Log:
    matchid: int
    version: str
    teams: Teams
    length: int
    players: Dict[str, Player]
    names: Dict[str, str]
    rounds: List[Round]
    healspread: Dict[str, Dict[str, int]]
    classkills: Dict[str, Dict[str, int]]
    classdeaths: Dict[str, Dict[str, int]]
    classkillassists: Dict[str, Dict[str, int]]
    chat: List[Message]
    info: Info
    killstreaks: List[Killstreak]
    success: bool


def download_log_zip(matchid):
    from zipfile import ZipFile
    from io import BytesIO

    zip_request = requests.get(f"https://logs.tf/logs/log_{matchid}.log.zip")

    # with open(filepath, "wb") as f:
    #     f.write(zip_request.content)

    # matchzip = ZipFile(filepath)

    match_zip = ZipFile(BytesIO(zip_request.content))

    return match_zip


def generate_match_log_file_path(season, week, playoff, matchid, part=0):
    return f"logs/season_{season}_week_{week}_playoff_{int(playoff)}_id_{matchid}_part_{part}.log"


# TODO: Determine if a cache/storage mechanism is necessary/useful.
def match_cached(matchid):
    return False


def match_cache(matchid):
    raise NotImplementedError("Match cache not implemented.")


# TODO: Clean up magic string for directory path
def get_file_path(matchid):
    return f"logs/log_{2114329}.log"
