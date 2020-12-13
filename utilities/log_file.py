import os

R_TIME = r"(?P<month>\d+)\/(?P<day>\d+)\/(?P<year>\d+) - (?P<hour>\d+):(?P<minute>\d+):(?P<second>\d+): "
R_PLAYER = r'"(?P<username>.*?)<(?P<userid>\d+)><(?P<steamid>\[U:\d:\d+\])><(?P<team>Red|Blue)>"'
