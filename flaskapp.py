from flask import Flask
from dotenv import load_dotenv
from Scrappers.models import CustomJsonEncoder
import ray

load_dotenv()
ray.init()

app = Flask(__name__)
app.json_encoder = CustomJsonEncoder

import routes

if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=5000)
