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
from multiprocessing import Value, Process

stop_thread = False
img_a_procesar = None
img_original = None
img_tk = None
im = None
img = None
lblVideo = None
cap = None
ret = 0
etiq_de_video = 0
botonAumentar = 0
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh()

t_inicial2 = ti.time()
t_final = 0
frame = 0
x_origen = 0
y_origen = 0
X_MOUSE_RELATIVA_ORIGEN = 0
Y_MOUSE_RELATIVA_ORIGEN = 0
newEnable = 1
keyInterfaz = 1

filtradoX = 300
filtradoY = 300
auxfiltx = 300
auxfilty = 300

filtradoX2 = int(winapi.GetSystemMetrics(0)/2)
filtradoY2 = int(winapi.GetSystemMetrics(1)/2)
auxfiltx2 = int(winapi.GetSystemMetrics(0)/2)
auxfilty2 = int(winapi.GetSystemMetrics(1)/2)

a1 = 0.25  # para punto
a2 = 0.6  # para movimiento del mouse
a3 = 0.1  # para punto DEMA
a4 = 0.4  # para movimiento del mouse DEMA

llave = 1

EstadoJoystick = ""
EstadoSipPuff = ""

def MediaX(meaX):
    global filtradoX, a1, auxfiltx, llave, a3
    filtradoX = a1*meaX + (1 - a1)*filtradoX
    filtradoX3 = 2*filtradoX - (a3*filtradoX + (1 - a3)*auxfiltx)
    auxfiltx = filtradoX
    if llave == 0:
        return int(filtradoX3), int(filtradoX)  # usar filtro DEMA        
    elif llave == 1:
        return int(filtradoX), int(filtradoX3)  # usar filtro EMA

def MediaY(meaY):
    global filtradoY, a1, auxfilty, a3
    filtradoY = a1*meaY + (1 - a1)*filtradoY
    filtradoY3 = 2*filtradoY - (a3*filtradoY + (1 - a3)*auxfilty)
    auxfilty = filtradoY
    if llave == 0:
        return int(filtradoY3), int(filtradoY)  # usar filtro DEMA
    elif llave == 1:
        return int(filtradoY), int(filtradoY3)  # usar filtro EMA

def MediaX2(meaX2):
    global filtradoX2, a2, auxfiltx2, a4
    filtradoX2 = a2*meaX2 + (1 - a2)*filtradoX2
    filtradoX4 = 2*filtradoX2 - (a4*filtradoX2 + (1 - a4)*auxfiltx2)
    auxfiltx2 = filtradoX2
    if llave == 0:
        return int(filtradoX4)  # usar filtro DEMA
    elif llave == 1:
        return int(filtradoX2)  # usar filtro EMA

def MediaY2(meaY2):
    global filtradoY2, a2, auxfilty2, a4
    filtradoY2 = a2*meaY2 + (1 - a2)*filtradoY2
    filtradoY4 = 2*filtradoY2 - (a4*filtradoY2 + (1 - a4)*auxfilty2)
    auxfilty2 = filtradoY2
    if llave == 0:
        return int(filtradoY4)  # usar filtro DEMA
    elif llave == 1:
        return int(filtradoY2)  # usar filtro EMA

