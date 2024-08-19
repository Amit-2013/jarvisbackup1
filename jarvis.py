import threading
import random
import time
from concurrent.futures import ThreadPoolExecutor

from internet_check import is_Online
from Alert import Alert
from Data.DLG_Data import online_dlg, offline_dlg
from co_brain import Jarvis
from TextToSpeech.Fast_DF_TTS import speak
from Automation.Battery import check_plug
from Time_Operations.throw_alert import check_schedule, check_Alam
from greetingtext import introduction, closing_message
# Paths to schedule and alarm data
ALARM_PATH = r"C:\Users\Admin\PycharmProjects\pythonProject1\Alam_data.txt"
SCHEDULE_PATH = r'C:\Users\Admin\PycharmProjects\pythonProject1\schedule.txt'

# Randomly select dialogues for online and offline scenarios
ran_online_dlg = random.choice(online_dlg)
ran_offline_dlg = random.choice(offline_dlg)

# Lock for thread safety
lock = threading.Lock()


def thread_safe_speak(dialogue):
    """A thread-safe wrapper for the speak function."""
    with lock:
        speak(dialogue)


def thread_safe_alert(dialogue):
    """A thread-safe wrapper for the Alert function."""
    with lock:
        Alert(dialogue)


def wish():
    """This function initiates threads to handle speaking and alerting."""
    try:
        t1 = threading.Thread(target=thread_safe_speak, args=(ran_online_dlg,))
        t2 = threading.Thread(target=thread_safe_alert, args=(ran_online_dlg,))
        t1.start()
        t2.start()
        t1.join()
        t2.join()
    except Exception as e:
        print(f"Error in wish function: {e}")


def start_threads():
    """Start all the necessary threads for the main functionality."""
    try:
        with ThreadPoolExecutor(max_workers=4) as executor:
            # Submitting tasks to the thread pool
            future1 = executor.submit(check_plug)
            future2 = executor.submit(check_schedule, SCHEDULE_PATH)
            future3 = executor.submit(Jarvis)
            future4 = executor.submit(check_Alam, ALARM_PATH)

            # Waiting for all futures to complete
            future1.result()
            future2.result()
            future3.result()
            future4.result()
    except Exception as e:
        print(f"Error in starting threads: {e}")


def main():
    """Main function to check online status and initiate respective processes."""
    try:
        if is_Online():
            wish()  # Handle online scenario
            introduction()  # Introduction from greetingtext.py
            start_threads()  # Start all relevant threads
        else:
            thread_safe_alert(ran_offline_dlg)  # Handle offline scenario
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        closing_message()  # Ensure closing message is sent


# Run the main function
if __name__ == "__main__":
    main()
