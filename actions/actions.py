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
        return "action_what_is_my_subscription_email"

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

        #TODO turn into a function that I can reuse to search for nearest date?
        today = date.today()
        d1 = today.strftime("%d/%m/%Y")

        index_of_nearest_row_in_future = df.index.get_loc(d1, method='backfill')
        nearest_row_in_future = df.iloc[[index_of_nearest_row_in_future]].reset_index()

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
        event_name = tracker.get_slot("event")
        print(event_name)

        current_month = date.today().strftime("%B")
        print(current_month)
        current_day = date.today().day
        print(current_day)

        sheets = pd.ExcelFile(os.path.join(project_root_dir, "external_data_test", "events.xlsx")).sheet_names

        # find substring "current_month" in sheets
        closest_sheet = [sheet for sheet in sheets if current_month in sheet][0]
        print(closest_sheet)
        df = pd.read_excel(os.path.join(project_root_dir, "external_data_test", "events.xlsx"),
                           sheet_name=closest_sheet)
        print(df.keys())
        event_data = df[df["EVENT"] == event_name]
        print(event_data)
        print(event_data.get("DATE"))

        df_sort = event_data.iloc[(event_data['DATE'] - current_day).abs().argsort()[:2]]
        print(df_sort)
        df_sort_list = df_sort.index.tolist()

        final_index = [x for x in df_sort_list if x >= current_day]
        final_data = df.iloc[final_index]
        final_date = int(final_data["DATE"].values[0])
        final_event_name = final_data["EVENT"].values[0]
        final_start_hour = final_data["START"].values[0]
        final_end_hour = final_data["END"].values[0]
        final_price = final_data["PRICE"].values[0]
        final_place = final_data["PLACE"].values[0]
        final_registration_form = final_data["REGISTRATION FORM\n(link na drive)"].values[0]
        print(
            f"The event {final_event_name} is taking place on {final_date}. from {final_start_hour} till {final_end_hour} "
            f"on the address {final_place}. It costs {final_price} and you can register here: {final_registration_form}")

        dispatcher.utter_message(
            text=f"The event {final_event_name} is taking place on {final_date}. from {final_start_hour} till {final_end_hour} "
            f"on the address {final_place}. It costs {final_price} and you can register here: {final_registration_form}")
        return []

