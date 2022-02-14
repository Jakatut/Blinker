import os

from blinkpy.blinkpy import Blink
from blinkpy.auth import Auth
from dotenv import load_dotenv

class BlinClient:
    def __init__(self, username, password) -> None:
        

### Setup

# Load our .env file for secrets
load_dotenv()

# Initialize our Blink system.
blink = Blink()
auth = Auth({"username": os.getenv("BLINK_USERNAME"), "password": os.getenv("BLINK_PASSWORD")}, no_prompt=True)
opts = {"retries": 10, "backoff": 2}
auth.session = auth.create_session(opts=opts)
blink.auth = auth
blink.start()

auth.send_auth_key(blink, "969752")
blink.setup_post_verify()
blink.save(os.getenv("BLINK_CREDENTIALS_PATH"))

for name, camera in blink.cameras.items():
    print(name)
    print(camera.attributes)