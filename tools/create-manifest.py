#DISCLAIMER: This code will not be able to create the following items inside the "manifest.json" file: webmodding, shaders, theme, name, developer, and description.
#Also, please note that this will only generate the manifest.json with the files inside the folder with the Code.py with the default names as given in the mode template, and can only hande up to 4 tracks.

import json, os

def Exists(string):
    return os.path.exists(string)

def Write(data, indent, file_name="manifest.json"):
    if os.path.exists(file_name):
        try:
            with open(file_name, "r") as infile:
                existing_data = json.load(infile)
        except json.JSONDecodeError:
            existing_data = {}
    else:
        existing_data = {}

    if not existing_data:
        existing_data = {
            "name": "MOD NAME GOES HERE",
            "description": "MOD DESCRIPTION GOES HERE",
            "developer": {
                "name": "DEVELOPER NAME GOES HERE"
            },
            "icons": {
                "512": "icon_512.png"
            },
            "manifest_version": 3,
            "mod": {
                "license": "license.txt",
                "payload": [],
                "schema_version": 1,
            "version": "1.0"
            }
        }

    if not isinstance(existing_data["mod"]["payload"], list):
        existing_data["mod"]["payload"] = []

    if not existing_data["mod"]["payload"]:
        existing_data["mod"]["payload"].append({
            "background_music": [],
            "browser_sounds": {},
            "keyboard_sounds": {},
            "wallpapers": {}
        })

    payload_data = existing_data["mod"]["payload"][-1]

    if "background_music" in data:
        print(f"Adding background music: {data['background_music']}")
        for music in data["background_music"]:
            if music not in payload_data["background_music"]:
                payload_data["background_music"].append(music)

    if "browser_sounds" in data:
        print(f"Adding browser sounds: {data['browser_sounds']}")
        for sound_key, sound_files in data["browser_sounds"].items():
            if sound_key not in payload_data["browser_sounds"]:
                payload_data["browser_sounds"][sound_key] = []
            for sound in sound_files:
                if sound not in payload_data["browser_sounds"][sound_key]:
                    payload_data["browser_sounds"][sound_key].append(sound)

    if "keyboard_sounds" in data:
        print(f"Adding keyboard sounds: {data['keyboard_sounds']}")
        for sound_key, sound_files in data["keyboard_sounds"].items():
            if sound_key not in payload_data["keyboard_sounds"]:
                payload_data["keyboard_sounds"][sound_key] = []
            for sound in sound_files:
                if sound not in payload_data["keyboard_sounds"][sound_key]:
                    payload_data["keyboard_sounds"][sound_key].append(sound)

    if "wallpapers" in data:
        print(f"Adding wallpapers: {data['wallpapers']}")
        for theme, wallpaper_data in data["wallpapers"].items():
            if theme not in payload_data["wallpapers"]:
                payload_data["wallpapers"][theme] = wallpaper_data

    with open(file_name, "w") as outfile:
        json.dump(existing_data, outfile, indent=indent)

    print(f"Updated '{file_name}' successfully.")


data = {
    "background_music": [],
    "browser_sounds": {},
    "keyboard_sounds": {},
    "wallpapers": {}
}

if Exists("license.txt"):
    Write({
        "name": "MOD NAME GOES HERE",
        "description": "MOD DESCRIPTION GOES HERE",
        "developer": {
            "name": "DEVELOPER NAME GOES HERE"
        },
        "icons": {
            "512": "icon_512.png"
        },
        "manifest_version": 3,
        "mod": {
            "license": "license.txt",
            "payload": []
        }
    }, 4)

if Exists("music"):
    print("Adding background music...")
    for i in range(1, 5):
        track = f"track{i}.mp3"
        path = os.path.join("music", track)
        if Exists(path):
            print(f" - Found {track}")
            data["background_music"].append(path)

if Exists("sound/click.mp3"):
    print("Adding sound: CLICK")
    data["browser_sounds"]["CLICK"] = ["sound/click.mp3"]
if Exists("sound/feature_switch_off.mp3"):
    print("Adding sound: FEATURE_SWITCH_OFF")
    data["browser_sounds"]["FEATURE_SWITCH_OFF"] = ["sound/feature_switch_off.mp3"]
if Exists("sound/feature_switch_on.mp3"):
    print("Adding sound: FEATURE_SWITCH_ON")
    data["browser_sounds"]["FEATURE_SWITCH_ON"] = ["sound/feature_switch_on.mp3"]
