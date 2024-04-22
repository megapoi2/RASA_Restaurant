import json
import os
from datetime import datetime, timedelta
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

class ActionVerifierDisponibilite(Action):
    def name(self) -> Text:
        return "action_verifier_disponibilite"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        nouvelle_date_resa = tracker.get_slot("date")  
        current_directory = os.path.dirname(os.path.realpath(__file__))
        reservations_file_path = os.path.join(current_directory, "reservations.json")
        with open(reservations_file_path, "r") as file:
            reservations = json.load(file)


        for reservation in reservations["reservation"]:
            if reservation["dateDeReservation"] == nouvelle_date_resa:
                dispatcher.utter_message("Désolé, cette date n'est pas disponible.")
                return [SlotSet("date_disponible", False)]

        dispatcher.utter_message("La date est disponible.")
        return [SlotSet("date_disponible", True)]


class ActionConfirmerReservation(Action):
    def name(self) -> Text:
        return "action_confirmer_reservation"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        date_resa = tracker.get_slot("date")
        nombre_personnes = tracker.get_slot("nombre_personnes")
        nom_resa = tracker.get_slot("nom")
        numero_telephone = tracker.get_slot("numero_telephone")
        commentaire = tracker.get_slot("commentaire")

        print("Date de réservation :", date_resa)
        print("Nombre de personnes :", nombre_personnes)
        print("Nom :", nom_resa)
        print("Numéro de téléphone :", numero_telephone)
        print("Commentaire :", commentaire)


        current_directory = os.path.dirname(os.path.realpath(__file__))
        reservations_file_path = os.path.join(current_directory, "reservations.json")

        with open(reservations_file_path, "r") as file:
            reservations = json.load(file)

        reservations["reservation"].append({
            "codeResa": len(reservations["reservation"]) + 1,
            "dateDeReservation": date_resa,
            "nombreDePersonnes": nombre_personnes,
            "nomDeResa": nom_resa,
            "numeroDeTelephone": numero_telephone,
            "commentaire": commentaire
        })

        with open(reservations_file_path, "w") as file:
            json.dump(reservations, file, indent=4)

        dispatcher.utter_message("Votre réservation a été confirmée.")

        return []


class ActionProposerNouvelleDate(Action):
    def name(self) -> Text:
        return "action_proposer_nouvelle_date"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        current_directory = os.path.dirname(os.path.realpath(__file__))
        reservations_file_path = os.path.join(current_directory, "reservations.json")

        with open(reservations_file_path, "r") as file:
            reservations = json.load(file)

        booked_dates = [reservation["dateDeReservation"] for reservation in reservations["reservation"] if reservation["dateDeReservation"]]

        next_available_date = self.find_next_available_date(booked_dates)

        if next_available_date:
            dispatcher.utter_message(f"La prochaine date disponible est le {next_available_date}.")
            dispatcher.utter_message("Pour quelle date voulez-vous réserver ?")
        else:
            dispatcher.utter_message("Désolé, aucune date disponible n'a été trouvée.")

        return []

    def find_next_available_date(self, booked_dates: List[str]) -> str:
        today = datetime.now().date()

        while True:
            if str(today) not in booked_dates:
                return str(today)
            today += timedelta(days=1)