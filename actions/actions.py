# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions
import os.path
import json
from typing import Any, Text, Dict, List
import pandas as pd
from datetime import date
from dateutil.parser import parse
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
#TODO move to some config file as a constant
full_path = os.path.realpath(__file__)
actions_dir = os.path.dirname(full_path)
project_root_dir = os.path.dirname(actions_dir)


class ShowOfficeHoursTime(Action):

    def name(self) -> Text:
        return "action_show_office_hours"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        df = pd.read_excel(os.path.join(project_root_dir, "external_data_test", "office_hours.xlsx"))
        df['date'] = pd.to_datetime(df['date'], format='%d%m%Y')
        df = df.set_index('date')

        #TODO turn into a function that I can reuse to search for nearest date?
        today = date.today()
        d1 = pd.to_datetime(today)

        index_of_nearest_row_in_future = df.index.get_indexer([d1], method='bfill')
        nearest_row_in_future = df.iloc[index_of_nearest_row_in_future].reset_index()

        dispatcher.utter_message(
            text=f"The office address is Jednota Dormitory, Opletalova 1663/38 and the nearest office hours are on "
                 f"{nearest_row_in_future['date'][0].strftime('%d/%m/%Y')} "
                 f"from {nearest_row_in_future['time_range_start'][0]}h "
                 f"till {nearest_row_in_future['time_range_end'][0]}h ")
        return []


class GetEvent(Action):

    def name(self) -> Text:
        return "action_get_event"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        with open(os.path.join(actions_dir, "events.json")) as events:
            contents = json.loads(events.read())

        # my_events = [event for event in contents["events"] if event["eventTemplate"]["category"]["id"] == "896575a3-89a7-47da-b80c-113205a7e02a"]
        for event in contents.get("events"):
            templateID = event["eventTemplate"]["category"]["id"]
            if templateID != "896575a3-89a7-47da-b80c-113205a7e02a":
                break

        title = event.get("title")
        location = event.get("location")
        start = event.get("start")
        datetime_object = parse(start)
        date = datetime_object.date()
        time = datetime_object.time()

        lat = float(event.get("coordinates").get("lat"))
        lng = float(event.get("coordinates").get("lng"))

        text = f"One of the closest events is '<b>{title}</b>' which takes place on {date} at {time}"
        dispatcher.utter_message(json_message={"text": text, "parse_mode": "HTML"})

        dispatcher.utter_message(json_message={"latitude": lat, "longitude": lng, "title":"Check capacity before you go!", "address": location})

        text = f"You can check it's capacity, register and pay within <a href='https://cu-prague.esn.world/events'>our app</a>."
        dispatcher.utter_message(json_message={"text": text, "parse_mode": "HTML"})
        return []

