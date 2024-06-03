# Achaea PowerBI scraper

This is an exploratory project that leverages Python requests and a bit of
meddling to retrieve Achaea kill data from the PowerBI leaderboard.

[Access the leaderboard from this link, created by Thaisen.](https://app.powerbi.com/view?r=eyJrIjoiMDdiNGM1YzEtNGIyNC00YmFjLWFkZjUtNmU2MDdkYzc4YjA1IiwidCI6IjlkMWIzNjEwLTlhYjAtNDJkNS05M2FhLTQ2MTUwZDcyM2Q4NyIsImMiOjF9)

## Setup

Clone repository and enter directory.

Create a python virtual environment, enter it, and install dependencies.

```sh
# Linux
python -m venv env
source env/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

Now you can use the tool.

## How to use

Run `get.py` without arguments to detail usage. Example output:

```
$ python get.py
Usage: python get.py <command>
Where command is one of:
       kdr - Fetch top fighters according to KDR
   victims - Fetch top victims
     kills - Fetch top killers
```

Example usage:

```
$ python get.py kdr | head
       Character          KDR   Kills  Deaths
       ---------          ---   -----  ------
   1 | Vinzent          4.718     184      39
   2 | Vothaec          4.650     479     103
   3 | Dalran           4.136     182      44
   4 | Kiryn            3.510     502     143
   5 | Dunn             3.190     689     216
   6 | Axios            2.683     585     218
   7 | Aegoth           2.640     623     236
   8 | Austere          2.589     321     124
```

## Development

This is a wobbly, hacked together solution for fun. In future, I may look into
developing a general use PowerBI dashboard scraping application (given a
PowerBI dashboard URL, scrape some subset of the data).

### Adding commands

The request data for each command (the data sent in the body of the POST
request that retrieves the data) is stored under the `data` directory.

These were retrieved from the PowerBI dashboard site using the Network tab of
Firefox's Developer Tools. Any request made to file "querydata" is a request
retrieving data to display on the dashboard. Upon selection the request and
response data is available as JSON. If we send the request data to the correct
URL with the right headers and request data, we get the same response data back
as the dashboard would.

Therefore, adding commands is as simple as fetching the request data from
Developer Tools, implementing a pretty printer for the data, and creating an
entry in the `commands` list as per the existing ones.

### TODO

* As of now, the data is all retrieved from one API endpoint:
  [https://wabi-us-east2-c-primary-api.analysis.windows.net/public/reports/querydata](https://wabi-us-east2-c-primary-api.analysis.windows.net/public/reports/querydata).
  There are presumably lots of mirrors around the world, which could be worth
  compiling and choosing from accordingly.
* I have no idea if the IDs hardcoded into the request data and headers will
  eventually expire or be blocked, which warrants investigation.
