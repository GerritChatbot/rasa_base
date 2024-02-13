from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport
from datetime import date, datetime, timedelta
# https://pypi.org/project/jq/
# https://pypi.org/project/pyjq/
import json
import os.path as path
from dateutil.parser import parse
import pytz

# Select your transport with a defined url endpoint
header = {'x-tumi-tenant': 'cu-prague'}
transport = AIOHTTPTransport(url="https://cu-prague.esn.world/graphql", headers=header)

# Create a GraphQL client using the defined transport
client = Client(transport=transport, fetch_schema_from_transport=True)

prague_tz = pytz.timezone('Europe/Prague')
now = datetime.now(prague_tz)
today = now.replace(minute=0, second=0, microsecond=0)
today_iso = today.isoformat()
within_two_weeks = today + timedelta(weeks=3)
within_two_weeks_iso = within_two_weeks.isoformat()
# Provide a GraphQL query
# after can also handle hours
query = gql(
    f"""
    query MyQuery {{
      events(
        after: "{today_iso}", before: "{within_two_weeks_iso}"
      ) {{
        id
        title
        location
        start
        coordinates
        eventTemplate {{
          category {{
          id
          }}
        }}
      }}
    }}
"""
)

# Execute the query on the transport
result = client.execute(query)
json_object = json.dumps(result, indent=2)

actions_path = path.abspath(path.join(__file__, "../..", "actions"))
with open(path.join(actions_path, "events.json"), "w+") as outfile:
    outfile.write(json_object)
