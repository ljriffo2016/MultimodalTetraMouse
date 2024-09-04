import cv2
import numpy as np


def inicializar_camara(fuente):
    cap = cv2.VideoCapture(fuente)
    return cap


def img_webcam (cap):
    timer = cv2.getTickCount()
    success, img = cap.read()
    img = cv2.flip(img, 1)
    rgb_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    fps = cv2.getTickFrequency()/(cv2.getTickCount()-timer)
    cv2.putText(img,str(int(fps)), (75,50),cv2.FONT_HERSHEY_SIMPLEX, 0.7 , (0,0,255),2)
    return img, rgb_image

def redimensionar(img, largo, alto, y1_ref = 0, y2_ref = 480, x1_ref = 0, x2_ref = 640):
    imgCrop = img[y1_ref:y2_ref, x1_ref:x2_ref]
    largoVentanita = (x2_ref-x1_ref)
    altoVentanita = (y2_ref-y1_ref)
    propLargo = int(largo/largoVentanita)
    propAmcho = int(alto/altoVentanita)
    imgCrop_rezise = cv2.resize(imgCrop,(largo,alto))
    return imgCrop_rezise

def umbraliza(img): #util para umbralizar y rellenar huecos mas complejos
    im_in = img
    im_in = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    th, im_th = cv2.threshold(im_in, 0, 255, cv2.THRESH_BINARY_INV)
    im_floodfill = im_th.copy()

    h, w = im_th.shape[:2]
    mask = np.zeros((h+2, w+2), np.uint8)
    cv2.floodFill(im_floodfill, mask, (0,0), 255)
    im_floodfill_inv = cv2.bitwise_not(im_floodfill)
    im_out = im_th | im_floodfill_inv

    #final_img = img_gray*im_out
    #final_img = cv2.bitwise_or(img_clean, img_clean, mask=im_out)
    return im_out

def umbralizaAlternativo(img): #solo necesito un punto , puede rellenar figuras simples
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_range = np.array([00,255,100])
    upper_range = np.array([100,255,100])
    mask = cv2.inRange(hsv, lower_range, upper_range)
    return mask

def dibujar_rectangulo(img, x1_ref, y1_ref,x2_ref , y2_ref, color, filt = False):
    # if x1_ref<0:
    #     x1_ref = 0
    # if y1_ref<0:
    #     y1_ref = 0
    # if x2_ref<0:
    #     x2_ref = 0
    # if y1_ref<0:
    #     y2_ref = 0 

    pto_medio_X_box= pto_medio(x1_ref,x2_ref)
    pto_medio_Y_box = pto_medio(y1_ref,y2_ref)

    #sin filtar
    cv2.rectangle(img,(x1_ref,y1_ref),(x2_ref,y2_ref),color,3)
    cv2.circle(img, (pto_medio_X_box,pto_medio_Y_box), 4, color, 1)
    return pto_medio_X_box, pto_medio_Y_box

def pto_medio(a,b):
    medio = round(a+(b-a)*0.5)
    return medio


def deteccionCara(results,image,width,height):
    if results.detections is not None:
        for detection in results.detections:
            # Bounding Box
            xmin = int(detection.location_data.relative_bounding_box.xmin * width)
            ymin = int(detection.location_data.relative_bounding_box.ymin * height)
            w = int(detection.location_data.relative_bounding_box.width * width)
            h = int(detection.location_data.relative_bounding_box.height * height)

            #cv2.rectangle(image, (xmin, ymin), (xmin + w, ymin + h), (0, 255, 0), 4)

            return xmin, ymin, xmin + w , ymin + h

            # # Centro de la boca
            # x_MC = int(mp_face_detection.get_key_point(detection, mp_face_detection.FaceKeyPoint.MOUTH_CENTER).x * width)
            # y_MC = int(mp_face_detection.get_key_point(detection, mp_face_detection.FaceKeyPoint.MOUTH_CENTER).y * height)
            # cv2.circle(image, (x_MC, y_MC), 3, (0, 255, 0), 25)

            # # Trago de la oreja derecha
            # x_RET = int(mp_face_detection.get_key_point(detection, mp_face_detection.FaceKeyPoint.RIGHT_EAR_TRAGION).x * width)
            # y_RET = int(mp_face_detection.get_key_point(detection, mp_face_detection.FaceKeyPoint.RIGHT_EAR_TRAGION).y * height)
            # cv2.circle(image, (x_RET, y_RET), 3, (0, 255, 255), 25)

            # # Trago de la oreja izquierda
            # x_LET = int(mp_face_detection.get_key_point(detection, mp_face_detection.FaceKeyPoint.LEFT_EAR_TRAGION).x * width)
            # y_LET = int(mp_face_detection.get_key_point(detection, mp_face_detection.FaceKeyPoint.LEFT_EAR_TRAGION).y * height)
            # cv2.circle(image, (x_LET, y_LET), 3, (255, 255, 0), 25)

def distanciaEntrePuntos(x1_ref, y1_ref, x2_ref, y2_ref):
    distancia = int(np.hypot((x2_ref-x1_ref),(y2_ref-y1_ref)))
    return distancia