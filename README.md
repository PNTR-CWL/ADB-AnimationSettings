# ADB-AnimationSettings

A small utility for changing animation scale settings on Android devices via ADB using a simple GUI built with Python and Tkinter.

It allows modifying the following developer settings:
- `window_animation_scale`
- `transition_animation_scale`
- `animator_duration_scale`

These values affect the speed of animations such as window transitions, activity launches, and notification panel behavior.

---

## Features

- Connects to a device over ADB and waits for connection if none is found
- Adjustable sliders with default range from 0.0 to 2.0
- Optional "ABSURD MODE" that extends the slider range up to 20.0
- Displays custom toast-like popup messages on success/failure
- Fixed-size dark-themed GUI

---

## Screenshot

![Screenshot](https://github.com/PNTR-CWL/ADB-AnimationSettings/blob/main/image.png)

---

## Requirements
- USB Debugging must be enabled on the connected Android device

---

## How to Use

1. Connect an Android device with USB debugging enabled.
2. Download and extract the [ZIP file](https://github.com/PNTR-CWL/ADB-AnimationSettings/blob/f3688ac7474d073a8f2638c1fe03ce3cf2779d62/ADB%20AnimationSettings.zip).
3. Run `ADB-AnimationSettings.exe`.

The app will wait for a device if none is connected. Once a device is detected, you can adjust animation scales using the sliders and click "Apply".

---

## Build Instructions (Optional)

To build the project into an executable:

**Requirements:**
- Python 3.10 or newer
- `pyinstaller` for packaging
- Tkinter (should come with Python)

**Build Command:**
```bash
pyinstaller --onefile --noconsole ADB-AnimationSettings.py
