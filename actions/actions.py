# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions
import os.path
# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []
from typing import Any, Text, Dict, List
import pandas as pd
from datetime import date

from rasa_sdk.events import SlotSet
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
#TODO move to some config file as a constant
full_path = os.path.realpath(__file__)
actions_dir = os.path.dirname(full_path)
project_root_dir = os.path.dirname(actions_dir)

class ActionSaySubscriptionEmail(Action):

    def name(self) -> Text:
        return "action_say_subscription_email"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        email = tracker.get_slot("email")
        if not email:
            dispatcher.utter_message(text="I don't know your email.")
        else:
            dispatcher.utter_message(text=f"Your email is {email}!")
        return []


class ShowOfficeHoursTime(Action):

    def name(self) -> Text:
        return "action_show_office_hours"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        df = pd.read_excel(os.path.join(project_root_dir, "external_data_test", "office_hours.xlsx"))
        df['date'] = pd.to_datetime(df['date'], format='%d%m%Y')
        df = df.set_index('date')

        today = date.today()
        d1 = today.strftime("%d/%m/%Y")

        index_of_nearest_row_in_future = df.index.get_loc(d1, method='backfill')
        nearest_row_in_future = df.iloc[[index_of_nearest_row_in_future]].reset_index()

        dispatcher.utter_message(
            text=f"The nearest Office Hours are on {nearest_row_in_future['date'][0].strftime('%d/%m/%Y')} "
                 f"from {nearest_row_in_future['time_range_start'][0]} "
                 f"till {nearest_row_in_future['time_range_end'][0]}")

        return []
