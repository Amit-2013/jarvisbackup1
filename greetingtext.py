from TextToSpeech import Fast_DF_TTS
import time
import random


def speak_and_print(text):
    print(text)
    Fast_DF_TTS.speak(text)


def get_greeting_based_on_time():
    current_hour = time.localtime().tm_hour

    morning_greetings = [
        "Good morning, Sir. JARVIS at your service.",
        "Good morning, Sir. Ready to assist you.",
        "Good morning, Sir. How can I help you today?"
    ]

    afternoon_greetings = [
        "Good afternoon, Sir. JARVIS is here to assist you.",
        "Good afternoon, Sir. How may I assist you this fine afternoon?",
        "Good afternoon, Sir. Ready to help with whatever you need."
    ]

    evening_greetings = [
        "Good evening, Sir. JARVIS is ready to help you.",
        "Good evening, Sir. How can I be of service tonight?",
        "Good evening, Sir. Here to assist with your evening needs."
    ]

    if 0 <= current_hour < 12:
        return random.choice(morning_greetings)
    elif 12 <= current_hour < 18:
        return random.choice(afternoon_greetings)
    else:
        return random.choice(evening_greetings)


def introduction():
    time.sleep(3)
    greeting = get_greeting_based_on_time()
    speak_and_print(greeting)


def get_closing_message_based_on_time():
    current_hour = time.localtime().tm_hour

    morning_closings = [
        "It was a pleasure assisting you this morning, Sir!",
        "I hope you have a productive day ahead. Goodbye, Sir!",
        "Have a great morning, Sir. Farewell!"
    ]

    afternoon_closings = [
        "It was great assisting you this afternoon, Sir!",
        "Enjoy the rest of your day. Goodbye for now, Sir!",
        "Have a pleasant afternoon, Sir. See you next time!"
    ]

    evening_closings = [
        "It was a pleasure assisting you this evening, Sir!",
        "Have a restful night and a great tomorrow. Goodbye, Sir!",
        "Goodbye for now, Sir. Have a wonderful evening!"
    ]

    if 0 <= current_hour < 12:
        return random.choice(morning_closings)
    elif 12 <= current_hour < 18:
        return random.choice(afternoon_closings)
    else:
        return random.choice(evening_closings)


def closing_message():
    time.sleep(1)
    closing_text = get_closing_message_based_on_time()
    speak_and_print(closing_text)
