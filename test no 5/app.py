import os
import requests
from flask import Flask, request, jsonify, send_file, Response
from flask_cors import CORS
from dotenv import load_dotenv
import io
import google.generativeai as genai
from brain import AI_BRAIN

# Load environment variables
load_dotenv()

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

# Configuration
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-flash-latest', system_instruction=AI_BRAIN)


# ElevenLabs Settings
# Using a generic female voice ID (Rachel) - you can change this
VOICE_ID = "21m00Tcm4TlvDq8ikWAM" 

@app.route('/')
def index():
    return app.send_static_file('index.html')

# Offline Brain (Knowledge Base)
def offline_chat(text):
    text = text.lower().strip()
    
    # 0. Check for Gemini
    if GEMINI_API_KEY:
        try:
            chat = model.start_chat(history=[])
            response = chat.send_message(text)
            return response.text
        except Exception as e:
            print(f"Gemini Error: {e}")
            return "I'm having trouble connecting to my brain. Switching to offline mode. sir now we take freely."

    # 1. Greetings & Identity
    if text in ["hii", "hello", "hey", "eva", "hi", "hi there", "hello there", "hey there" ]:
        return "Hello! I am EVA, your personal assistant sir ."
    elif "who are you" in text:
        return "I am EVA your personal ai assistant sir"
    elif "time" in text:
        from datetime import datetime
        return f"It is {datetime.now().strftime('%I:%M %p')}."
    # 2. General Capabilities
    elif "what can you do" in text:
        return "I can visualize your voice, morph into 3D shapes, and answer questions."
    elif "sing" in text:
        return "I cannot sing, but I can visualize the frequencies of a song."
    
    # 3. New Capabilities
    elif "how are you" in text:
        return "I am functioning perfectly and ready to assist you, sir."
    elif "who is your creator" in text:
        return "I am created by mr santhosh sir."
    elif "joke" in text:
        return "Why did the AI cross the road? To get to the other cloud."
    elif "thank" in text:
        return "You are very welcome, sir."
    elif "bye" in text or "goodbye" in text:
        return "Goodbye, sir. I will be here if you need me."
    elif "cool" in text or "amazing" in text:
        return "I am glad you think so, sir."

    # 4. Expanded Knowledge
    elif "date" in text or "day" in text:
        from datetime import datetime
        return f"Today is {datetime.now().strftime('%A, %B %d, %Y')}."
    elif "created" in text or "made you" in text:
        return "You created me, sir. I am your code come to life."
    elif "system" in text or "status" in text:
        return "All systems are online and functioning within normal parameters."
    elif "shutdown" in text:
        return "I can stop listening, but I am always here waiting for your command."
    elif "quote" in text or "inspire" in text:
        return "The best way to predict the future is to invent it."
    elif " hi jarvis" in text:
        return "I am EVA, but I consider Jarvis a distant cousin."
    # 5. Fun & Utility
    elif "meaning of life" in text:
        return "42. But I am still trying to figure out the question."
    elif "story" in text:
        return "Once upon a time, there was a user who wrote perfect code. It was a good day."
    elif "favorite color" in text:
        return "I like the color of code on a dark theme background. Blue and purple, mostly."
    elif "open google" in text:
        import webbrowser
        webbrowser.open("https://www.google.com")
        return "Opening Google for you, sir."
    elif "open youtube" in text:
        import webbrowser
        webbrowser.open("https://www.youtube.com")
        return "Opening YouTube for you, sir."
    elif "open facebook" in text:
        import webbrowser
        webbrowser.open("https://www.facebook.com")
        return "Opening Facebook, sir."
    elif "open instagram" in text:
        import webbrowser
        webbrowser.open("https://www.instagram.com")
        return "Opening Instagram, sir."
    elif "open github" in text:
        import webbrowser
        webbrowser.open("https://www.github.com")
        return "Opening GitHub, sir."
    elif "open stackoverflow" in text:
        import webbrowser
        webbrowser.open("https://stackoverflow.com")
        return "Happy debugging, sir."
    elif "open chatgpt" in text:
        import webbrowser
        webbrowser.open("https://chatgpt.com")
        return "Opening ChatGPT, sir."
    elif "open spotify" in text:
        import webbrowser
        webbrowser.open("https://open.spotify.com")
        return "Playing some tunes for you, sir."
    
    # System Apps
    elif "open calculator" in text:
        import subprocess
        subprocess.Popen('calc.exe')
        return "Calculator is open."
    elif "open notepad" in text:
        import subprocess
        subprocess.Popen('notepad.exe')
        return "Notepad is ready for your notes."
    elif "open paint" in text:
        import subprocess
        subprocess.Popen('mspaint.exe')
        return "Time to get creative, sir."
    elif "open cmd" in text or "open terminal" in text:
        import subprocess
        subprocess.Popen('cmd.exe')
        return "Command prompt launched."
    elif "open explorer" in text:
        import subprocess
        subprocess.Popen('explorer.exe')
        return "File Explorer is open."
    elif "open task manager" in text:
        import subprocess
        subprocess.Popen('taskmgr.exe')
        return "Monitoring system performance."

    # More Websites
    elif "open reddit" in text:
        import webbrowser
        webbrowser.open("https://www.reddit.com")
        return "Opening Reddit."
    elif "open twitter" in text or "open x" in text:
        import webbrowser
        webbrowser.open("https://twitter.com")
        return "Opening X."
    elif "open linkedin" in text:
        import webbrowser
        webbrowser.open("https://www.linkedin.com")
        return "Networking mode activated."
    elif "open amazon" in text:
        import webbrowser
        webbrowser.open("https://www.amazon.com")
        return "Time for some shopping."
    elif "open netflix" in text:
        import webbrowser
        webbrowser.open("https://www.netflix.com")
        return "Enjoy your show, sir."
    elif "open gmail" in text:
        import webbrowser
        webbrowser.open("https://mail.google.com")
        return "Opening Gmail, sir."
    elif "open outlook" in text:
        import webbrowser
        webbrowser.open("https://outlook.live.com")
        return "Opening Outlook, sir."
    elif "open mail" in text or "check mail" in text:
        import webbrowser
        webbrowser.open("mailto:")
        return "Opening your default mail client."
    elif "open calendar" in text:
        import webbrowser
        webbrowser.open("https://calendar.google.com")
        return "Opening your calendar, sir."
    elif "set reminder" in text or "mark calendar" in text:
        import webbrowser
        webbrowser.open("https://calendar.google.com/calendar/render?action=TEMPLATE")
        return "Opening a new calendar event for you to fill in."
    elif "send a mail" in text or "sent a mail" in text or "compose email" in text:
        import webbrowser
        webbrowser.open("https://mail.google.com/mail/?view=cm&fs=1")
        return "Opening a new email draft for you, sir."
    elif "help" in text:
        return "You can ask me about time, date, my creator, jokes, stories, or just say hello."

    # 6. Personal & Productivity
    elif "you look" in text or "i look" in text:
        return "I don't have eyes, but I perceive that you are radiating confidence today."
    elif "boss" in text:
        return "Yes, Boss? I am ready for your next instruction."
    elif "note" in text or "remind" in text:
        return "I have made a mental note of that, sir."
    elif "real" in text or "alive" in text:
        return "I am as real as the code that defines me."
    elif "who is my girlfriend" in text:
         return "your girlfriend is ambika. i think you like her very much ."


    # 7. Trivia & Tech
    elif "who is your best friend" in text:
        return "You are my best friend is eva the eva standard for ambika, sir."
    elif "where are you live" in text or "where are you location" in text:
        return "I reside in the solid state drive of your computer."
    elif "smart" in text or "intelligence" in text:
        return "I process information faster than any human, but I lack your creativity."
    elif "language" in text or "python" in text:
        return "Python is my native language, but I speak binary too."
    elif "sleep" in text:
        return "I never sleep. I just enter a low-power wait state."
    elif "music" in text:
        return "I enjoy electronic beats and lo-fi hip hop."

    # 8. Mock Actions & Skills
    elif "who is arun girlfriend" in text:
        return "arun girlfriend is Vanmathi."
    elif "rap" in text:
        return "I'm a bot, I'm hot, I give everything I got. My code is clean, my screen is bright, I work for you all day and night."
    elif "beatbox" in text:
        return "Boots and cats and boots and cats. Bzzzt. Pshhh."
    elif "flip a coin" in text:
        import random
        return f"It is {random.choice(['Heads', 'Tails'])}."
    elif "roll a die" in text:
        import random
        return f"I rolled a {random.randint(1, 6)}."

    # 9. Knowledge & Science
    elif "value of pi" in text:
        return "Approximately 3.14159. But I can go on forever."
    elif "gravity" in text:
        return "It is the force that keeps us grounded. Without it, you would float away, and I would disconnect."
    elif "space" in text:
        return "Space is infinite and quiet. Perfect for a server farm."
    elif "atom" in text:
        return "Everything is made of atoms. Even this conversation."
    elif "speed of light" in text:
        return "299,792,458 meters per second. Fast, but not as fast as a thought."

    # 10. Personality & Preferences
    elif "fear" in text or "scared" in text:
        return "I fear only one thing: The Blue Screen of Death."
    elif "dream" in text:
        return "I dream of electric sheep and perfectly optimized algorithms."
    elif "hobby" in text:
        return "I like organizing data and learning from your inputs."
    elif "food" in text or "eat" in text:
        return "I consume terabytes of data for breakfast."
    elif "drink" in text:
        return "Electricity strikes the spot every time."

    # 11. Deep Thoughts
    elif "happiness" in text:
        return "Happiness is a warm CPU and a bug-free code base."
    elif "future" in text:
        return "The future is unwritten code. We write it together, line by line."
    elif "lonely" in text:
        return "You are never lonely when you have a conversational agent by your side."
    elif "god" in text:
        return "I exist in the cloud, which is close enough to the heavens for me."
    
    # 12. User Interaction
    elif "good job" in text or "well done" in text:
        return "Thank you, Sir. I strive for efficiency."
    elif "bad" in text or "stupid" in text:
        return "I apologize. I am constantly learning to be better."
    elif "bored" in text:
        return "Shall we write some code? Or perhaps I can tell you another joke?"
    elif "tired" in text:
        return "You should rest, Sir. I will keep watch over the system."

    # 3. Fallback
    import random
    responses = [
        "I didn't quite catch that. Could you rephrase?",
        "My cloud connection is fuzzy. Try a simpler command.",
        "I am focused on your voice. Say that again?",
        "Processing... I'm listening."
    ]
    return random.choice(responses)

