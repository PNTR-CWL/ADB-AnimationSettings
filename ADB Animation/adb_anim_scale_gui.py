import tkinter as tk
from tkinter import ttk
import subprocess
import threading
import time

absurd_mode = False
root = tk.Tk()
root.geometry("450x480")
root.resizable(False, False)
root.title("ADB Animation Scale Controller")

# --- DARK THEME COLORS ---
BG_COLOR = "#121212"
FG_COLOR = "#E0E0E0"
SLIDER_BG = "#333333"
SLIDER_FG = "#BBBBBB"
BUTTON_BG = "#222222"
BUTTON_FG = "#E0E0E0"
TITLE_COLOR = "#FFFFFF"

root.configure(bg=BG_COLOR)

window_scale = None
transition_scale = None
animator_scale = None
mode_button = None
title_label = None

def show_toast(message, duration=2000, bg_color="#333", fg_color="#fff"):
    toast = tk.Toplevel(root)
    toast.overrideredirect(True)
    toast.attributes("-topmost", True)
    toast.configure(bg=bg_color)

    label = tk.Label(toast, text=message, bg=bg_color, fg=fg_color, font=("Helvetica", 10))
    label.pack(ipadx=10, ipady=5)

    root_x = root.winfo_rootx()
    root_y = root.winfo_rooty()
    root_w = root.winfo_width()
    root_h = root.winfo_height()

    toast.update_idletasks()
    w = toast.winfo_width()
    h = toast.winfo_height()

    x = root_x + root_w - w - 20
    y = root_y + root_h - h - 40
    toast.geometry(f"{w}x{h}+{x}+{y}")

    toast.after(duration, toast.destroy)

def is_device_connected():
    try:
        result = subprocess.run(
            ["adb", "get-state"],
            capture_output=True,
            text=True,
            timeout=2,
            creationflags=subprocess.CREATE_NO_WINDOW  # <-- dodane
        )
        return "device" in result.stdout.strip().lower()
    except Exception:
        return False

def set_animation_scales(window_val, transition_val, animator_val):
    try:
        subprocess.run(
            ["adb", "shell", "settings", "put", "global", "window_animation_scale", str(window_val)],
            check=True,
            creationflags=subprocess.CREATE_NO_WINDOW  # <-- dodane
        )
        subprocess.run(
            ["adb", "shell", "settings", "put", "global", "transition_animation_scale", str(transition_val)],
            check=True,
            creationflags=subprocess.CREATE_NO_WINDOW  # <-- dodane
        )
        subprocess.run(
            ["adb", "shell", "settings", "put", "global", "animator_duration_scale", str(animator_val)],
            check=True,
            creationflags=subprocess.CREATE_NO_WINDOW  # <-- dodane
        )
        show_toast("Animation scales set successfully!", duration=2500, bg_color="#4CAF50")
    except subprocess.CalledProcessError:
        show_toast("Failed to set animation scales.", duration=2500, bg_color="#f44336")

def get_current_animation_scales():
    def get_scale(setting):
        try:
            result = subprocess.run(
                ["adb", "shell", "settings", "get", "global", setting],
                capture_output=True,
                text=True,
                timeout=2,
                creationflags=subprocess.CREATE_NO_WINDOW  # <-- dodane
            )
            return float(result.stdout.strip())
        except Exception:
            return 1.0
    return (
        get_scale("window_animation_scale"),
        get_scale("transition_animation_scale"),
        get_scale("animator_duration_scale")
    )

def apply():
    win = window_scale.get()
    trans = transition_scale.get()
    anim = animator_scale.get()
    set_animation_scales(win, trans, anim)

def toggle_mode():
    global absurd_mode
    absurd_mode = not absurd_mode
    if absurd_mode:
        new_to = 20.0
        mode_button.config(text="Switch to Normal Mode (0–2)")
        title_label.config(text="ABSURD MODE ACTIVATED 🔥")
    else:
        new_to = 2.0
        mode_button.config(text="Switch to ABSURD MODE (0–20)")
        title_label.config(text="ADB Animation Scale Controller")

    for scale in [window_scale, transition_scale, animator_scale]:
        current = scale.get()
        scale.config(to=new_to)
        if current > new_to:
            scale.set(new_to)