if Exists("sound/hover.mp3"):
    print("Adding sound: HOVER")
    data["browser_sounds"]["HOVER"] = ["sound/hover.mp3"]
    data["browser_sounds"]["HOVER_UP"] = ["sound/hover.mp3"]
if Exists("sound/important_click.mp3"):
    print("Adding sound: IMPORTANT_CLICK")
    data["browser_sounds"]["IMPORTANT_CLICK"] = ["sound/important_click.mp3"]
if Exists("sound/level_upgrade.mp3"):
    print("Adding sound: LEVEL_UPGRADE")
    data["browser_sounds"]["LEVEL_UPGRADE"] = ["sound/level_upgrade.mp3"]
if Exists("sound/limiter_off.mp3"):
    print("Adding sound: LIMITER_OFF")
    data["browser_sounds"]["LIMITER_OFF"] = ["sound/limiter_off.mp3"]
if Exists("sound/limiter_on.mp3"):
    print("Adding sound: LIMITER_ON")
    data["browser_sounds"]["LIMITER_ON"] = ["sound/limiter_on.mp3"]
if Exists("sound/switch.mp3"):
    print("Adding sound: SWITCH_TOGGLE")
    data["browser_sounds"]["SWITCH_TOGGLE"] = ["sound/switch.mp3"]
if Exists("sound/close_tab.mp3"):
    print("Adding sound: TAB_CLOSE")
    data["browser_sounds"]["TAB_CLOSE"] = ["sound/close_tab.mp3"]
if Exists("sound/new_tab.mp3"):
    print("Adding sound: TAB_INSERT")
    data["browser_sounds"]["TAB_INSERT"] = ["sound/new_tab.mp3"]
if Exists("sound/tab_slash.mp3"):
    print("Adding sound: TAB_SLASH")
    data["browser_sounds"]["TAB_SLASH"] = ["sound/tab_slash.mp3"]

if Exists("keyboard/backspace.wav"):
    print("Adding keyboard sound: BACKSPACE")
    data["keyboard_sounds"]["TYPING_BACKSPACE"] = ["keyboard/backspace.wav"]
if Exists("keyboard/enter.wav"):
    print("Adding keyboard sound: ENTER")
    data["keyboard_sounds"]["TYPING_ENTER"] = ["keyboard/enter.wav"]
if Exists("keyboard/letter_1.wav"):
    print("Adding keyboard sound: LETTER_1")
    data["keyboard_sounds"]["TYPING_LETTER_1"] = ["keyboard/letter_1.wav"]
if Exists("keyboard/letter_2.wav"):
    print("Adding keyboard sound: LETTER_2")
    data["keyboard_sounds"]["TYPING_LETTER_2"] = ["keyboard/letter_2.wav"]
if Exists("keyboard/letter_3.wav"):
    print("Adding keyboard sound: LETTER_3")
    data["keyboard_sounds"]["TYPING_LETTER_3"] = ["keyboard/letter_3.wav"]
if Exists("keyboard/space.wav"):
    print("Adding keyboard sound: SPACE")
    data["keyboard_sounds"]["TYPING_SPACE"] = ["keyboard/space.wav"]

if Exists("wallpaper/dark.png"):
    print("Adding Wallpaper: DARK")
    data["wallpapers"]["dark"] = {
        "image": "wallpaper/dark.png",
        "text_color": "#FFFFFF",
        "text_shadow": "#757575"
    }
elif Exists("wallpaper/video.webm") and not Exists("wallpaper/dark.png"):
    print("Adding Wallpaper: DARK")
    data["wallpapers"]["dark"] = {
        "image": "wallpaper/video.webm",
        "first_frame": "wallpaper/first_frame.jpeg",
        "text_color": "#FFFFFF",
        "text_shadow": "#757575"
    }

if Exists("wallpaper/light.png"):
    print("Adding Wallpaper: LIGHT")
    data["wallpapers"]["light"] = {
        "image": "wallpaper/light.png",
        "text_color": "#FFFFFF",
        "text_shadow": "#0B000E"
    }
elif Exists("wallpaper/video.webm") and not Exists("wallpaper/light.png"):
    print("Adding Wallpaper: LIGHT")
    data["wallpapers"]["LIGHT"] = {
        "image": "wallpaper/video.webm",
        "first_frame": "wallpaper/first_frame.jpeg",
        "text_color": "#FFFFFF",
        "text_shadow": "#0B000E"
    }

Write(data, 4)
input()
