# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions
import os.path
import json
from typing import Any, Text, Dict, List
from dateutil.parser import parse
import pytz
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
#TODO move to some config file as a constant
full_path = os.path.realpath(__file__)
actions_dir = os.path.dirname(full_path)
project_root_dir = os.path.dirname(actions_dir)
prague_timezone = pytz.timezone('Europe/Prague')

class GetOfficeHoursTime(Action):

    def name(self) -> Text:
        return "action_get_office_hours"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        with open(os.path.join(actions_dir, "events.json")) as events:
            contents = json.loads(events.read())

        event_exists_flag = False
        for event in contents.get("events"):
            templateID = event["eventTemplate"]["category"]["id"]
            # templateID of office hours category
            if templateID == "20397038-f186-4cb1-ab88-8ea23b318898":
                event_exists_flag = True
                break

        if event_exists_flag:
            title = event.get("title")
            location = event.get("location")
            start = event.get("start")
            datetime_object = parse(start)
            datetime_object = datetime_object.astimezone(prague_timezone)
            date = datetime_object.date()
            time = datetime_object.time()

            lat = float(event.get("coordinates").get("lat"))
            lng = float(event.get("coordinates").get("lng"))

            text = f"The next '<b>Office hours</b>' takes place on {date} at {time} on {location}"
            dispatcher.utter_message(json_message={"text": text, "parse_mode": "HTML"})

            dispatcher.utter_message(json_message={"latitude": lat, "longitude": lng, "title":"The magic happens here!", "address": location})

            text = f"For more info about the other events, you can check <a href='https://cu-prague.esn.world/events'>our app</a>."
            dispatcher.utter_message(json_message={"text": text, "parse_mode": "HTML"})
        # no event with the correct category ID was found, no Office hours in json
        else:
            text = f'We are sorry, it seems there are no scheduled Office hours.'
            dispatcher.utter_message(json_message={"text": text, "parse_mode": "HTML"})
            text = f"Keep an eye on <a href='https://cu-prague.esn.world/events'>our events app</a> or write me later - there might be some Office hours scheduled soon."
            dispatcher.utter_message(json_message={"text": text, "parse_mode": "HTML"})
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
            if templateID not in ["896575a3-89a7-47da-b80c-113205a7e02a", "20397038-f186-4cb1-ab88-8ea23b318898"]:
                break

        title = event.get("title")
        location = event.get("location")
        start = event.get("start")
        datetime_object = parse(start)
        datetime_object = datetime_object.astimezone(prague_timezone)
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

