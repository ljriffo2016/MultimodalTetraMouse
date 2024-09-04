
import time as t
import serial
import win32api as winapi
import win32con as wincon
import win32com.client as winclient

"""
Esta funcion asigna los click al sip and puff 

"""
def iniciarComSerial(estado_sip):
    try:
        serialArduino = serial.Serial("COM5",115200)
        estado_sip.value = 2
        t.sleep(3)
        conectado = 1
        return serialArduino, conectado
    except (serial.serialutil.SerialException, AttributeError):
        conectado = 0
        serialArduino = 0
        return serialArduino, conectado



def clickFunc(enable,success,close,modo,clic_puff_act,estado_sip):       #(modo,enable):

    key = 0
    sostenido = 0
    tiempo_sostenido=0
    while enable.value == 1:
        serialArduino, conectado = iniciarComSerial(estado_sip)
        #print("conectando SIP")
        if conectado == 1:
            print("SIP CONECTADO!")
            estado_sip.value = 0
            break
        else:
            estado_sip.value = 1
            #print("conectando SIP")

    contador = 0
    t_inicial_c_iz = t.time()
    t_inicial_c_der = t_inicial_c_iz
    tiempo = 1
    tiempo_clk_der = 0.7
    while close.value == 0:   
        try:   
            data = serialArduino.readline().decode().rstrip()  
            if modo.value == 2 or modo.value  == 3:
                
                
                #print(type(data))
                if data == '':
                    cad = 0
                else:
                    cad = int(data)  
        #______________________________click izquierdo_______________________________________________
                if cad == 1 and key == 0:
                    
                    print("clic izquierdo")                
                    winapi.mouse_event(wincon.MOUSEEVENTF_LEFTDOWN,0,0)
                    
                    
                    key=1
                    # tiempo_sostenido = tiempo_sostenido+1
                elif cad == 1 and key == 1:
                    # tiempo_sostenido = tiempo_sostenido+1
                    # print(tiempo_sostenido)
                    if t.time()-t_inicial_c_iz>=tiempo: #tiempo_sostenido>=tiempo:
                        print("sosteniendo click...") 
                        tiempo_sostenido = 0
                        t_inicial_c_iz = t.time()
                        key = 2
                        winapi.keybd_event(0x11, 0, 0, 0)
                        winapi.keybd_event(0x11, 0, wincon.KEYEVENTF_KEYUP, 0)
                

                        
                elif (cad == 1) and key == 3:
                    print("se liberó el click...")
                    # clic_puff_act.value = 1  
                    winapi.mouse_event(wincon.MOUSEEVENTF_LEFTUP,0,0)
                    key = 4
                else:
                    tiempo_sostenido = 0
                    t_inicial_c_iz = t.time()


                if cad == 0 and key == 1:
                    print("soltó click izquierdo")
                    winapi.mouse_event(wincon.MOUSEEVENTF_LEFTUP,0,0)
                    
                    
                    key = 0
                elif cad == 0 and key == 2:
                    # clic_puff_act.value = 1 
                    print("se soltó el click sostenido, pero se mantiene la funcion")
                    print("presione click izquierdo nuevamente para dejar de sostener...") 
                    key = 3
                elif cad == 0 and key == 4:
                    key = 0

                

        #______________________________click derecho_______________________________________________

                if cad == -1 and key == 0:
                    print("click derecho")
                    
                    key = 5
                elif cad == -1 and key == 5:
                    clic_puff_act.value = 0
                    print(tiempo_sostenido)
                    if t.time()-t_inicial_c_der>=tiempo_clk_der: #tiempo_sostenido>=tiempo:                        
                        print("doble click...") 
                        tiempo_sostenido = 0
                        t_inicial_c_der = t.time()
                        key = 6
                        winapi.mouse_event(wincon.MOUSEEVENTF_LEFTDOWN,0,0)
                        winapi.mouse_event(wincon.MOUSEEVENTF_LEFTUP,0,0)
                        t.sleep(0.5)
                        winapi.mouse_event(wincon.MOUSEEVENTF_LEFTDOWN,0,0)
                        winapi.mouse_event(wincon.MOUSEEVENTF_LEFTUP,0,0)
                
                elif cad == 0 and key == 6:
                    clic_puff_act.value = 1
                    t_inicial_c_der = t.time()   
                    key=0       
                elif cad == 0 and key == 5:
                    print("soltó click derecho")
                    clic_puff_act.value = 1
                    t_inicial_c_der = t.time()
                    winapi.mouse_event(wincon.MOUSEEVENTF_RIGHTDOWN,0,0) 
                    winapi.mouse_event(wincon.MOUSEEVENTF_RIGHTUP,0,0)
                    key=0
                else:
                    t_inicial_c_der = t.time() 

                # if t.time()-t_inicial>=1:
                #     print("loops por segundo: ", contador)
                    
                #     t_inicial = t.time()
                #     contador = 0
                # contador = (contador + 1)    
        except (serial.serialutil.SerialException, AttributeError):
            serialArduino, conectado = iniciarComSerial(estado_sip)
            if conectado == 1:
                print("SIP CONECTADO!")
                estado_sip.value = 0
            
            else:
                estado_sip.value = 1
                print("conectando SIP")     

                

