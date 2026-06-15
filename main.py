"""
Este proyecto tiene la razon de ser gracias al escaneo de redes y poder tener una conciencia
mejor sobre lo vulnerables que son nuestras redes
"""

import sys
import socket
import os

# Lista donde se almacenarán los dispositivos encontrados
dispositivos = []


def obtener_ip_local():

    nombre_host = socket.gethostname()
    direcciones = socket.gethostbyname_ex(nombre_host)

    for ip in direcciones[2]:
        if not ip.startswith("127."):
            return ip

    return direcciones[2][0]


def main():

    print(r"""


  _________                        __   _________
 /   _____/           ____   _____/  |_/   _____/ ____ _____    ____
 \_____  \   ______  /    \_/ __ \   __\_____  \_/ ___|\__  \  /    \
 /        \ /_____/ |   |  \  ___/|  | /        \  \___ / __ \|   |  \
/_______  /         |___|  /\___  >__|/_______  /\___  >____  /___|  /
        \/               \/     \/            \/     \/     \/     \/

""")

    while True:

        print("\n===== MENU =====")
        print("1. Escanear red")
        print("2. Dispositivos encontrados")
        print("3. Informacion del host")
        print("4. Guardar reporte")
        print("5. Salir")

        opcion = input("Presiona el numero que deseas: ")

        if opcion == "1":
            escanear_red()

        elif opcion == "2":
            dispositivos_enc()

        elif opcion == "3":
            informacion_host()

        elif opcion == "4":
            guardar_reporte()

        elif opcion == "5":
            print("bye bye :3")
            sys.exit()

        else:
            print("Caracter no valido")


def informacion_host():

    hostname = socket.gethostname()
    direccion_ip = obtener_ip_local()

    print("\n===== INFORMACION DEL HOST =====")
    print("Nombre del host:", hostname)
    print("Direccion IP:", direccion_ip)


def escanear_red():

    global dispositivos

    dispositivos = []

    direccion_ip = obtener_ip_local()

    print("\nEscaneando red...")
    print("IP local:", direccion_ip)

    partes = direccion_ip.split(".")

    red = partes[0] + "." + partes[1] + "." + partes[2]

    print("Red detectada:", red + ".0/24")
    print("Buscando dispositivos...\n")

    encontrados = 0

    # Detectar sistema operativo para usar el ping correcto
    if os.name == "nt":
        comando_ping = "ping -n 1 "
        salida = " > nul 2>&1"
    else:
        comando_ping = "ping -c 1 "
        salida = " > /dev/null 2>&1"

    for numero in range(1, 255):

        ip = red + "." + str(numero)

        print("Probando:", ip)

        respuesta = os.system(comando_ping + ip + salida)

        if respuesta == 0:

            print("✓ Dispositivo encontrado:", ip)

            dispositivos.append(ip)

            encontrados += 1

    print("\n===== ESCANEO FINALIZADO =====")
    print("Total encontrados:", encontrados)


def dispositivos_enc():

    print("\n===== DISPOSITIVOS ENCONTRADOS =====")

    if len(dispositivos) == 0:

        print("No hay dispositivos almacenados.")
        print("Realiza un escaneo primero.")

        return

    contador = 1

    for dispositivo in dispositivos:

        print(str(contador) + ". " + dispositivo)

        contador += 1


def guardar_reporte():

    archivo = open("reporte.txt", "w")

    archivo.write("===== S-netScan =====\n\n")

    archivo.write("Dispositivos encontrados:\n\n")

    if len(dispositivos) == 0:

        archivo.write("No se encontraron dispositivos.\n")

    else:

        contador = 1

        for dispositivo in dispositivos:

            archivo.write(str(contador) + ". " + dispositivo + "\n")

            contador += 1

    archivo.close()

    print("\nReporte guardado correctamente.")
    print("Archivo: reporte.txt")


main()