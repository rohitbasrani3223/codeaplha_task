def start_chat():
    print("-------------------------------------------------------")
    print("🤖 PyBot: Namaste! Main aapka naya dost hoon.")
    print("Mujhse kuch bhi puchiye! (Baat khatam karne ke liye 'bye' likhein)")
    print("-------------------------------------------------------")

    while True:
        # STEP 1: User se input lena
        # .lower() lagaya hai taaki 'Hello', 'HELLO' sab same maana jaye
        user_text = input("\nAap: ").lower()

        # STEP 2: Decision Making Logic (Bahut saare rules)
        
        # Greeting Check
        if "hello" in user_text or "hi" in user_text or "namaste" in user_text:
            print("🤖 PyBot: Hello ji! Kahiye kya haal hain?")

        # Haal-chaal
        elif "kaise ho" in user_text or "how are you" in user_text:
            print("🤖 PyBot: Main ek code hoon, hamesha first class rehta hoon! 😎 Aap sunao?")

        # Naam puchna
        elif "naam kya" in user_text or "your name" in user_text:
            print("🤖 PyBot: Mera naam 'PyBot' hai. Mujhe Python ne banaya hai.")

        # Creator ke baare mein
        elif "kisne banaya" in user_text or "who made you" in user_text:
            print("🤖 PyBot: Mujhe ek bahut smart developer ne banaya hai (wo aap hain!).")

        # Joke sunna
        elif "joke" in user_text or "chutkula" in user_text:
            print("🤖 PyBot: Teacher: Pappu, batao 'Hospital' ko Hindi mein kya kehte hain?")
            print("          Pappu: Dharti pe Narak! 😂")

        # Kya kar rahe ho
        elif "kya kar" in user_text or "what are you doing" in user_text:
            print("🤖 PyBot: Bas aapke message ka wait kar raha tha.")

        # Coding related
        elif "python" in user_text:
            print("🤖 PyBot: Python meri favourite language hai! ❤️")

        # STEP 3: Exit/Stop Rule (Sabse Important)
        elif "bye" in user_text or "tata" in user_text or "goodbye" in user_text:
            print("🤖 PyBot: Chaliye theek hai, baad mein milte hain. Alvida! 👋")
            break  # Yeh loop ko tod dega aur program band ho jayega

        # STEP 4: Default Reply (Jab kuch samajh na aaye)
        else:
            print("🤖 PyBot: Maaf kijiye, mujhe yeh samajh nahi aaya. Kuch aasaan puchiye?")

# Main function ko call karna taaki program shuru ho
start_chat()