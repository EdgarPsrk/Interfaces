import serial
import time

# Establece el puerto serie
ser = serial.Serial('/dev/ttyACM0', 9600)  # Ajusta el nombre del puerto según tu sistema

try:
    while True:
        # Lee el valor del potenciómetro desde Arduino
        data = ser.readline().decode('utf-8').strip()

        # Verifica si la cadena no está vacía antes de intentar convertirla
        if data:
            valor_pot = int(data)
            # Visualiza el valor del potenciómetro
            print(f"Valor del potenciómetro: {valor_pot}")

        # Puedes agregar aquí la lógica para controlar otras cosas en tu programa

except KeyboardInterrupt:
    print("Programa detenido por el usuario.")

finally:
    ser.close()

