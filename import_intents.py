import json

from environs import Env


def create_intent(project_id, display_name, training_phrases_parts, message_texts):
    """Create an intent of the given intent type."""
    from google.cloud import dialogflow

    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part)
        # Here we create a new training phrase for each provided part.
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name, training_phrases=training_phrases, messages=[message]
    )

    response = intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )

    print("Intent created: {}".format(response))


if __name__ == "__main__":
    env = Env()
    env.read_env()
    google_project_name = env.str('GOOGLE_PROJECT_NAME')

    with open("questions.json", "r", encoding="utf-8") as my_file:
        questions_file = my_file.read()

    questions = json.loads(questions_file)

    for intent_name, questions_and_answer in questions.items():
        create_intent(
            google_project_name,
            intent_name,
            questions_and_answer.get('questions'),
            [questions_and_answer.get('answer')],
        )
