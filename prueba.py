import time
import serial

# If you have a file named serial.py in your directory, rename or remove it to avoid conflicts.

# Configura el puerto y la velocidad (ajusta según tu Arduino)
arduino = serial.Serial('COM3', 9600, timeout=1)
time.sleep(2)  # Espera a que Arduino reinicie


# Cierra la conexión
while True:
    # Solicita al usuario los grados a mover el servo
    grados = input("¿Cuántos grados quieres mover el servo? (o escribe 'salir' para terminar) ")
    if grados.lower() == 'salir':
        break
    # Envía el valor ingresado al Arduino
    arduino.write(grados.encode())

# Cierra la conexión
arduino.close()