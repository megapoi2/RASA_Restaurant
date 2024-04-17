from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionVerifierDisponibilite(Action):
    def name(self) -> Text:
        return "action_verifier_disponibilite"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Implémentez la logique pour vérifier la disponibilité ici
        return []

class ActionConfirmerReservation(Action):
    def name(self) -> Text:
        return "action_confirmer_reservation"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Implémentez la logique pour confirmer la réservation ici
        return []

class ActionGenererCodeReservation(Action):
    def name(self) -> Text:
        return "action_generer_code_reservation"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Implémentez la logique pour générer le code de réservation ici
        return []
