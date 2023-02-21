from ML_Pipeline.utlis import read_data
import json
from ML_Pipeline.infer import infer_message
from ML_Pipeline.dialog import process_message
from ML_Pipeline.training import train_rasa
# import uuid

from ML_Pipeline.config import training_data_input


# def regrex_code(text):
#     return text.strip().replace('\"', '').replace('\'', '').replace('?', '').replace(',', '').replace('!', '').lower()
#
#
# def regrex(text):
#     return text.strip().replace('\"', '').replace('\'', '').replace('?', '').replace(',', '').replace('!', '')
#
#
# # # train rasa with the specified data inside Input Folder
# def validate_data(text, intent, entities_list):
#     print(text, intent)
#     final_text = regrex_code(text)
#     final_intent = regrex(intent)
#     # start =  end = entity = value = []
#     obj_dict = {}
#
#     list_dict = []
#     for data in entities_list:
#         entity = (regrex(data['entity']))
#         value = (regrex_code(data['value']))
#         start = (data['start'])
#         end = (data['end'])
#         list_dict.append({"start": start,
#                           "end": end,
#                           "value": value,
#                           "entity": entity})
#     temp = {"text": final_text,
#             "intent": final_intent,
#             "entities": list_dict}
#     obj_dict.update(temp)
#     # print(obj_dict)
#     return obj_dict
#
#
# def read_json():
#     file = open('../input/data.json', 'r', encoding="utf8")
#     json_data = json.loads(file.read())
#     file.close()
#     final_data = {"rasa_nlu_data": {
#         "common_examples": [
#         ]
#     }}
#     for i in json_data['rasa_nlu_data']['common_examples']:
#         text = i['text']
#         intent = i['intent']
#         entities_list = i['entities']
#         temp_dict = validate_data(text, intent, entities_list)
#         final_data['rasa_nlu_data']['common_examples'].append(temp_dict)
#     file = open('../input/final_data.json', 'w', encoding="utf8")
#     file.write(json.dumps(final_data))
#     file.close()
#
#
# read_json()
train_rasa()
print("read successfully")

# infer rasa intent and entity on one single message using infer_message
# message = "Will my access to foodwatch features be restricted if my status is 'Inactive'??"
# response = infer_message(message)
# print(response, '4')
# print()
# dialog conversation and context management
# if __name__ == "__main__":
#     chat_id = uuid.uuid4()
#     client_id = 32
#     print(chat_id, client_id)
# while True:
#     message = input(">>").lower()
#     response = process_message(message, client_id, chat_id)
#     print(response)
# print("done")
