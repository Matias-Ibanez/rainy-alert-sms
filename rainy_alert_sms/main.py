from dotenv import load_dotenv
import os
import requests
from vonage import Vonage, Auth

load_dotenv()

MY_KEY = os.getenv("OPENWEATHER_API_KEY")
VONAGE_KEY = os.getenv("VONAGE_API_KEY")
VONAGE_SECRET = os.getenv("VONAGE_API_SECRET")

parameters = {
    'appid' : MY_KEY,
    'lat' : -26.830139,
    'lon' : -65.225670,
    'cnt': 4
}

def is_rainy() -> bool:
    for hour_data in weather_data['list']:
        if hour_data['weather'][0]['id'] < 700:
            return True
    return False

response = requests.get(url="https://api.openweathermap.org/data/2.5/forecast", params=parameters)
response.raise_for_status()

weather_data = response.json()

if is_rainy():
    print("Rainy!")

    auth = Auth(api_key=VONAGE_KEY, api_secret=VONAGE_SECRET)
    client = Vonage(auth=auth)

    responseData = client.sms.send(
        {
            "from_": "Vonage APIs",
            "to": "Number",
            "text": "Va a llover, llevar paraguas papilo ",
        }
    )

    data = responseData.model_dump()
    if data["messages"][0]["status"] == "0":
        print("SMS sent successfully!")
    else:
        print(f"Message failed with error: {responseData['messages'][0]['error-text']}")








