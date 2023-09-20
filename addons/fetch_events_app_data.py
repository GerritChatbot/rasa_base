from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport
from datetime import datetime, timedelta
# https://pypi.org/project/jq/
# https://pypi.org/project/pyjq/
import json
import os.path as path
from dateutil.parser import parse

# Select your transport with a defined url endpoint
header = {'x-tumi-tenant': 'cu-prague'}
transport = AIOHTTPTransport(url="https://cu-prague.esn.world/graphql", headers=header)

# Create a GraphQL client using the defined transport
client = Client(transport=transport, fetch_schema_from_transport=True)

today = datetime.now().date().strftime("%Y.%m.%d %H:%M")
within_two_weeks = parse(today) + timedelta(weeks=3)
# Provide a GraphQL query
# after can also handle hours
query = gql(
    f"""
    query MyQuery {{
      events(
        after: "{today}", before: "{within_two_weeks}"
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