class MultimodalInterface:
    def __init__(self, root, enable, modo, botonAumentar, botonDisminuir, botonAumentarY, botonDisminuirY, close):
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
        self.close = close

        self.setup_background()
        self.setup_mode_buttons()
        self.setup_sensitivity_buttons()
        self.setup_video_label()

        self.cap = cv2.VideoCapture(0)
        self.update_video()

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

    def update_video(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.flip(frame, 1)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = imutils.resize(frame, width=640)
            photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
            self.video_label.config(image=photo)
            self.video_label.image = photo
        self.root.after(10, self.update_video)

    def on_closing(self):
        self.close.value = 1
        self.enable.value = 0
        self.root.quit()

def video_stream():
    global img_a_procesar, img_tk, lblVideo, ret, im, img, cap, frame
    if cap is not None:
        if ret == True:   
            im = Image.fromarray(img_tk)
            img = ImageTk.PhotoImage(image=im)       
            lblVideo.configure(image=img)
            lblVideo.image = img
            lblVideo.after(10, video_stream)

def start_capture_thread(cap):
    global img_original, stop_thread, img_a_procesar, t_inicial2, frame, img_tk, keyInterfaz, ret, im, img
    while True:
        ret, img_original = cap.read()
        if img_original is not None:
            img_original = cv2.flip(img_original, 1)
            img_a_procesar = img_original.copy()
            img_a_procesar = cv2.cvtColor(img_a_procesar, cv2.COLOR_BGR2RGB)
            frame = 1
        if stop_thread:
            cap.release()
            print("ME CERRE")
            break

def main(enable, success, close, modo, new_screen_x, new_screen_y, reset_modo3, clic_modo3, clic_puff_act, botonAumentar, botonDisminuir, botonAumentarY, botonDisminuirY, estado_joystick, estado_sip, Xjoy, Yjoy):
    global img_a_procesar, stop_thread, mp_face_mesh, face_mesh, frame, x1, x2, y1, y2, img_tk, img, cap, keyInterfaz, newEnable, EstadoJoystick, llave

    cap = cv2.VideoCapture(0)

    t = Thread(target=start_capture_thread, args=(cap,), daemon=True)
    t.start()
    
    root = tk.Tk()
    app = MultimodalInterface(root, enable, modo, botonAumentar, botonDisminuir, botonAumentarY, botonDisminuirY, close)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    
    t_inicial = ti.time() 
    t_boca_abierta_inicial = 0 
    contador = 0
    primer_loop = 0

    screen_x = int(winapi.GetSystemMetrics(0)/2)
    screen_y = int(winapi.GetSystemMetrics(1)/2)

    X_FILTRADO = 0
    Y_FILTRADO = 0
    t_total = 0
    auxLlave = 0
    auxReset = 0
    reset = 0
    activo = 0
    auxActivo = 0
    auxParam1_1_x = 0
    auxParam1_1_y = 0
    auxVeloX = 0
    auxVeloY = 0
    safe_zoneX = 0
    safe_zoneY = 0
    x_ant = 0
    y_ant = 0
    Mar = 0
    FPS_ANT = None
    mover_mouse = 0
    reset_mouse = 0
    param_1_1_x = 10
    param_1_1_y = 10
    velX = 1
    velY = 1
    key_aux = 0
    paramVeloX = 1
    paramVeloY = 1
    distancia_cm = 0
    distancia_px = 0
    relacion_escala_inicial = 1
    key_distancia_ojos = 1
    relación_escala_cm = 1
    keyAuxActivo = 0
    keyAuxInactivo = 0
    estado_mouse = "MOUSE DESACTIVADO"
    periodoIniciar = ti.time()

    while (newEnable == 1):
        if estado_joystick.value == 1:
            EstadoJoystick = "Joystick: DESCONECTADO"
            color_joy = (255,0,0)
        else:
            EstadoJoystick = "Joystick: CONECTADO"
            color_joy = (0,255,0)
        
        if estado_sip.value == 1:
            EstadoSipPuff = "Sip-and-Puff: DESCONECTADO"
            color_sip = (255,0,0)
        elif estado_sip.value == 0:
            EstadoSipPuff = "Sip-and-Puff: CONECTADO"
            color_sip = (0,255,0)
        elif estado_sip.value == 2: 
            EstadoSipPuff = "Sip-and-Puff: CONECTANDO..."
            color_sip = (255,255,0)

        if (img_a_procesar is not None):
            if modo.value == 3:
                modo_activo = "MODO JOYSTICK + SnP"
            elif modo.value == 2:
                modo_activo = "MODO WEBCAM + SnP"
            else:
                modo_activo = "MODO JOYSTICK DUAL"

            if modo.value == 3:
                screen_x, screen_y = new_screen_x.value, new_screen_y.value
                key_aux = 1
            elif modo.value == 2 and key_aux == 1:
                screen_x = int(winapi.GetSystemMetrics(0)/2)
                screen_y = int(winapi.GetSystemMetrics(1)/2)
                key_aux = 0  
            if frame == 1:
                height, width, _ = img_a_procesar.shape
                rgb_image = img_a_procesar.copy()
                result = face_mesh.process(rgb_image)
                color = (255,0,0)
                if activo == 0:
                    color_MAR = (0,0,255)
                else:
                    color_MAR = (0,255,0)
                try:                    
                    for facial_landmarks in result.multi_face_landmarks:
                        for i in range(0,403):   
                            if i == 4:
                                pt_nariz = facial_landmarks.landmark[i]
                                x_nariz = int(pt_nariz.x*width)
                                y_nariz = int(pt_nariz.y*height)
                     
                                if True:
                                    x_nariz, x_DEMA = MediaX(x_nariz)
                                    y_nariz, y_DEMA = MediaY(y_nariz)
                                    cv2.circle(img_a_procesar, (x_nariz,y_nariz), 5, (0,255,0), -1)
                                     
                            if i == 33:
                                pt_ojo_iz = facial_landmarks.landmark[i]
                                x_ojo_iz = int(pt_ojo_iz.x*width)
                                y_ojo_iz = int(pt_ojo_iz.y*height)
                                z_ojo_iz = pt_ojo_iz.y*distancia_px

                            if i == 263:
                                pt_ojo_der = facial_landmarks.landmark[i]
                                x_ojo_der = int(pt_ojo_der.x*width)
                                y_ojo_der = int(pt_ojo_der.y*height) 
                                z_ojo_der = pt_ojo_der.z*distancia_px

                            pt_MAR = facial_landmarks.landmark[i]
                            x = int(pt_MAR.x*width)
                            y = int(pt_MAR.y*height)  
                            
                            if i == 62:
                                p1x = x
                                p1y = y
                            if i == 81:
                                p2x = x
                                p2y = y 
                            if i == 13:
                                p3x = x 
                                p3y = y 
                            if i == 311:
                                p4x = x
                                p4y = y 
                            if i == 292:
                                p5x = x
                                p5y = y
                            if i == 402:
                                p6x = x
                                p6y = y 
                            if i == 14:
                                p7y = y
                                p7x = x 
                            if i == 178:
                                p8y = y
                                p8x = x

                    p2_p8 = distanciaEntrePuntos(p2x, p2y, p8x, p8y)*relación_escala_cm
                    p3_p7 = distanciaEntrePuntos(p3x, p3y, p7x, p7y)*relación_escala_cm
                    p4_p6 = distanciaEntrePuntos(p4x, p4y, p6x, p6y)*relación_escala_cm
                    p1_p5 = distanciaEntrePuntos(p1x, p1y, p5x, p5y)*relación_escala_cm
                    Mar = ((p2_p8+p3_p7+p4_p6)/((p1_p5)))

                    if Mar > 0.4:
                        if ti.time()-t_boca_abierta_inicial > 1 and p1_p5 > 50:
                            reset_mouse = (reset_mouse+1)%2
                            print("RESET")
                            t_boca_abierta_inicial = ti.time()
                        elif ti.time()-t_boca_abierta_inicial > 1 and Mar > 1.1 and p1_p5 < 50:
                            mover_mouse = (mover_mouse+1)%2
                            t_boca_abierta_inicial = ti.time() 
                    else:
                        t_boca_abierta_inicial = ti.time()
                        reset_mouse = 0

                    pow = np.array([2,2])
                    distancia_entre_ojos_VARIABLE = np.array([x_ojo_iz-x_ojo_der, y_ojo_iz-y_ojo_der])
                    distancia_entre_ojos_VARIABLE = np.power(distancia_entre_ojos_VARIABLE, pow)                        
                    distancia_entre_ojos_VARIABLE = np.sqrt(distancia_entre_ojos_VARIABLE[0]+distancia_entre_ojos_VARIABLE[1])
                    
                    distancia_cm = (60*80)/distancia_entre_ojos_VARIABLE
                    distancia_px = (60*80)/distancia_cm
                    if primer_loop < 60:
                        x_origen_nariz = x_nariz 
                        y_origen_nariz = y_nariz 
                        
                        x_origen_ojo_iz = x_ojo_iz
                        y_origen_ojo_iz = y_ojo_iz

                        x_origen_ojo_der = x_ojo_der 
                        y_origen_ojo_der = y_ojo_der 

                        if key_distancia_ojos == 1:
                            distancia_entre_ojos = np.array([x_origen_ojo_iz-x_origen_ojo_der, y_origen_ojo_iz-y_origen_ojo_der])                             
                            distancia_entre_ojos = np.power(distancia_entre_ojos, pow)                        
                            distancia_entre_ojos = np.sqrt(distancia_entre_ojos[0]+distancia_entre_ojos[1])
                            distancia_cm_inicial = distancia_cm   

                        primer_loop = primer_loop+1

                    relación_escala_cm = round(distancia_cm/60,1)
                    relacion_escala_entreojos = distancia_entre_ojos_VARIABLE/distancia_entre_ojos

                    if activo == 1:
                        estado_mouse = "MOUSE ACTIVO"
                        keyAuxInactivo = 0
                        if keyAuxActivo == 0:
                            winapi.keybd_event(0x11, 0, 0, 0)
                            winapi.keybd_event(0x11, 0, wincon.KEYEVENTF_KEYUP, 0)
                            ti.sleep(0.5)
                            winapi.keybd_event(0x11, 0, 0, 0)
                            winapi.keybd_event(0x11, 0, wincon.KEYEVENTF_KEYUP, 0)
                            keyAuxActivo = 1
                    elif activo == 0:
                        estado_mouse = "MOUSE DESACTIVADO"
                        keyAuxActivo = 0
                        if keyAuxInactivo == 0:
                            winapi.keybd_event(0x11, 0, 0, 0)
                            winapi.keybd_event(0x11, 0, wincon.KEYEVENTF_KEYUP, 0)
                            ti.sleep(0.5)
                            winapi.keybd_event(0x11, 0, 0, 0)
                            winapi.keybd_event(0x11, 0, wincon.KEYEVENTF_KEYUP, 0)
                            keyAuxInactivo = 1

                    if reset == 1:
                        key_distancia_ojos = 0
                        primer_loop = 59
                        reset = 0  
                        if llave == 1:
                            relacion_escala_inicial = relación_escala_cm
                    if True:
                        cv2.putText(img_a_procesar, (modo_activo), (20,20), 2, 1, (255,0,0))
                        cv2.putText(img_a_procesar, (estado_mouse), (20,50), 2, 1, color_MAR)
                        cv2.putText(img_a_procesar, (EstadoJoystick), (20,80), 1, 1, color_joy)
                        cv2.putText(img_a_procesar, (EstadoSipPuff), (20,100), 1, 1, color_sip)
                        cv2.putText(img_a_procesar, ("Sensibilidad X webcam  : "+str(param_1_1_x)), (20,140), 1, 1, (0,255,0)) 
                        cv2.putText(img_a_procesar, ("Sensibilidad Y webcam  : "+str(param_1_1_y)), (20,150), 1, 1, (0,255,0)) 
                        cv2.putText(img_a_procesar, ("Sensibilidad X Joystic : "+str(Xjoy.value)), (20,170), 1, 1, (255,0,255)) 
                        cv2.putText(img_a_procesar, ("Sensibilidad Y Joystic : "+str(Yjoy.value)), (20,180), 1, 1, (255,0,255)) 

                    X_MOUSE_RELATIVA_ORIGEN = (x_nariz-x_origen_nariz)
                    Y_MOUSE_RELATIVA_ORIGEN = ((y_nariz-y_origen_nariz))
                 
                    print("Movimiento filtradro")
                    X_FILTRADO = param_1_1_x*X_MOUSE_RELATIVA_ORIGEN*relacion_escala_inicial 
                    Y_FILTRADO = param_1_1_y*Y_MOUSE_RELATIVA_ORIGEN*relacion_escala_inicial 

                    X_FILTRADO = X_FILTRADO+screen_x
                    Y_FILTRADO = Y_FILTRADO+screen_y
                    safe_zoneX = X_FILTRADO-x_ant
                    safe_zoneY = Y_FILTRADO-y_ant
                    x_ant = X_FILTRADO
                    y_ant = Y_FILTRADO

                    if ((abs(safe_zoneX)>4 or abs(safe_zoneY)>3) and activo == 1 and (modo.value == 2 or modo.value == 3)): 
                        if modo.value == 2 and clic_puff_act.value == 1:
                            winapi.SetCursorPos((int(X_FILTRADO),int(Y_FILTRADO))) 

                    tiempo_pasado = ti.time()-periodoIniciar
                    periodoIniciar = ti.time()
                    velX = 0
                except TypeError:
                    pass

                frame = 0
                img_tk = img_a_procesar.copy()
                img_tk = imutils.resize(img_tk, width = 640)   

        if kb.is_pressed("F11") == True and auxLlave == 0:
            llave = (llave+1)%2
            auxLlave = 1            
        elif kb.is_pressed("F11") == False and auxLlave == 1:
            auxLlave = 0   

        if (kb.is_pressed("F9") == True or mover_mouse == 1) and auxActivo == 0:
            activo = (activo+1)%2
            auxActivo = 1
            mover_mouse = 0
        elif kb.is_pressed("F9") == False and auxActivo == 1:
            auxActivo = 0   

        if (kb.is_pressed("F8") == True or reset_mouse == 1) and auxReset == 0:
            reset = (reset+1)%2
            auxReset = 1
            reset_mouse = 0
        elif kb.is_pressed("F8") == False and auxReset == 1:
            auxReset = 0 

        if ((kb.is_pressed("F5") == True and kb.is_pressed("F4") == False) or botonAumentar.value >= 1) and auxParam1_1_x == 0:
            if botonAumentar.value == 2:
                Xjoy.value = (Xjoy.value + 1)%30
            else: 
                param_1_1_x = (param_1_1_x+1)%30
            botonAumentar.value = 0
            auxParam1_1_x = 1
        elif kb.is_pressed("F5") == False and kb.is_pressed("F4") == False and auxParam1_1_x == 1:
            auxParam1_1_x = 0   

        elif ((kb.is_pressed("F4") == True and kb.is_pressed("F5") == False) or botonDisminuir.value >= 1) and auxParam1_1_x == 0:
            if botonDisminuir.value == 2:
                Xjoy.value = (Xjoy.value - 1)%30
            else:
                param_1_1_x = (param_1_1_x-1)%30
            botonDisminuir.value = 0
            auxParam1_1_x = 1
        elif kb.is_pressed("F4") == False and kb.is_pressed("F5") == False and auxParam1_1_x == 1:
            auxParam1_1_x = 0             

        if ((kb.is_pressed("F7") == True and kb.is_pressed("F6") == False) or botonAumentarY.value >= 1) and auxParam1_1_y == 0:
            if botonAumentarY.value == 2:
                Yjoy.value = (Yjoy.value + 1)%30
            else:
                param_1_1_y = (param_1_1_y+1)%30
            botonAumentarY.value = 0
            auxParam1_1_y = 1
        elif kb.is_pressed("F7") == False and kb.is_pressed("F6") == False and auxParam1_1_y == 1:
            auxParam1_1_y = 0   

        elif ((kb.is_pressed("F6") == True and kb.is_pressed("F7") == False) or botonDisminuirY.value >= 1) and auxParam1_1_y == 0:
            if botonDisminuirY.value == 2:
                Yjoy.value = (Yjoy.value - 1)%30
            else:
                param_1_1_y = (param_1_1_y-1)%30
            botonDisminuirY.value = 0
            auxParam1_1_y = 1
        elif kb.is_pressed("F6") == False and kb.is_pressed("F7") == False and auxParam1_1_y == 1:
            auxParam1_1_y = 0

        key = cv2.waitKey(1)
        velX = velX + 1

        root.update_idletasks()
        root.update()

    print("TERMINEEEE")
    cv2.destroyAllWindows()
    cap.release()
    close.value = 1
    enable.value = 0

if __name__ == "__main__":
    enable = Value('i', 1)
    modo = Value('i', 1)
    success = Value('i', 1)
    close = Value('i', 0)
    new_screen_x = Value('i', 0)
    new_screen_y = Value('i', 0)
    reset_modo3 = Value('i', 0)
    clic_modo3 = Value('i', 0)
    clic_puff_act = Value('i', 0)
    botonAumentar = Value('i', 0)
    botonDisminuir = Value('i', 0)
    botonAumentarY = Value('i', 0)
    botonDisminuirY = Value('i', 0)
    estado_joystick = Value('i', 0)
    estado_sip = Value('i', 0)
    Xjoy = Value('i', 0)
    Yjoy = Value('i', 0)

    p = Process(target=main, args=(enable, success, close, modo, new_screen_x, new_screen_y, reset_modo3, clic_modo3, clic_puff_act, botonAumentar, botonDisminuir, botonAumentarY, botonDisminuirY, estado_joystick, estado_sip, Xjoy, Yjoy))
    p.start()
    p.join()