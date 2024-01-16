import itertools
import json
from pathlib import Path

import urllib3

# Downloading the .json file from the GitHub repository
url = "https://raw.githubusercontent.com/kiibo382/bigquery-functions/main/output/function_names_by_category.json"
http = urllib3.PoolManager()
response = http.request("GET", url)
content = response.data.decode("utf-8")
function_names_by_category: dict[str, list[str]] = json.loads(content)

aggregators = sorted(function_names_by_category["Aggregate"])
del function_names_by_category["Aggregate"]
functions = sorted(list(itertools.chain(*function_names_by_category.values())))

# Overwrite file in ../src/harlequin_bigquery/functions.py
# creating it if it doesn't exist
# and write the keys_unique list to it
path = Path(__file__).parents[1] / "src" / "harlequin_bigquery" / "functions.py"
prefix = "# Autogenerated using `scripts/parse_builtins.py`\n\n"

with path.open("w+") as file:
    file.write(
        prefix + f"AGGREGATE_FUNCTIONS = {json.dumps(aggregators, indent=4)}\n\n"
    )
    file.write(f"BUILTIN_FUNCTIONS = {json.dumps(functions, indent=4)}\n")
