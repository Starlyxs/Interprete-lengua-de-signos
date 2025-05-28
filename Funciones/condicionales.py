import cv2
import time

letra = ""


def condicionalesLetras(dedos, frame, mano_lado=None):
# Diccionario de letras fuera de la función para evitar recrearlo cada llamada
        if not hasattr(condicionalesLetras, "letras_dict"):
                condicionalesLetras.letras_dict = {
                (1, 1, 0, 0, 0, 0): 'A',
                (0, 0, 0, 0, 0, 0): 'E',
                (0, 0, 1, 0, 0, 0): 'I',
                (1, 0, 1, 0, 0, 0): 'O',
                (0, 0, 1, 0, 0, 1): 'U',
                (0, 0, 1, 1, 1, 1): 'B',
                (1, 0, 1, 0, 0, 0): 'C',
                (0, 0, 0, 0, 0, 1): 'D',
                (1, 1, 0, 0, 1, 1): 'K',
                (1, 1, 0, 0, 0, 1): 'L',
                (0, 1, 0, 1, 1, 1): 'W',
                (0, 1, 0, 0, 1, 1): 'N',
                (1, 1, 1, 0, 0, 0): 'Y',
                (1, 1, 1, 1, 1, 0): 'F',
                (0, 1, 1, 1, 1, 1): 'P',
                (0, 1, 0, 0, 1, 1): 'V'
                }

        font = cv2.FONT_HERSHEY_SIMPLEX
        dedos_tuple = tuple(dedos)
        letra_actual = condicionalesLetras.letras_dict.get(dedos_tuple)

        if mano_lado is None:
            mano = "Izquierda"  # Valor por defecto si no se pasa nada
            is_mano_derecha = False
        else:
            mano = mano_lado
            is_mano_derecha = mano_lado == "Derecha"

        if letra_actual:
            _dibujar_letra(frame, letra_actual, font)

        _inicializar_atributos(condicionalesLetras)

        is_mano_cerrada = all(d == 0 for d in dedos)
        if is_mano_cerrada:
            condicionalesLetras.prev_letra = None
            condicionalesLetras.prev_mano = None
        else:
            tiempo_signo = 1 if is_mano_derecha else -1  # Ahora derecha es negativo
            tolerancia = 0.2  # 0.2 segundos de tolerancia

            _gestionar_tiempo_letra(condicionalesLetras, letra_actual, mano, tiempo_signo, tolerancia)

        if not hasattr(condicionalesLetras, "last_time"):
            condicionalesLetras.last_time = time.time()
            condicionalesLetras.last_letra = None

        if letra_actual != condicionalesLetras.last_letra:
            condicionalesLetras.last_time = time.time()
            condicionalesLetras.last_letra = letra_actual

        if letra_actual:
                tiempo = time.time() - condicionalesLetras.last_time
                grados = int(tiempo * 19)
                grados = min(grados, 180)
                cv2.putText(frame, f"{letra_actual} ({mano}): {grados} deg", (10, 150), font, 1, (0, 255, 0), 2, cv2.LINE_AA)

        return dedos

def _dibujar_letra(frame, letra, font):
        cv2.rectangle(frame, (0, 0), (100, 100), (255, 255, 255), -1)
        cv2.putText(frame, letra, (20, 80), font, 3, (0, 0, 0), 2, cv2.LINE_AA)

def _inicializar_atributos(func):
        if not hasattr(func, "prev_letra"):
                func.prev_letra = None
        if not hasattr(func, "prev_mano"):
                func.prev_mano = None

def _gestionar_tiempo_letra(func, letra_actual, mano, tiempo_signo, tolerancia):
        if hasattr(func, "last_letra") and hasattr(func, "last_time"):
                letra_cambio = letra_actual != func.prev_letra
                mano_cambio = mano != func.prev_mano
                if func.prev_letra and (letra_cambio or mano_cambio):
                        tiempo = time.time() - func.last_time
                        if tiempo > tolerancia:
                                tiempo *= tiempo_signo
                                print(f"Letra '{func.prev_letra}' mostrada por {tiempo:.2f} segundos ({func.prev_mano})")
                                LETRAS_MOTORES = {"P", "W", "V", "Y", "A", "L"}
                                if func.prev_letra in LETRAS_MOTORES:
                                        enviar_a_arduino_letra_tiempo(func.prev_letra, tiempo)
                        func.last_time = time.time()
                func.prev_letra = letra_actual
                func.prev_mano = mano

import serial

arduino = None

def enviar_a_arduino_letra_tiempo(letra, tiempo, puerto='COM6', baudrate=9600):
    """
    Envía la letra y el tiempo al Arduino en el formato LetraGrados (ejemplo: P19).
    El tiempo se interpreta como grados (1 segundo = 19 grados).
    """
    global arduino
    try:
        if arduino is None or not arduino.is_open:
            arduino = serial.Serial(puerto, baudrate, timeout=1)
            time.sleep(2)  # Espera a que Arduino reinicie si es necesario

        grados = int(tiempo * 19)  # 1 segundo = 19 grados
        grados = min(grados, 180)
        mensaje = f"{letra}{grados}\n"
        arduino.write(mensaje.encode())
        print(f"Enviado a Arduino: {mensaje.strip()}")
    except Exception as e:
        print(f"Error enviando a Arduino: {e}")