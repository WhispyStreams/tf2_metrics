import requests


def get_match(matchid):
    if match_cached(matchid):
        return match_cache(matchid)
    return requests.get(f"http://logs.tf/json/{matchid}").json()


# TODO: Determine if a cache/storage mechanism is necessary/useful.
def match_cached(matchid):
    return False
