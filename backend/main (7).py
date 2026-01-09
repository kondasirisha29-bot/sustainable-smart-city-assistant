from fastapi import FastAPI
from pydantic import BaseModel
import requests
import random
import datetime

app = FastAPI()

# ✅ API Keys
HF_API_KEY = "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"
WEATHER_API_KEY = "4a43426d0ad0a654181c29ece16ecbe9"

# ✅ Hugging Face Model URLs
CHAT_MODEL_URL = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"
ECOTIP_MODEL_URL = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"
POLICY_SUMMARY_MODEL_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"

headers = {"Authorization": f"Bearer {HF_API_KEY}"}

# ✅ Chat Assistant
class ChatRequest(BaseModel):
    question: str

@app.post("/chat/ask")
def chat_assistant(request: ChatRequest):
    payload = {"inputs": request.question}
    response = requests.post(CHAT_MODEL_URL, headers=headers, json=payload)
    if response.status_code == 200:
        output = response.json()
        return {"answer": output[0]["generated_text"]}
    else:
        return {"error": f"Chat API Error: {response.status_code}. Response: {response.text}"}

# ✅ Eco Tip
class EcoTipRequest(BaseModel):
    topic: str

@app.post("/eco/tips")
def generate_eco_tip(request: EcoTipRequest):
    prompt = f"Give me one short eco-friendly tip about {request.topic}."
    payload = {"inputs": prompt}
    response = requests.post(ECOTIP_MODEL_URL, headers=headers, json=payload)
    if response.status_code == 200:
        output = response.json()
        return {"tip": output[0]["generated_text"]}
    else:
        return {"error": f"Eco Tip API Error: {response.status_code}. Response: {response.text}"}

# ✅ Feedback
class FeedbackRequest(BaseModel):
    name: str
    message: str

@app.post("/feedback/submit")
def submit_feedback(feedback: FeedbackRequest):
    print(f"Feedback from {feedback.name}: {feedback.message}")
    return {"status": "Feedback received successfully"}

# ✅ Policy Summarizer
class PolicyText(BaseModel):
    text: str

@app.post("/policy/summarize")
def summarize_policy(req: PolicyText):
    payload = {"inputs": req.text}
    response = requests.post(POLICY_SUMMARY_MODEL_URL, headers=headers, json=payload)
    if response.status_code == 200:
        output = response.json()
        return {"summary": output[0]["summary_text"]}
    else:
        return {"error": f"Policy Summarizer API Error: {response.status_code}. Response: {response.text}"}

# ✅ Weather Data
@app.get("/weather/get")
def get_weather(city: str):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            "Temperature": f"{data['main']['temp']}°C",
            "Humidity": f"{data['main']['humidity']}%",
            "Weather": data['weather'][0]['description'].title()
        }
    else:
        return {"error": f"Weather API Error: {response.status_code} - {response.text}"}

# ✅ KPI Forecast (Water & Energy Only)
@app.get("/kpi/forecast")
def kpi_forecast(city: str):
    try:
        weather_url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={WEATHER_API_KEY}&units=metric"
        weather_response = requests.get(weather_url).json()

        next_temp = weather_response['list'][0]['main']['temp']
        next_humidity = weather_response['list'][0]['main']['humidity']

        estimated_water_usage = round(75000 + (next_temp * 500))
        estimated_energy_usage = round(10000 + (next_humidity * 50))

        return {
            "Forecast Temperature (°C)": next_temp,
            "Forecast Humidity (%)": next_humidity,
            "Estimated Water Usage (Liters)": estimated_water_usage,
            "Estimated Energy Consumption (kWh)": estimated_energy_usage
        }
    except Exception as e:
        return {"error": str(e)}

# ✅ Dynamic Sustainability Report
@app.get("/sustainability/report")
def get_sustainability_report(city: str):
    carbon_reduction = f"Reduced by {random.randint(5, 20)}%"
    recycling_rate = f"{random.randint(40, 80)}%"
    green_spaces = f"{random.randint(5, 20)} new parks added"
    ev_stations = random.randint(50, 200)

    return {
        "City": city.title(),
        "Carbon Emissions": carbon_reduction,
        "Recycling Rate": recycling_rate,
        "Green Spaces": green_spaces,
        "EV Charging Stations": ev_stations
    }

# ✅ Dynamic Anomaly Detection
@app.get("/anomaly/check")
def anomaly_check(city: str):
    today = datetime.date.today()
    anomaly_types = ["Energy Spike", "Water Leakage", "Traffic Surge", "Power Outage", "Air Quality Drop"]
    severity_levels = ["Low", "Medium", "High"]

    anomalies = []
    for i in range(3):
        anomalies.append({
            "Date": str(today - datetime.timedelta(days=i)),
            "Type": random.choice(anomaly_types),
            "Severity": random.choice(severity_levels),
            "City": city
        })

    return {"city": city, "anomalies": anomalies}
