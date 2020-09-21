#######################################################################
##                            LIBRERIAS                              ##
#######################################################################

from socket import *
import time
from _thread import *

#######################################################################
##                            FUNCIONES                              ##
#######################################################################

#ini() -- Pide al usuario el host y puerto.
def ini():
    #host = input("Server Address: ")
    #port = int(input("Port: "))
    host = "192.168.1.56"
    port = 55
    return host, port

#crearSocket() -- Retorna un nuevo socket siguiendo el esquema del protocolo TCP
def crearSocket():
    s = socket(AF_INET, SOCK_STREAM)
    return s

#conectarse (host, port, s) -- Su nombre lo dice todo
def conectarse (host, port, s):
    s.connect((host, port))


#intentoConexion(host, port, s) -- Si el puerto no esta tomado y la direccion sumistrada es correcta
#se conectara al servidor
def intentoConexion(host, port, s):

        while True:
            print("\nTrying to connect to:", host + ":" + str(port))
            try:
                conectarse(host, port, s)
                break
            except:
                print("There is no Server at:", host + ":" + str(port))
                print("Trying again in 5 Seconds\n")
                time.sleep(5)

#recibir(s) -- Hilo que se ejecuta una vez y muere. Recibe los mensajes del servidor
def recibir(s):
    while True:

        global comenzarJ
        global exit



        try:
            reply = s.recv(2048)
            print("salida def0")
            print(reply.decode("UTF-8")[1:4])
            if reply.decode("UTF-8") == "Nombre Usuario: ":
                comenzarJ = True
            
            if reply.decode("UTF-8")[0:5] == "Perdio" :
                exit = True

            if reply.decode("UTF-8")[1:4] == "Man" :
                exit = True

            print(reply.decode("UTF-8"))
            break

        except:
            print("Cant recieve response\n")
            print("Trying in 5 seg")
            time.sleep(5)


#enviar(s) -- Gestiona los mensajes que seran enviados al servidor. Esta funcion llama a recibir una vez que el 
# mensaje es enviado al cliente
def enviar(s):
    
    while True:

        global exit

        try:

            msg = input("")
            msg = client +": " + msg
            if exit :
                print("SALIDA")
                s.close
                break
            else:
                s.send(msg.encode("UTF-8"))
                start_new_thread(recibir,(s,))


        except:
            print("Something happend\n")
            print("Trying in 5 seg")
            time.sleep(5)

#recibirEspecial(s) -- Recibe un numero. Este sera el numero del cliente
def recibirEspecial(s):
    global client
    client = s.recv(2048).decode("UTF-8")

#######################################################################
##                          VARIABLES GLOBALES                       ##
#######################################################################

exit=False      # Si el cliente envia salir, exit se pone en true y el
                # el programa termina
client = ""

comenzarJ = False
#######################################################################
##                                MAIN                               ##
#######################################################################

def main():

    host, port = ini()
    s = crearSocket()
    intentoConexion(host,port,s)
    recibirEspecial(s)
    print("\nConnection To Server Established!\nThe server is:", host+":"+str(port)+"\n")
    print("Write your messages\n")
    start_new_thread(recibir, (s,))
    start_new_thread(enviar, (s,))
    

    while exit!=True:   # Necesarios para que los hilos no mueran
        pass

    print("\nSorry something went wrong! You have lost connection to the server.:(")
    print("Closing the windows in 5 seg")
    time.sleep(10)

main()