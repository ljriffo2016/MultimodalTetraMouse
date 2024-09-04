import numpy as np
import cv2
from threading import Thread
import mediapipe as mp
from PIL import Image
import time as ti
import win32api as winapi
import win32con as wincon
import keyboard as kb
from funcionesAuxiliares import distanciaEntrePuntos
import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk
import imutils
import pyautogui
import multiprocessing as multi
import ctypes

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

class MultimodalInterface:
    def __init__(self, root, enable, modo, botonAumentar, botonDisminuir, botonAumentarY, botonDisminuirY):
        self.root = root
        self.root.title("Prototipo Multimodal")
        self.root.geometry("1122x528+200+10")
        self.root.resizable(False, False)

        self.enable = enable
        self.modo = modo
        self.botonAumentar = botonAumentar
        self.botonDisminuir = botonDisminuir
        self.botonAumentarY = botonAumentarY
        self.botonDisminuirY = botonDisminuirY

        self.setup_background()
        self.setup_mode_buttons()
        self.setup_sensitivity_buttons()
        self.setup_video_label()

    def setup_background(self):
        self.background = PhotoImage(file="plantilla_interfaz v2.png")
        background_label = tk.Label(self.root, image=self.background)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

    def setup_mode_buttons(self):
        modes = [
            ("Joystick dual", lambda: self.change_mode(1)),
            ("Webcam y\nsip and puff", lambda: self.change_mode(2)),
            ("Joystick y\nsip and puff", lambda: self.change_mode(3))
        ]

        for i, (text, command) in enumerate(modes):
            btn = tk.Button(self.root, text=text, width=14, height=3, font=("Helvetica", 15), command=command)
            btn.grid(row=i, column=0, padx=(690, 0), pady=(27 if i == 0 else 20, 0))

        keyboard_btn = tk.Button(self.root, text="Abrir Teclado", width=12, height=3, font=("Helvetica", 15), command=self.open_keyboard)
        keyboard_btn.grid(row=3, column=0, padx=(920, 0), pady=(20, 0))

    def setup_sensitivity_buttons(self):
        sensitivities = [("X", "Joystick"), ("Y", "Joystick"), ("X", "Webcam"), ("Y", "Webcam")]
        
        for i, (axis, mode) in enumerate(sensitivities):
            row = i // 2 * 2
            col = i % 2 * 2 + 1
            padx = (925, 0) if col == 1 else (0, 0)
            pady = (25 if row == 0 else 180, 0) if col == 1 else (0, 0)

            minus_btn = tk.Button(self.root, text="-", width=3, height=1, font=("Helvetica", 15),
                                  command=lambda a=axis, m=mode: self.change_sensitivity(a, m, -1))
            minus_btn.grid(row=row, column=col, padx=padx, pady=pady)

            plus_btn = tk.Button(self.root, text="+", width=3, height=1, font=("Helvetica", 15),
                                 command=lambda a=axis, m=mode: self.change_sensitivity(a, m, 1))
            plus_btn.grid(row=row, column=col+1, padx=(0, 0), pady=pady)

    def setup_video_label(self):
        self.video_label = tk.Label(self.root)
        self.video_label.grid(row=0, column=1, rowspan=4, padx=(20, 0), pady=(19, 0))

    def change_mode(self, new_mode):
        self.modo.value = new_mode

    def change_sensitivity(self, axis, mode, direction):
        if mode == "Joystick":
            if axis == "X":
                self.botonAumentar.value = 2 if direction > 0 else 0
                self.botonDisminuir.value = 2 if direction < 0 else 0
            else:
                self.botonAumentarY.value = 2 if direction > 0 else 0
                self.botonDisminuirY.value = 2 if direction < 0 else 0
        else:
            if axis == "X":
                self.botonAumentar.value = 1 if direction > 0 else 0
                self.botonDisminuir.value = 1 if direction < 0 else 0
            else:
                self.botonAumentarY.value = 1 if direction > 0 else 0
                self.botonDisminuirY.value = 1 if direction < 0 else 0

    def open_keyboard(self):
        pyautogui.keyDown("ctrl")
        pyautogui.keyDown("winleft")
        pyautogui.press("o")
        ti.sleep(0.05)
        pyautogui.keyUp("ctrl")
        ti.sleep(0.05)
        pyautogui.keyUp("winleft")

def interfaz(enable, modo, botonAumentar, botonDisminuir, botonAumentarY, botonDisminuirY):
    root = tk.Tk()
    app = MultimodalInterface(root, enable, modo, botonAumentar, botonDisminuir, botonAumentarY, botonDisminuirY)
    root.mainloop()

def main(enable, success, close, modo, new_screen_x, new_screen_y, reset_modo3, clic_modo3, clic_puff_act, botonAumentar, botonDisminuir, botonAumentarY, botonDisminuirY, estado_joystick, estado_sip, Xjoy, Yjoy):
    # Main function implementation (as in the original code)
    pass

def Principal(enable, success, close, modo, new_screen_x, new_screen_y, reset_modo3, clic_modo3, estado_joystick, Xjoy, Yjoy):
    # Principal function implementation
    pass

if __name__ == '__main__':
    if is_admin():
        multi.freeze_support()
        enable = multi.Value('i', 1)
        modo = multi.Value('i', 1)
        success = multi.Value('i', 1)
        close = multi.Value('i', 0)
        new_screen_x = multi.Value('i', 0)
        new_screen_y = multi.Value('i', 0)
        reset_modo3 = multi.Value('i', 0)
        clic_modo3 = multi.Value('i', 0)
        clic_puff_act = multi.Value('i', 1)
        botonAumentar = multi.Value('i', 0)
        botonDisminuir = multi.Value('i', 0)
        botonAumentarY = multi.Value('i', 0)
        botonDisminuirY = multi.Value('i', 0)
        Xjoy = multi.Value('i', 10)
        Yjoy = multi.Value('i', 10)
        
        estado_joystick = multi.Value('i', 0)
        estado_sip = multi.Value('i', 0)

        p1 = multi.Process(target=main, args=(enable, success, close, modo, new_screen_x, new_screen_y, reset_modo3, clic_modo3, clic_puff_act, botonAumentar, botonDisminuir, botonAumentarY, botonDisminuirY, estado_joystick, estado_sip, Xjoy, Yjoy))
        p3 = multi.Process(target=Principal, args=(enable, success, close, modo, new_screen_x, new_screen_y, reset_modo3, clic_modo3, estado_joystick, Xjoy, Yjoy))
        p4 = multi.Process(target=interfaz, args=(enable, modo, botonAumentar, botonDisminuir, botonAumentarY, botonDisminuirY))

        p1.start()
        p3.start()
        p4.start()

        p1.join()
        p3.join()
        p4.join()
    else:
        print("This script must be run with administrator privileges.")