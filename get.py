import requests
import json
from sys import argv
from os.path import join

# Headers for the request
HEADERS = {
    "Host": "wabi-us-east2-c-primary-api.analysis.windows.net",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:126.0) Gecko/20100101 Firefox/126.0",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "ActivityId": "02d2eca7-8dc1-f611-8ca7-ecf992e98f10",
    "RequestId": "6a47d565-aafc-2b1e-0d9c-0757ae529ce3",
    "X-PowerBI-ResourceKey": "07b4c5c1-4b24-4bac-adf5-6e607dc78b05",
    "Content-Type": "application/json;charset=UTF-8",
    "Content-Length": "6911",
    "Origin": "https://app.powerbi.com",
    "DNT": "1",
    "Sec-GPC": "1",
    "Connection": "keep-alive",
    "Referer": "https://app.powerbi.com/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "cross-site",
}

def get_query_result(data):
    """Extract the query result from the data.

    Bit of a hack, clearly. `item` will point to a dictionary with the desired
    value under the first key, but that key name is different e.g. for KDR vs
    Kills.
    """
    item = data["results"][0]["result"]["data"]["dsr"]["DS"][0]["PH"][0]
    return next(iter(item.values()))

def print_kdr(query):
    """Pretty print KDR data."""
    print("       %-14s%8s%8s%8s" % ("Character", "KDR", "Kills", "Deaths"))
    print("       %-14s%8s%8s%8s" % ("---------", "---", "-----", "------"))
    for entry in query:
        try:
            [char, kdr, kills, deaths, rank] = entry["C"]
            print("%4d | %-14s%8.3f%8d%8d" % (rank, char, float(kdr), kills, deaths))
        except ValueError:
            # Compensate for the empty name ("") killer, whose kills obviously
            # don't count
            pass

def print_victims(query):
    """Pretty print victim data."""
    last = (0, 0)
    print("       %-14s%8s" % ("Character", "Deaths"))
    print("       %-14s%8s" % ("---------", "------"))
    for entry in query:
        if "R" in entry:
            # This signifies that the character has the same number of deaths as
            # the last
            [char] = entry["C"]
            rank, deaths = last
        else:
            [char, rank, deaths] = entry["C"]
            last = rank, deaths
        print("%4d | %-14s%8d" % (rank, char, deaths))

def print_kills(query):
    """Pretty print kill data."""
    last = (0, 0)
    print("       %-14s%8s" % ("Character", "Kills"))
    print("       %-14s%8s" % ("---------", "-----"))
    for entry in query:
        if "R" in entry:
            # This signifies that the character has the same number of deaths as
            # the last
            [char] = entry["C"]
            rank, kills = last
        else:
            [char, kills, rank] = entry["C"]
            last = rank, kills
        print("%4d | %-14s%8d" % (rank, char, kills))

if __name__ == "__main__":
    commands = {
        "kdr": (
            "Fetch top players and their KDR",
            "kdr_request.json",
            print_kdr,
        ),
        "victims": (
            "Fetch top victims",
            "victim_request.json",
            print_victims
        ),
        "kills": (
            "Fetch top killers",
            "kills_request.json",
            print_kills
        ),
    }

    if len(argv) < 2 or argv[1] not in commands:
        print("Usage: python get.py <command>")
        print("Where command is one of:")
        for cmd, help in commands.items():
            print("  %8s - %s" % (cmd, help[0]))
        exit(1)
    else:
        _, request_data_file, pretty_printer = commands[argv[1]]

    filename = join("data", request_data_file)
    try:
        f = open(filename)
        request_data = json.load(f)
        f.close()
    except FileNotFoundError:
        print(f"Error: Request file not found: {filename}")
        exit(1)

    try:
        r = requests.Response = requests.post(
            url="https://wabi-us-east2-c-primary-api.analysis.windows.net/public/reports/querydata?synchronous=true",
            json=request_data,
            headers=HEADERS,
        )
    except requests.RequestException as e:
        print(f"Error: Retrieving from API failed: {e}")
        exit(1)

    if r.status_code != 200:
        print("Error: Request failed with status code {r.status_code}")
        exit(1)

    if "--raw" in argv:
        print(r.text)
        exit(0)

    data = r.json()
    item = get_query_result(data)
    pretty_printer(item)
