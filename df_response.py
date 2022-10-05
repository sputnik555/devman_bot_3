from google.cloud import dialogflow


def get_dialogflow_response(google_project_name, message, chat_id):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(google_project_name, chat_id)
    text_input = dialogflow.TextInput(text=message, language_code='ru')
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )
    return response
