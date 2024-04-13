from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import serial
import time
import threading

app = FastAPI()

# Lista para almacenar los datos del puerto serial
serial_data = []

# Función para inicializar y leer el puerto serial en un hilo separado
def leer_puerto_serial():
    global serial_data
    try:
        serialArduino = serial.Serial("COM5", 9600)
        time.sleep(1)
        while True:
            cad = serialArduino.readline().decode('ascii').strip()  # Eliminar \r\n
            serial_data.append(cad)
    except serial.SerialException as e:
        serial_data.append("Error en el puerto serial: " + str(e))
    except Exception as e:
        serial_data.append("Se produjo un error: " + str(e))
    finally:
        serialArduino.close()

# Iniciar la lectura del puerto serial en un hilo separado
thread = threading.Thread(target=leer_puerto_serial)
thread.start()

# Configuración de CORS
origins = [
    "http://localhost",
    "http://localhost:3000",  # Agrega aquí la URL de tu aplicación React Native
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

# Ruta para obtener los datos del puerto serial
@app.get("/datos_serial")
async def datos_serial():
    global serial_data
    return {"datos": serial_data}

# Ruta raíz para servir el archivo index.html
@app.get("/")
async def root():
    return FileResponse("index.html")

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)