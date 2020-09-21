#######################################################################
##                            LIBRERIAS                              ##
#######################################################################

from socket import *
from _thread import *
import time
import sys
from blackJack import Jugador, Mazo

#######################################################################
##                            FUNCIONES                              ##
#######################################################################

#ini() -- Pide al usuario el host y puerto.
def ini():
    #host = input("Host: ")
    #port = int(input("Port: "))
    host = "192.168.1.56"
    port = 55
    return host, port

#crearSocket() -- Retorna un nuevo socket siguiendo el esquema del protocolo TCP
def crearSocket():
    s = socket(AF_INET, SOCK_STREAM)
    return s

#ligarSocket(s, host, port) -- Intenta ligar un socket a los parametros host y port
def ligarSocket(s, host, port):
    while True:
        try:
            s.bind((host, port))
            break

        except error as e:
            print("ERROR:", e)


#conexiones(s) -- Espera por la conexion de clientes externos. Retorna la direccion del cliente en una tupla
def conexiones(s):

    conn, addr = s.accept()
    print("\nEstablished Connection.\nThe client is:", addr[0] + ":" + str(addr[1])+"\n")
    return conn, addr


#enviar(conn) -- Envia un mensaje codificado a la direccion del cliente 1
def enviar(conn):

    global indexReg
    global terminarJ
    global repetirJuego

    print("TERMINA ES ")
    print(terminarJ)

    #msg = input("")
    if indexReg == 1 :
        msg = "Ingrese la cedula: "
        
    elif indexReg == 2 : 
        msg = "Nombre Usuario: "

    elif indexReg == 3 :

        if jugador.contar_mano() <= 21 and not terminarJ:
            msg = "Mano Jugador   " + jugador.mostrar_mano_string()
            msg = msg + "\nMano Maquina   " + maquina.mostrar_mano_string()
            msg = msg + "\n¿Qué desea hacer?\n"
            msg = msg + "1. Pedir carta\n"
            msg = msg + "2. Plantarse"
                    
        elif jugador.contar_mano() > 21:
            msg = "Perdio, la suma de las cartas es mayor a 21\n"
            msg = msg + jugador.mostrar_mano_string()

        elif terminarJ :
            indexReg = 4
            print("FIN AHORA MAQUINA JUEGA :)")
            m.dar_una_carta(maquina)
            msg = "\nMano Maquina  " + maquina.mostrar_mano_string()
                        
            if jugador.contar_mano() <= 21 :
                while (maquina.contar_mano() < jugador.contar_mano() and maquina.contar_mano() < 21 ):
                    m.dar_una_carta(maquina)
                    print(maquina.mostrar_mano_string())
                    msg = msg + "\nMano Maquina  " + maquina.mostrar_mano_string()

                if maquina.contar_mano() > 21 :
                    msg = msg + "\n\nMano Maquina  " + maquina.mostrar_mano_string()
                    msg = msg + "\nPerdio la maquina"

                elif maquina.contar_mano() == jugador.contar_mano() :
                    msg = msg + "\n\nMano Maquina  " + maquina.mostrar_mano_string()
                    msg = msg + "\nMano Jugador  " + jugador.mostrar_mano_string()
                    msg = msg + "\nEMPATE"

                else :
                    msg = msg + "\n\nMano Maquina  " + maquina.mostrar_mano_string()
                    msg = msg + "\nGano La Maquina"
            
            else :
                msg = msg + "\n\nMano Maquina  " + maquina.mostrar_mano_string()
                msg = msg + "\nGano la Maquina"

    elif indexReg == 4 :
        msg = "\nJugar de nuevo: "
        msg = msg + "\n<1.> Si "
        msg = msg + "\n<2.> Salir "

    try:

        conn.send(msg.encode("UTF-8"))

    except:
        print("\nSomething happend")
        print("Try in 5 seg\n")
        time.sleep(5)


#enviar2(conn) -- Envia un mensaje codificado a la direccion del cliente 2
def enviar2(conn):

        msg = input("")
        msg = "Servidor: " + msg
        try:

            conn.send(msg.encode("UTF-8"))

        except:
            print("\nSomething happend")
            print("Try in 5 seg\n")
            time.sleep(5)