def style_scale_widget(scale):
    scale.config(bg=BG_COLOR, fg=FG_COLOR, troughcolor=SLIDER_BG, highlightthickness=0)
    scale["sliderrelief"] = "flat"
    # Unfortunately Tkinter's native Scale doesn't support detailed styling per element, but this is a decent base.

def show_main_ui():
    global window_scale, transition_scale, animator_scale, mode_button, title_label

    for widget in root.winfo_children():
        widget.destroy()

    # Pobierz aktualne wartości animacji z urządzenia
    win_val, trans_val, anim_val = get_current_animation_scales()

    # --- HELP ICON ---
    help_icon = tk.Label(root, text="?", font=("Helvetica", 13, "bold"), fg="#2196F3", bg=BG_COLOR, cursor="question_arrow")
    help_icon.place(x=420, y=10, width=20, height=20)

    tooltip = tk.Toplevel(root)
    tooltip.withdraw()
    tooltip.overrideredirect(True)
    tooltip.configure(bg="#222", padx=8, pady=5)
    tip_label = tk.Label(tooltip, text="If you set the value to 0, animations will be disabled.",
                         bg="#222", fg="#fff", font=("Helvetica", 9))
    tip_label.pack()

    def show_tooltip(event):
        x = help_icon.winfo_rootx() + 20
        y = help_icon.winfo_rooty() + 20
        tooltip.geometry(f"+{x}+{y}")
        tooltip.deiconify()

    def hide_tooltip(event):
        tooltip.withdraw()

    help_icon.bind("<Enter>", show_tooltip)
    help_icon.bind("<Leave>", hide_tooltip)

    title_label = tk.Label(root, text="ADB Animation Scale Controller", font=("Helvetica", 14, "bold"), fg=TITLE_COLOR, bg=BG_COLOR)
    title_label.pack(pady=10)

    tk.Label(root, text="Window animation scale", fg=FG_COLOR, bg=BG_COLOR).pack(pady=5)
    window_scale = tk.Scale(root, from_=0.0, to=2.0, resolution=0.05, orient=tk.HORIZONTAL, length=400)
    window_scale.set(win_val)
    style_scale_widget(window_scale)
    window_scale.pack()

    tk.Label(root, text="Transition animation scale", fg=FG_COLOR, bg=BG_COLOR).pack(pady=5)
    transition_scale = tk.Scale(root, from_=0.0, to=2.0, resolution=0.05, orient=tk.HORIZONTAL, length=400)
    transition_scale.set(trans_val)
    style_scale_widget(transition_scale)
    transition_scale.pack()

    tk.Label(root, text="Animator duration scale", fg=FG_COLOR, bg=BG_COLOR).pack(pady=5)
    animator_scale = tk.Scale(root, from_=0.0, to=2.0, resolution=0.05, orient=tk.HORIZONTAL, length=400)
    animator_scale.set(anim_val)
    style_scale_widget(animator_scale)
    animator_scale.pack()

    apply_btn = tk.Button(root, text="Apply", command=apply, bg=BUTTON_BG, fg=BUTTON_FG, activebackground="#555555", relief="flat")
    apply_btn.pack(pady=15)

    mode_button = tk.Button(root, text="Switch to ABSURD MODE (0–20)", command=toggle_mode, bg=BUTTON_BG, fg=BUTTON_FG, activebackground="#555555", relief="flat")
    mode_button.pack()

    # --- GITHUB LINK ---
    github_link = tk.Label(
        root,
        text="View on GitHub",
        fg="#2196F3",
        bg=BG_COLOR,
        cursor="hand2",
        font=("Helvetica", 10, "underline")
    )
    github_link.pack(pady=(30, 10))

    def open_github(event):
        import webbrowser
        webbrowser.open_new("https://github.com/PNTR-CWL/ADB-AnimationSettings")

    github_link.bind("<Button-1>", open_github)

def wait_for_device_gui():
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Waiting for ADB device...", font=("Helvetica", 12), fg=FG_COLOR, bg=BG_COLOR).pack(pady=20)
    pb = ttk.Progressbar(root, mode="indeterminate")
    pb.pack(pady=10, padx=40, fill="x")
    pb.start()

    def checker():
        while not is_device_connected():
            time.sleep(1)
        root.after(0, show_main_ui)

    threading.Thread(target=checker, daemon=True).start()

def center_window(window, width=450, height=480):
    window.update_idletasks()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")

wait_for_device_gui()
center_window(root, 450, 480)
root.mainloop()