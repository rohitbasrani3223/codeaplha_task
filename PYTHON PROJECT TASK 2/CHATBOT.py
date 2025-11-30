import random
import datetime
import webbrowser
import time
import sys

# FEATURE 1: Typing Effect (Hacker/AI style writing)
def type_msg(text):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.04) # Speed control
    print() # New line

# FEATURE 2: Random Responses (Taaki bot natural lage)
greetings = ["Hello ji!", "Namaste!", "Hi! Main taiyar hoon.", "Swagat hai aapka!"]
farewells = ["Bye bye!", "Alvida!", "See you soon!", "Have a nice day!"]
confused = ["Samajh nahi aaya, dubara boliye?", "Thoda aasan shabdon mein puchiye.", "Sorry, main abhi seekh raha hoon."]

def start_advanced_chat():
    print("=========================================")
    type_msg("⚡ SYSTEM INITIATED: JARVIS LITE ⚡")
    type_msg("Main aapka Advanced Assistant hoon.")
    print("=========================================")

    while True:
        user_input = input("\n👤 Aap: ").lower()

        # 1. Greetings (Random Selection)
        if "hello" in user_input or "hi" in user_input:
            type_msg("🤖 Bot: " + random.choice(greetings))

        # 2. Time Batana (Datetime Module)
        elif "time" in user_input or "samay" in user_input:
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            type_msg(f"🤖 Bot: Abhi samay hua hai: {current_time}")

        # 3. Date Batana
        elif "date" in user_input or "tarikh" in user_input:
            today = datetime.datetime.now().strftime("%d %B, %Y")
            type_msg(f"🤖 Bot: Aaj ki tarikh hai: {today}")

        # 4. Website Open Karna (Webbrowser Module)
        elif "open google" in user_input:
            type_msg("🤖 Bot: Google open kar raha hoon...")
            webbrowser.open("https://www.google.com")
            
        elif "open youtube" in user_input:
            type_msg("🤖 Bot: YouTube chalu kar diya hai! Enjoy.")
            webbrowser.open("https://www.youtube.com")

        elif "play song" in user_input or "gana" in user_input:
            type_msg("🤖 Bot: Aapke liye gaana baja raha hoon...")
            # Seedha YouTube par music search khul jayega
            webbrowser.open("https://www.youtube.com/results?search_query=latest+hindi+songs")

        # 5. Developer Info
        elif "kaun ho" in user_input or "who are you" in user_input:
            type_msg("🤖 Bot: Main ek Advanced Python Program hoon.")

        # 6. Exit
        elif "bye" in user_input or "exit" in user_input:
            type_msg("🤖 Bot: " + random.choice(farewells))
            break

        # 7. Default (Jab samajh na aaye)
        else:
            type_msg("🤖 Bot: " + random.choice(confused))

# Project Run Karna
start_advanced_chat()