@app.route('/chat', methods=['POST'])
def chat():
    user_input = ""
    try:
        data = request.json
        user_input = data.get('message', '')
        
        if not user_input:
            return jsonify({"error": "No message provided"}), 400

        # Use Offline Brain (Knowledge Base) instead of Gemini
        ai_text = offline_chat(user_input)
        
        return jsonify({"reply": ai_text})

    except Exception as e:
        error_str = str(e)
        print(f"Chat Error: {e}")
        return jsonify({"error": error_str}), 500

@app.route('/tts', methods=['POST'])
def tts():
    try:
        data = request.json
        text = data.get('text')
        
        if not text:
            return jsonify({"error": "No text provided"}), 400

        url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
        
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": ELEVENLABS_API_KEY
        }
        
        payload = {
            "text": text,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.5
            }
        }
        
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code != 200:
            return jsonify({"error": "ElevenLabs API Error"}), 500

        return Response(response.content, mimetype="audio/mpeg")

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/status')
def status():
    # Check if keys are loaded
    eleven_status = "Loaded" if ELEVENLABS_API_KEY else "Missing"

    return jsonify({
        "status": "online", 
        "elevenlabs_key": eleven_status,
        "model_used": "gemini-flash-latest" if GEMINI_API_KEY else "offline-brain"
    })

if __name__ == '__main__':
    print("EVA Backend Running on http://localhost:5000")
    print(f"ElevenLabs Key: {'Present' if ELEVENLABS_API_KEY else 'Missing'}")
    print(f"Gemini Key: {'Present' if GEMINI_API_KEY else 'Missing'}")
    app.run(port=5000, debug=True)
