from ML_Pipeline.db import ContextManager, IntentFlow, UserQuery
from ML_Pipeline.infer import interpreter


def process_message(message, client_id, chat_id):
    """
    :param message: chat message from the user ,to be processed by the ML models
    :param client_id: client id
    :param chat_id: chat id for storing context
    :return: returns response / prompt for the un - fulfilled slots defined for the given intent
    """
    """ take chat message,predicts from rasa nlu pipeline"""
    response = interpreter.parse(message.lower())
    intent_pred = response['intent']['name']
    intent_conf = response['intent']['confidence']

    """Check if the conf is > 90% or else intent is None"""
    intent = None
    if intent_conf > 0.70:
        intent = intent_pred

    entities_pred = response['entities']
    print(entities_pred, 'model_entity', intent_conf, "model_name", intent_pred)
    """ Init the context object by client and chat id"""
    ask_user = UserQuery(client_id)
    context_manager = ContextManager(client_id, chat_id)
    '''Check if there is an existing intent'''
    '''if yes, check predicted now is same or not, if same fine, if not, prompt user , if they wants to change??'''
    print(len(entities_pred), "no of entity")
    try:
        if len(entities_pred) == 0:
            try:
                ask_user.add_query(message.lower())
            except Exception as e:
                print('db', e)
            print("1", "1")
            return "I'm sorry, but I don't understand what you mean by \"{}\" " \
                   " Can you please provide some context or clarify what you're looking for?".format(message)
        # if intent_conf <= 5.0 and len(entities_pred) >0:

        if intent_conf == 0.0 or intent_pred is None:
            print("2,1")
            return "I'm sorry, but I don't understand what you mean by \"{}\" " \
                   " Can you please provide some context or clarify what you're looking for?'".format(message)
        context = context_manager.get_context()

        if "intent" in context.keys():
            intent_context = context['intent']
            print(context['intent'], intent_pred)
            """check if the intent predicted and intent stored in the context are same or not!!"""
            # print(intent,'predicted')
            # print(intent_context,'db predicted')
            if intent_context == intent:
                intent = intent_context
            else:
                # if intent:
                if intent:
                    # return "Do you want to change the intent?"
                    intent = intent_pred

                else:
                    """it means there is no intent now, so we will continue the intent in context"""
                    intent = intent_context
        elif "entity" in context.keys:
            print(context['entity'],"entity in context..")

        print("model intent ", intent, 'database --> ', context['intent'])
    except:
        """No context has been saved yet for this chat yet!! """
        # todo here
        # print('exception')
        if intent:
            context_manager.update_slots(intent=intent)

    if entities_pred:
        for each_ent in entities_pred:
            """
            Push each entity label and text if the thers>0.6 as the context
            """

            entity = each_ent['entity']
            value = each_ent['value']
            conf = each_ent['confidence']
            # print(entity, conf)
            if conf > 0.50:  # confidence of entity
                # print("happened")
                # intent =""

                context_manager.update_slots(entity=entity)
            else:
                print('your entity confidence is low', conf)
                return "Don't know what you want to say!"
    """Get the slots for that intent ,given chat_id"""
    if intent is None:
        # return 'sorry to information reading that intent'
        print("none --> intent")
        return "I'm sorry, but I don't understand what you mean by \"{}\" " \
               "Can you please provide some context or clarify what you're looking for?'".format(message)

    print(intent, "<---intent")

    response = context_manager.get_slots(intent)
    if response:
        prompt_question = response[0]['prompt']
        return prompt_question
    else:
        """get the api response , given client id, runs and returns response"""
        intent_obj = IntentFlow(client_id)
        api_url = intent_obj.extract_api(intent)
        print(response)
        return api_url
