import time
import schedule
from playsound import playsound
import threading
from datetime import datetime
import sys
import os
from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# === Settings ===
REMINDER_INTERVAL_MIN = 30 # Plays the sound every X minutes
SLEEP_HOURS = (23, 7)  # No reminders between 23:00–07:00 
SOUND_FILE = resource_path("blink.mp3") # Change path if needed.

is_paused = False

def is_sleep_time():
    hour = datetime.now().hour
    return SLEEP_HOURS[0] <= hour or hour < SLEEP_HOURS[1]

def remind_to_blink():
    if not is_paused and not is_sleep_time():
        try:
            playsound(SOUND_FILE)
        except Exception as e:
            print(f"Error playing sound: {e}")

def run_scheduler():
    schedule.every(REMINDER_INTERVAL_MIN).minutes.do(remind_to_blink)
    while True:
        schedule.run_pending()
        time.sleep(1)

# === Tray icon setup ===
def create_image():
    img = Image.new("RGB", (64, 64), "black")
    draw = ImageDraw.Draw(img)
    draw.ellipse((16, 16, 48, 48), fill="blue")
    return img

def toggle_pause(icon, item):
    global is_paused
    is_paused = not is_paused

def quit_app(icon, item):
    icon.stop()
    os._exit(0)

def setup_tray():
    icon = Icon("Blink Reminder")
    icon.icon = create_image()
    icon.menu = Menu(
        MenuItem(lambda item: "Pause" if not is_paused else "Resume", toggle_pause),
        MenuItem("Quit", quit_app)
    )
    threading.Thread(target=run_scheduler, daemon=True).start()
    icon.run()

if __name__ == "__main__":
    setup_tray()

