import cv2
from matplotlib.pyplot import pink
import mediapipe as mp
from Funciones.condicionales import condicionalesLetras
from Funciones.normalizacionCords import obtenerAngulos

lectura_actual = 0

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
mp_drawing_styles = mp.solutions.drawing_styles

#cap = cv2.VideoCapture("Letras/Letra_o.mp4")
cap = cv2.VideoCapture(0)

wCam, hCam = 1280, 720
cap.set(3, wCam)
cap.set(4, hCam)

with mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=2,
        min_detection_confidence=0.75) as hands:

    while True:
        ret, frame = cap.read()
        if ret == False:
            break
        height, width, _ = frame.shape
        frame = cv2.flip(frame, 1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)
        if results.multi_hand_landmarks is not None:
            # Accediendo a los puntos de referencia, de acuerdo a su nombre
                
                angulosid = obtenerAngulos(results, width, height)[0]
                pinky = obtenerAngulos(results, width, height)[1]

                dedos = []
                # pulgar externo angle
                if angulosid[5] > 125:
                    dedos.append(1)
                else:
                    dedos.append(0)

                # pulgar interno
                if angulosid[4] > 150:
                    dedos.append(1)
                else:
                    dedos.append(0)

                # 4 dedos
                for id in range(0, 4):
                    if angulosid[id] > 90:
                        dedos.append(1)
                    else:
                        dedos.append(0)

                
                TotalDedos = dedos.count(1)

                # guardar lectura anterior y comparar con lectura acutal de pinky
                
                pinkY=pinky[1] + pinky[0]   
                resta = pinkY - lectura_actual
                lectura_actual = pinkY
                
                print(abs(resta), pinkY, lectura_actual)

                if abs(resta) > 30:
                    print("jota en movimento")
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    cv2.rectangle(frame, (0, 0), (100, 100), (255, 255, 255), -1)
                    cv2.putText(frame, 'J', (20, 80), font, 3, (0, 0, 0), 2, cv2.LINE_AA)
                    print("J")

                if dedos == [0, 0, 1, 0, 0, 0]:
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    cv2.rectangle(frame, (0, 0), (100, 100), (255, 255, 255), -1)
                    cv2.putText(frame, 'I', (20, 80), font, 3, (0, 0, 0), 2, cv2.LINE_AA)
                    print("I")
                # # condicionalesLetras(dedos, frame)
                
            
                #testing--------------------------------------
                # print(dedos)
                # print("meñique:", angle1, "anular:", angle2, "medio:", angle3,
                #       "indice:", angle4, "pulgar 1:", angle5, "pulgar 2:", angle6)
                # print (angle1, angle2, angle3, angle4, angle5, angle6)

                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        mp_drawing.draw_landmarks(
                            frame,
                            hand_landmarks,
                            mp_hands.HAND_CONNECTIONS,
                            mp_drawing_styles.get_default_hand_landmarks_style(),
                            mp_drawing_styles.get_default_hand_connections_style())
        cv2.imshow('Frame', frame)
        #mostra fotogramas por segundos
        
        if cv2.waitKey(1) & 0xFF == 27:
            break

cap.release()
cv2.destroyAllWindows()