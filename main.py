import os

from dotenv import load_dotenv
from pathlib import Path

# import agent
from agent import Agent

# local files:
from gui import *

def load_secrets():
    load_dotenv()
    env_path = Path(".") / ".env"
    load_dotenv(dotenv_path=env_path)

    openai_api_key = os.getenv("OPENAI_API_KEY")
    google_palm_key = os.getenv("GOOGLE_PALM_API_KEY")

    return {
        "OPENAI_API_KEY": openai_api_key,
        "GOOGLE_PALM_API_KEY": google_palm_key,
    }



if __name__ == "__main__":
    secrets = load_secrets()
    travel_agent = Agent(openai_api_key=secrets["OPENAI_API_KEY"], debug=False)
    app = TravelGuideApp(travel_agent) # ao passarmos isto para a App fazemos os pedidos acontecerem na frontend basicamente (acho eu)
    app.chat_text.tag_configure("user", foreground="blue", font=("Helvetica", 12, "bold"))
    app.chat_text.tag_configure("travelagent", foreground="green", font=("Helvetica", 12, "italic"))
    app.mainloop()
