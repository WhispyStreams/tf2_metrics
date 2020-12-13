from dataclasses import dataclass
import json
from logging import getLogger
from os import path
from types import SimpleNamespace
from typing import List, Dict, Union, Optional

import requests

log = getLogger(__name__)


def get_match(matchid):
    return requests.get(f"http://logs.tf/json/{matchid}").json()


def _get_file_path(matchid, directory):
    return f"{directory}/{matchid}.json"


def get_log(matchid, directory="log_json", save_locally=True, indent=4):
    filepath = _get_file_path(matchid, directory)
    if path.exists(filepath):
        with open(filepath) as f:
            log_json = json.load(f)
            return Log(matchid, log_json, **log_json)
    json_log = get_match(matchid)
    if save_locally:
        with open(filepath, "w") as f:
            json.dump(json_log, f, indent=indent)
    return Log(matchid, json_log, **json_log)


@dataclass
class Event:
    type: str


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


@dataclass
class Drop(Event):
    time: int
    team: str
    steamid: str


event_types = {
    "pointcap": Pointcap,
    "charge": Charge,
    "medic_death": MedicDeath,
    "round_win": RoundWin,
    "drop": Drop,
}


@dataclass
class Team:
    color: str
    score: int
    kills: int
    dmg: int
    ubers: Optional[int] = None
    deaths: Optional[int] = None
    charges: Optional[int] = None
    drops: Optional[int] = None
    firstcaps: Optional[int] = None
    caps: Optional[int] = None


@dataclass
class Weapon:
    name: str
    kills: int
    dmg: int
    avg_dmg: float
    shots: int
    hits: int


@dataclass
class ClassStat:
    type: str
    kills: int
    assists: int
    deaths: int
    dmg: int
    weapon: Dict[str, Weapon]
    total_time: int

    def __post_init__(self):
        for weapon_name, weapon in self.weapon.items():
            if not isinstance(weapon, Weapon):
                self.weapon[weapon_name] = Weapon(weapon_name, **weapon)


@dataclass
class MedicStats:
    advantages_lost: int
    biggest_advantage_lost: int
    avg_time_to_build: int
    avg_time_before_using: Optional[int] = None
    avg_uber_length: Optional[int] = None
    deaths_with_95_99_uber: Optional[int] = None
    avg_time_before_healing: Optional[int] = None
    deaths_within_20s_after_uber: Optional[int] = None


@dataclass
class Player:
    steamid: str
    team: str
    kills: int
    dmg: int
    class_stats: List[ClassStat] = None
    deaths: Optional[int] = None
    assists: Optional[int] = None
    suicides: Optional[int] = None
    kapd: Optional[float] = None
    kpd: Optional[float] = None
    dmg_real: Optional[int] = None
    dt: Optional[int] = None
    dt_real: Optional[int] = None
    hr: Optional[int] = None
    lks: Optional[int] = None
    as_: Optional[int] = None
    dapd: Optional[int] = None
    dapm: Optional[int] = None
    ubers: Optional[int] = None
    ubertypes: Dict[str, int] = None
    drops: Optional[int] = None
    medkits: Optional[int] = None
    medkits_hp: Optional[int] = None
    backstabs: Optional[int] = None
    headshots: Optional[int] = None
    headshots_hit: Optional[int] = None
    sentries: Optional[int] = None
    heal: Optional[int] = None
    cpc: Optional[int] = None
    ic: Optional[int] = None
    medicstats: Optional[MedicStats] = None

    def __post_init__(self):
        self.class_stats = [
            ClassStat(**class_stat)
            if not isinstance(class_stat, ClassStat)
            else class_stat
            for class_stat in self.class_stats
        ]
        for class_stat in self.class_stats:
            if not isinstance(class_stat, ClassStat):
                self.class_stats = ClassStat(**self.class_stats)
        if self.medicstats and not isinstance(self.medicstats, MedicStats):
            self.medicstats = MedicStats(**self.medicstats)


@dataclass
class Teams:
    red: Team
    blue: Team

    def __iter__(self):
        return [self.red, self.blue]


@dataclass
class Round:
    start_time: int
    winner: Team
    team: Teams
    events: List[Union[Event, Pointcap, Charge, MedicDeath, RoundWin]]
    players: Dict[str, Player]
    firstcap: str
    length: int

    def __post_init__(self):
        self.events = [
            event_types[event["type"]](**event)
            if not isinstance(
                event, tuple(event_type for _, event_type in event_types.items())
            )
            else event
            for event in self.events
        ]


@dataclass
class Message:
    steamid: str
    name: str
    msg: str


@dataclass
class Uploader:
    id: int
    name: str
    info: str


@dataclass
class Info:
    map: str
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
    hasAS: bool
    hasHR: bool
    hasIntel: bool
    AD_scoring: bool
    notifications: List
    title: str
    date: int
    uploader: Uploader

    def __post_init__(self):
        if isinstance(self.uploader, Uploader):
            return
        self.uploader = Uploader(**self.uploader)


@dataclass
class Killstreak:
    steamid: str
    streak: int
    time: int


@dataclass
class Log:
    matchid: int
    json: Dict
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

    def __post_init__(self):
        log.info(f"Post processing Log instantiation for {self.matchid}...")
        log.info("Handling player dictionaries...")
        for steamid, player in self.players.items():
            if not isinstance(player, Player):
                player = dict(player)
                player["as_"] = player["as"]
                del player["as"]
                self.players[steamid] = Player(steamid, **player)
        log.info("Handling rounds...")
        self.rounds = [
            Round(**round) if not isinstance(round, Round) else round
            for round in self.rounds
        ]
        log.info("Handling chat...")
        self.chat = [
            Message(**message) if not isinstance(message, Message) else message
            for message in self.chat
        ]
        log.info("Handling info...")
        if not isinstance(self.info, Info):
            self.info = Info(**self.info)
        log.info("Handling killstreaks...")
        self.killstreaks = [
            Killstreak(**ks) if not isinstance(ks, Killstreak) else ks
            for ks in self.killstreaks
        ]


def generate_teams(teams):
    red = None
    blue = None
    for team_color, team_data in teams.items():
        if team_color == "Red":
            red = Team(color=team_color, **team_data)
        elif team_color == "Blue":
            blue = Team(color=team_color, **team_data)
        else:
            log.warning(f"Invalid team {team_color} present in teams data.")
    if not (red and blue):
        raise ValueError("Red and Blue teams not present in teams data.")
    return Teams(red, blue)


def generate_players(players_d):
    players = {}
    for steamid, player_d in players_d.items():
        players[steamid] = Player(class_stats=Player(**player_d))


def generate_log(json_log, matchid):
    return Log(matchid=matchid, **json_log)


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