#recibir(conn) -- Gestiona los mensajes recibidos de los distintos clientes. 
#Llama a la funcion enviar una vez que recibe mensajes
def recibir(conn):
    while True:

#Variables Globales
        global bandera
        global indexReg
        global m
        global terminarJ
        global repetirJuego

        try:
            reply = conn.recv(2048)
            reply = reply.decode("UTF-8")
            print("EL DE REPLY")
            print(reply)

            if reply[0] == "1":
                print("Cliente", reply)

                if indexReg == 1 :
                    jugador.cedula = reply[3:]
                    indexReg = 2
        
                elif indexReg == 2 : 
                    jugador.nombre = reply[3:]
                    m.dar_una_carta(maquina)
                    m.dar_una_carta(jugador)
                    m.dar_una_carta(jugador)
                    jugadores.append(jugador)
                    print("jug")
                    print("nam" + jugador.nombre)
                    print("celd" + jugador.cedula)
                    jugador.mostrar_mano()
                    indexReg = 3

                elif indexReg == 3 :
                    print("CASO 3 DE INGRESO")
                    r = int(reply[3])
                    if(r == 1):
                        m.dar_una_carta(jugador)
                    if(r == 2):
                        terminarJ = True
                        
                elif indexReg == 4 :
                    
                    r = int(reply[3])

                    if(r == 1):
                        repetirJuego = True
                        
                    if repetirJuego :
                        m.dar_una_carta(maquina)
                        m.dar_una_carta(jugador)
                        m.dar_una_carta(jugador)
                        jugador.mostrar_mano()
                        indexReg = 3
                    
                    else :
                        break
             
                start_new_thread(enviar, (conn,))

            elif reply[0] == "2":
                print("Cliente", reply)
                start_new_thread(enviar2, (conn,))

            else:
                lista_de_clientes.append(reply[4])
                print("\nThe client "+reply[4]+" is gone")
                bandera = True
                break



        except:
            print("\nCant recieve response")
            print("Trying in 5 seg\n")
            time.sleep(5)


#enviarEspecial(conn) -- El servidor asigna un numero y lo envia al cliente respectivo

def enviarEspecial(conn):
    global lista_de_clientes,client
    client = lista_de_clientes.pop()
    conn.send(client.encode("UTF-8"))

def iniciarJuego1():
    global terminarJ
    global jugador
    global maquina
    global m
    global indexReg

    terminarJ = False
    jugador.mano = []
    maquina.mano = []
    m = Mazo()
    indexReg = 2

#######################################################################
##                          VARIABLES GLOBALES                       ##
#######################################################################

bandera = False      # Utilizada en la desconexion/conexion de clientes

lista_de_clientes = ["2","1"]   # El servidor le asigna un numero a los
                                # clientes segun esta lista

client = ""     # Numero del cliente

indexReg = 1

jugadores = []

jugador = Jugador()

maquina = Jugador()
maquina.nombre = "Crupier"
maquina.cedula = "2015"

m = Mazo()

terminarJ = False
repetirJuego = False

#######################################################################
##                                MAIN                               ##
#######################################################################

def main():

    global bandera
    host,port = ini()
    s = crearSocket()
    ligarSocket(s, host,port)
    s.listen(2)     # Espero 2 clientes

    print("\nW A R N I N G : THE SERVER IS A SLAVE. DON'T "
          "WRITE IF THE SERVER DOESN'T HAVE ANY MESSAGE TO RESPONSE")
    print("\nWaiting for clients")

    conn,addr = conexiones(s)
    enviarEspecial(conn)               # Espero conexion del 1 cliente
    start_new_thread(enviar,(conn,))
    time.sleep(2)
    start_new_thread(recibir,(conn,))


    conn2,addr2 = conexiones(s)
    enviarEspecial(conn2)              # Espero conexion del 2 cliente
    start_new_thread(recibir,(conn2,))

    while True: # Necesario para que los hilos no mueran

        if bandera != True:     # En caso de desconectarse un cliente,
                                # esperara a que otro vuelve a conectarse
            conn3,addr3 = conexiones(s)
            enviarEspecial(conn3)
            start_new_thread(recibir,(conn3,))
            bandera = False


main()
