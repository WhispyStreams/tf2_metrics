from pandas import DataFrame
import numpy as np
from os import listdir, path

from logging import getLogger

log = getLogger(__name__)


def collect_matches(directory) -> DataFrame:
    #     data = DataFrame(columns=["season", "week", "logs"])
    data = []
    filenames = listdir(directory)
    for filename in filenames:
        current_season = None
        current_week = None
        playoff = False
        if "checkpoints" in filename:
            continue
        with open(f"{directory}/{filename}") as f:
            for line in f:
                if "finals" in line.lower() or "playoff" in line.lower():
                    playoff = True
                if "Season" in line:
                    current_season = _handle_season_line(line)
                    log.info(f"Season is now {current_season}")
                elif "Week" in line:
                    current_week = _handle_week_line(line)
                    log.info(f"Week is now {current_week}")
                elif "logs.tf" in line:
                    data.append(
                        _handle_log_line(line, current_season, current_week, playoff)
                    )
    return DataFrame(data)


def _handle_season_line(line):
    return int(line[-2])


def _handle_week_line(line):
    import re

    regex = r"Week (\d+)"
    return int(re.match(regex, line).group(1))


def _handle_log_line(line, current_season, current_week, playoff):
    import re

    regex = r"logs.tf\/(\d+)"
    logs = re.findall(regex, line)[0]
    # print(logs[0])
    row = {
        "season": current_season,
        "week": current_week,
        "playoff": playoff,
        "logs": int(logs),
    }
    return row

