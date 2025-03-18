import os
import textwrap

import openai
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from the .env file

# Set up the OpenAI API client
openai.api_key = os.environ["OPENAI_API_KEY"]


def read_text_from_file(file_path):
    with open(file_path, "r") as file:
        return file.read()


def chunk_text(text, max_tokens):
    return textwrap.wrap(text, max_tokens)


def start_conversation():
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        prompt="The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.\n\nHuman: Hello, who are you?\nAI: I am an AI created by OpenAI. How can I help you today?\nHuman: I'd like to cancel my subscription.\nAI:",
        temperature=0.9,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.6,
        stop=[" Human:", " AI:"],
    )
    return response["id"]


def send_message(conversation_id, message):
    response = openai.ChatCompletion.append_message(conversation_id, role="user", content=message)
    return response.choices[0].text.strip()


def main():
    # Step 1: Read the text from a file
    file_path = "09 Clustering Variables.txt"
    text = read_text_from_file(file_path)

    # Step 2: Chunk the text into parts that fit in the ChatGPT API token limits
    max_tokens = 4096  # Adjust this value according to your API token limit
    text_chunks = chunk_text(text, max_tokens)

    # Step 3: Start a conversation with the ChatGPT API and return the conversation ID
    conversation_id = start_conversation()

    # Step 4: Feed a ChatGPT conversation with the consecutive parts
    for chunk in text_chunks:
        send_message(conversation_id, chunk)

    # Step 5: Ask ChatGPT for a summary of 100-200 words
    summary_request = "Please provide a summary of the text in 100-200 words."
    summary = send_message(conversation_id, summary_request)
    print("Summary:\n", summary)

    # Step 6: Ask ChatGPT to generate 6 multiple choice questions about the text
    question_request = "Generate 6 multiple choice questions about the text."
    questions = send_message(conversation_id, question_request)
    print("\nQuestions:\n", questions)

    # Step 7: Let ChatGPT ask if more multiple choice questions should be generated
    more_questions_request = "Should more multiple choice questions be generated?"
    more_questions_response = send_message(conversation_id, more_questions_request)
    print("\nMore Questions Response:\n", more_questions_response)


if __name__ == "__main__":
    main()
