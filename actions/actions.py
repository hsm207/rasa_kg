import logging
from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from typedb.client import *


def get_device_plan_type(device):
    query = f"""
    match

        $d isa device, has name "{device}";
        $p isa plan;
        $r (device:$d, plan:$p) isa contract;

    get $p;
    """

    with TypeDB.core_client("knowledge-base:1729") as client:
        with client.session("shop", SessionType.DATA) as session:
            with session.transaction(TransactionType.READ) as read_transaction:
                plan = read_transaction.query().match(query)
                plan = list(plan)

    if not plan:
        return None

    return plan[0].get("p").get_type().get_label().name()


def has_entity_type(entities, type):
    return any(e for e in entities if e["entity"] == type)


def extract_entity(entities, type):
    return [e["value"] for e in entities if e["entity"] == type][0]


class ActionDisambiguateContract(Action):
    def name(self) -> Text:
        return "action_disambiguate_contract"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        entities = tracker.latest_message.get("entities")

        has_contract_type = has_entity_type(entities, "contract_type")
        has_device = has_entity_type(entities, "device")

        if has_contract_type or not has_device:
            return []

        device = extract_entity(entities, "device")
        plan_type = get_device_plan_type(device)
        logging.debug(f"device is {device}")
        logging.debug(f"plan_type is {plan_type}")

        return [SlotSet("contract_type", plan_type)]
