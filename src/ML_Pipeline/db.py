import json
from pymongo import MongoClient


class IntentFlow:
    def __init__(self, client_id):
        """
        :param client_id: takes client id as parameter to store intent flow per client wise
        """
        self.mongo_client = MongoClient()
        self.db = self.mongo_client.chatflowdb
        self.intent_table = self.db['chatflow']
        self.client_id = client_id
        # self.collections = self.db.list_collection_names()

    def add_flows(self, flow):
        """
        :param flow: Inserts specified flow per client
        :return: None
        """
        self.intent_table.insert_one({
            "client_id": self.client_id,
            "flow": flow,
        })

    # @staticmethod

    def extract_api(self, intent_name):
        """
        :param intent_name: intent name is the name of intent for which we need to extract api details
        :return: calls resolve api internally ,returns response from resolve api
        """
        response = self.intent_table.find_one({"client_id": self.client_id, "flow.intent": intent_name})
        api_url = response['flow']['api_data']['url']
        print(api_url, "api_url", type(api_url))
        print('calling resolve')
        # response = resolve_api(api_url)
        return api_url

    def get_flows(self):
        """
        :return: returns flows associated with the given client id
        """
        response = self.intent_table.find({
            "client_id": self.client_id,

        })
        return list(response)

    def get_slots_by_intent(self, intent_name):
        """
        :param intent_name: intent names to which we need the slots
        :return: returns slots needs to be fulfilled before triggering api
        """
        response = self.intent_table.find_one({
            "client_id": self.client_id,
            "flow.intent": intent_name})
        slots = None
        if response:
            slots = response['flow']['entities']
        return slots


class ContextManager:
    def __init__(self, client_id, chat_id):
        """
        :param client_id: client id of the context
        :param chat_id: chat id to be stored ,so that the context stored is stored by chat for windows per client
        """
        self.mongo_client = MongoClient()
        self.db = self.mongo_client.chatflowdb
        self.chat_session = self.db['chatsession']
        self.client_id = client_id
        self.chat_id = chat_id

    def disconnect(self):
        self.mongo_client.close()

    def get_context(self):
        """
        :return: returns context stored for a given chat_id
        """
        response = self.chat_session.find_one({"chat_id": self.chat_id})
        return response

    def update_slots(self, intent=None, entity=None):
        """
        :param intent: intent to be updated for a given chat_id
        :param entity: entity to be updated for a given chat_id
        :return: None
        """
        if intent:
            self.chat_session.find_one_and_update(
                {"chat_id": self.chat_id},
                {"$set": {"intent": intent}},
                upsert=True
            )
        if entity:
            self.chat_session.find_one_and_update(
                {"chat_id": self.chat_id},
                {"$push": {"entity": entity}},
                upsert=True

            )

    def get_filled_slots(self):
        """
        :return: returns all the filled slots in the given context for a given chat_id
        """
        response = self.chat_session.find_one({"chat_id": self.chat_id})
        # print(response)
        filled_slots = None

        if response and "entity" in response:
            filled_slots = response['entity']
        return filled_slots

    def add_flow_user(self, ref):
        file = open('ML_Pipeline/test.json', 'r')
        data = json.load(file)
        file.close()
        try:
            for d in data['flow']:
                ref.add_flows(d)
                print('*' * 60)
                print("data added for new client id is ", self.client_id)
                print('*' * 60)
        except Exception as e:
            print(e)

    def get_slots(self, intent_name):
        """
        :param intent_name: intent to be checked for a not-filled Slots
        :return: slots which are not filled, first check the context and returns  slots are not filled
        """
        intent_flow_obj = IntentFlow(self.client_id)
        # find client id if not perform add flow
        temp = intent_flow_obj.get_flows()
        if not temp:
            self.add_flow_user(intent_flow_obj)
        slots = intent_flow_obj.get_slots_by_intent(intent_name)
        print(slots, "slot")
        if slots:
            filled_slots = self.get_filled_slots()
            print(filled_slots, 'filled')

            not_filled_slots = [ent for ent in slots if ent['entity'] not in filled_slots]

            print(not_filled_slots, "not filled")
            return not_filled_slots
        else:
            print("No flow found for this intent")


class UserQuery:
    def __init__(self, client_id):
        """
        :param client_id: client id of the context
        """
        self.mongo_client = MongoClient()
        self.db = self.mongo_client.chatflowdb
        self.chat_query = self.db['users_query']
        self.request_api = self.db['users_query_answer']
        self.client_id = client_id
        # self.chat_id = chat_id

    def get_answers(self, question_no):
        """
              :return: returns query stored for a given chat_id
        """

        ls = []
        try:
            print(type(question_no), "question type")
            response = self.request_api.find({"question_no": question_no})
            for res in response:
                print(res['answer'])
                ls.append(res['answer'])
        except Exception as e:
            print(e)
        response = ls
        return response

    def add_answers(self, question_no, answers):
        """
            :param question_no:
            :param answers:
            :return: None
            """
        self.request_api.insert_one({
            "question_no": question_no,
            "answer": answers,
        })

    def add_query(self, query):
        """
        :param query: Insert query from client
        :return: None
        """
        self.chat_query.insert_one({
            "client_id": self.client_id,
            "query": query,
        })

    def get_query(self):
        """
        :return: returns query stored for a given chat_id
        """
        response = self.chat_query.find({"client_id": self.client_id})
        return response
