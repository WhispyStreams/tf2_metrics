# tf2_metrics
## Python Setup
### Clone the repo
`git clone git@github.com:WhispyStreams/tf2_metrics.git`
### Conda
If using conda, create the tf2_metrics environment using the environment yaml file. You will want conda for python 3.

`cd tf2_metrics`

`conda create -f environment.yml`

Activate your environment: `conda activate tf2_metrics`

## Notebook Usage
It's pretty quick to start playing with python.

`cd tf2_metrics`

`jupyter-lab`

This will open up jupyter lab on your default browser. You can also use vscode or pycharm professional to view notebooks.

In jupyter lab, open up log_collection.ipynb. This is an **I**nteractive **Py**thon **N**ote**b**ook.

# Utilities
## logs_tf
This module contains a collection of object definitions and methods related to "Logs" as we view them as players, typically referring to `logs.tf`.

### Usage
```python
from utilities.logs_tf import get_match, download_match_zip, get_file_path

matchid = 12345

log_json = get_match(matchid)
print(log_json["version"])

log_zip = download_match_zip
log_zip.extractall("logs")

with open(get_file_path(matchid)) as lf:
    log_line = lf.readline()
    print(log_line)
    
    for line in lf:
        magically_parse_log_lines(line)
```

## match_directory
This module contains methods related to the match directory files shared by requiescas, located in the match_directory folder.
This dataset is not complete.

### Usage
```python
from utilities.match_directory import collect_matches

matches = collect_matches("match_directory")
for index, match in matches.iterrows():
    log_zip = download_match_zip(match.logs)
    log_zip.extractall("logs")

season_7_matches = matches[matches.season == 7]
```