if __name__ == '__main__':
    clickFunc()


















    # key = 0
    # sostenido = 0
    # tiempo_sostenido=0
    # serialArduino = serial.Serial("COM3",115200)
    # t.sleep(3)
    

    # while enable.value:

    #     if modo.value == 0 or modo.value == 1:

    #         tiempo = 10
    #         data = serialArduino.readline().decode().rstrip()
    #         #print(type(data))
    #         if data == '':
    #             cad = 0
    #         else:
    #             cad = int(data)  
    # #______________________________click izquierdo_______________________________________________
    #         if cad == 1 and key == 0:
    #             print("clic izquierdo")
    #             winapi.mouse_event(wincon.MOUSEEVENTF_LEFTDOWN,0,0) 
    #             key=1
    #             tiempo_sostenido = tiempo_sostenido+1
    #         elif cad == 1 and key == 1:
    #             tiempo_sostenido = tiempo_sostenido+1
    #             print(tiempo_sostenido)
    #             if tiempo_sostenido>=tiempo:
    #                 print("sosteniendo click...") 
    #                 tiempo_sostenido = 0
    #                 key = 2
    #                 winapi.keybd_event(0x11, 0, 0, 0)
    #                 winapi.keybd_event(0x11, 0, wincon.KEYEVENTF_KEYUP, 0)
                    
    #         elif (cad == 1) and key == 3:
    #             print("se liberó el click...") 
    #             winapi.mouse_event(wincon.MOUSEEVENTF_LEFTUP,0,0)
    #             key = 4
    #         else:
    #             tiempo_sostenido = 0


    #         if cad == 0 and key == 1:
    #             print("soltó click izquierdo")
    #             winapi.mouse_event(wincon.MOUSEEVENTF_LEFTUP,0,0) 
    #             key = 0
    #         elif cad == 0 and key == 2:
    #             print("se soltó el click sostenido, pero se mantiene la funcion")
    #             print("presione click izquierdo nuevamente para dejar de sostener...") 
    #             key = 3
    #         elif cad == 0 and key == 4:
    #             key = 0

            

    # #______________________________click derecho_______________________________________________

    #         if cad == -1 and key == 0:
    #             print("click derecho")
    #             winapi.mouse_event(wincon.MOUSEEVENTF_RIGHTDOWN,0,0)
    #             key = 5
    #         if cad == 0 and key == 5:
    #             print("soltó click derecho")
    #             winapi.mouse_event(wincon.MOUSEEVENTF_RIGHTUP,0,0)
    #             key=0
    #     else: 
    #         pass
                      