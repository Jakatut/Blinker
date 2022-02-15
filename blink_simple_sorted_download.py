from datetime import datetime
import os

from blinkpy.blinkpy import Blink
from blinkpy.auth import Auth
from dotenv import load_dotenv

base_blink_storage_path = '/media/conor/Blink Videos/'
last_read_time_file_name = 'last_read_time.txt'

def getLastReadTime() -> str:
    with open(base_blink_storage_path + last_read_time_file_name) as file:
        last_read = file.read()
        print("last read: " + last_read)
        if not last_read:        
            # There would most likely not be any new videos at the current time so exit the program and try again later.
            saveNewLastReadTime()
            exit()
        return last_read

def downloadVideos(blink: Blink, last_read: str):
    # Iterate over each camera and store the videos in the camera's directory.
    for camera_name, _ in blink.cameras.items():
        print(f'Downloading videos for camera {camera_name}')
        camera_base_storage_path = f'/media/conor/Blink Videos/{camera_name}/'
        # since in the format of 2018/07/04 09:34 (Y/m/d H:M)
        blink.download_videos(camera_base_storage_path, since=f'{last_read}', delay=2, camera=camera_name)
        sortVideos(camera_name, camera_base_storage_path)

def sortVideos(camera_name, camera_base_storage_path: str):
    # After all are downloaded, iterate over the files in the cameras directroy, pull the date (YYYY-MM-DD)
    # and create a directory for that date if one does not already exist.
    # Then, move the videos in the original download path to the directory for that videos specific day.
    for _, _, files in os.walk(camera_base_storage_path):
        for file in files:
            # Change from format g8t1-9000-0301-5s9b-2022-02-14t01-18-43-00-00.mp4 to 2022-02-14
            video_date = file.replace(camera_name.lower() + '-', '').replace("-00-00.mp4", '').split(sep='t')[0]

            # Move the videos to their correct location.
            os.makedirs(camera_base_storage_path + video_date, exist_ok=True)
            os.replace(camera_base_storage_path + file, camera_base_storage_path + video_date + '/' + file)

def saveNewLastReadTime():
    # Save the last read time to files.
    last_read_time_file = open(base_blink_storage_path + 'last_read_time.txt', 'w')
    last_read_time_file.write(datetime.now().strftime("%Y/%m/%d %H:%M"))

def setup() -> Blink:
    load_dotenv()

    # Initialize our Blink system.
    blink = Blink()
    auth = Auth({"username": os.getenv("BLINK_USERNAME"), "password": os.getenv("BLINK_PASSWORD")}, no_prompt=True)
    opts = {"retries": 10, "backoff": 2}
    auth.session = auth.create_session(opts=opts)
    blink.auth = auth
    blink.start()
    auth.send_auth_key(blink, "633585")
    blink.setup_post_verify()

    return blink

def run():
    print("Setup...")
    blink = setup()
    print()
    print("Checking last read time...")
    last_read = getLastReadTime()
    print("Downloading videos..")
    downloadVideos(blink, last_read)
    print()
    print("Saving new read time...")
    saveNewLastReadTime()
    print()
    print("Done!")

run()