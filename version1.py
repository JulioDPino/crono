import time
import RPi.GPIO as GPIO
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics

# Configuración del sensor de ultrasonido
GPIO.setmode(GPIO.BCM)
TRIG = 23  # Asegúrate de conectar el TRIG al pin GPIO 23
ECHO = 24  # Asegúrate de conectar el ECHO al pin GPIO 24
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

# Configuración de la matriz LED
options = RGBMatrixOptions()
options.rows = 64
options.cols = 64
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = 'regular'  # Cambiar según configuración
matrix = RGBMatrix(options=options)

# Función para mostrar el tiempo en el panel LED
def mostrar_tiempo(tiempo, matrix):
    canvas = matrix.CreateFrameCanvas()
    font = graphics.Font()
    font.LoadFont("/home/pi/rpi-rgb-led-matrix/fonts/9x15B.bdf")
    textColor = graphics.Color(255, 255, 255)  # Color blanco
    tiempo_str = f"{tiempo}s"
    graphics.DrawText(canvas, font, 22, 32, textColor, tiempo_str)
    matrix.SwapOnVSync(canvas)

# Función para medir la distancia
def medir_distancia():
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)
    inicio = time.time()
    while GPIO.input(ECHO) == 0:
        inicio = time.time()
    while GPIO.input(ECHO) == 1:
        final = time.time()
    duracion = final - inicio
    distancia = (duracion * 34300) / 2
    return distancia

try:
    print("Esperando a que el sensor se estabilice")
    GPIO.output(TRIG, False)
    time.sleep(2)  # Permitir que el sensor se estabilice

    detectado = False
    start_time = None
    while True:
        distancia = medir_distancia()
        print(f"Distancia medida: {distancia} cm")

        if distancia < 40 and not detectado:
            print("Objeto detectado a menos de 40 cm")
            start_time = time.time() if not start_time else start_time
            detectado = True
        elif distancia >= 40 and detectado:
            detectado = False
            print("No hay objeto dentro del rango")

        if start_time:
            elapsed_time = int(time.time() - start_time)
            mostrar_tiempo(elapsed_time, matrix)

        time.sleep(1)

finally:
    GPIO.cleanup()
    print("Limpieza de GPIO y salida del programa")
