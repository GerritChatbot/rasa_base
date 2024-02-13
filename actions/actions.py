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

    def get_event(self):
        with open(os.path.join(actions_dir, "events.json")) as events:
            contents = json.loads(events.read())
        print(contents)
        office_hours_event = None
        OFFICE_HOURS_TEMPLATE_ID = "20397038-f186-4cb1-ab88-8ea23b318898"
        events = contents.get("events")
        office_hours_events = [event for event in events if
                               event["eventTemplate"]["category"]["id"] == OFFICE_HOURS_TEMPLATE_ID]

        if office_hours_events:
            office_hours_event = office_hours_events[0]
            return office_hours_event
        else:
            return office_hours_event

    def get_event_details(self, event):
        if event is None:
            return None, None, None, None, None, None

        title = event.get("title")
        print(title)
        location = event.get("location")
        start = event.get("start")
        print(start)
        datetime_object = parse(start)
        print(datetime_object)
        datetime_object = datetime_object.astimezone(prague_timezone)
        date = datetime_object.date()
        time = datetime_object.time()
        lat = float(event.get("coordinates").get("lat"))
        lng = float(event.get("coordinates").get("lng"))
        return title, location, date, time, lat, lng

    def compile_answer(self, channel, dispatcher, title, location, date, time, lat, lng):
        if channel == 'custom_telegram':
            if title is None:
                text = f'We are sorry, it seems there are no scheduled ESN Office hours.'
                dispatcher.utter_message(json_message={"text": text, "parse_mode": "HTML"})
                text = f"Keep an eye on <a href='https://cu-prague.esn.world/events'>our events app</a> or write me later - there might be some Office hours scheduled soon."
                dispatcher.utter_message(json_message={"text": text, "parse_mode": "HTML"})
            else:
                text = f"The next '<b>ESN Office hours</b>' takes place on {date} at {time} on {location}"
                dispatcher.utter_message(json_message={"text": text, "parse_mode": "HTML"})

                dispatcher.utter_message(
                    json_message={"latitude": lat, "longitude": lng, "title": "The magic happens here!",
                                  "address": location})

                text = f"For more info about the other events, you can check <a href='https://cu-prague.esn.world/events'>our app</a>."
                dispatcher.utter_message(json_message={"text": text, "parse_mode": "HTML"})
        elif channel == 'facebook':
            if title is None:
                text = f'We are sorry, it seems there are no scheduled ESN Office hours.'
                dispatcher.utter_message(text=text)
                text = f"Keep an eye on our events app or write me later - there might be some Office hours scheduled soon."
                dispatcher.utter_message(text=text)
            else:
                text = f"The next ESN Office hours takes place on {date} at {time} on {location}"
                dispatcher.utter_message(text=text)

                #dispatcher.utter_message(
                #    json_message={"latitude": lat, "longitude": lng, "title": "The magic happens here!",
                #                  "address": location})

                text = f"For more info about the other events, you can check our app."
                dispatcher.utter_message(text=text)

        else:
            text = f"Sorry it seems you are using an unsupported channel"
            dispatcher.utter_message(text=text)

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        #1 figure out if there is an office hours event (return event)
        #2 get details about such event
        #3 compile and answer
        channel = tracker.get_latest_input_channel()
        print(channel)
        event = self.get_event()
        title, location, date, time, lat, lng = self.get_event_details(event)
        self.compile_answer(channel, dispatcher, title, location, date, time, lat, lng)
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

        prompt_template

        text = f"You can check it's capacity, register and pay within <a href='https://cu-prague.esn.world/events'>our app</a>."
        dispatcher.utter_message(json_message={"text": text, "parse_mode": "HTML"})
        return []


from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import UserUtteranceReverted
from rasa_sdk.executor import CollectingDispatcher

class ActionDefaultFallback(Action):
    """Executes the fallback action and goes back to the previous state
    of the dialogue"""

    def name(self) -> Text:
        return "custom_nlu_fallback"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        prompt = tracker.latest_message['text']


        text = llm(prompt)
        dispatcher.utter_message(json_message={"text": text, "parse_mode": "HTML"})

        # Revert user message which led to fallback.
        return [UserUtteranceReverted()]