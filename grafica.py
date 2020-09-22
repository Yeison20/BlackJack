from tkinter import *
from PIL import Image, ImageTk
import os
import random
import time
import threading
from tkinter import messagebox as tkMessageBox
from blackJack import *

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
    host = "192.168.0.19"
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

    #host, port = ini()
    host = entryIP.get()
    port = int(entryHost.get())

    s = crearSocket()
    intentoConexion(host,port,s)
    recibirEspecial(s)
    print("\nConnection To Server Established!\nThe server is:", host+":"+str(port)+"\n")
    print("Write your messages\n")

    '''start_new_thread(recibir, (s,))
    start_new_thread(enviar, (s,))
    

    while exit!=True:   # Necesarios para que los hilos no mueran
        pass

    print("\nSorry something went wrong! You have lost connection to the server.:(")
    print("Closing the windows in 5 seg")
    time.sleep(10)'''

# print carpetaraiz
carpetaraiz = os.path.dirname(__file__)

# directorio cartas
DirCartas = "."+"\\Poker Cards\\PNG\\"
allcards = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
allsymbols = ["H", "S", "C", "D"]
mazo = []
mano = []

jugador = Jugador()
crupier = Jugador()

for pinta in allsymbols:
    for valor in allcards:
        mazo.append(valor+pinta)


def contar_mano(mano):
    contador = 0
    ases = 0
    for c in mano:
        if(c[0] == "A"):
            ases += 1
        else:
            if (c[0] == "J" or c[0] == "K" or c[0] == "Q" or (c[0] == "1" and c[1] == "0")):
                contador += 10
            else:
                contador += int(c[0])
    contador += ases
    ases_usados = 0
    while(contador <= 11 and ases_usados < ases):
        contador += 10
        ases_usados += 1
    return contador


labelsarray = []
imagenes = []
indice = 0
# numerocolumna = 1
puntajetotal = 0
contadorposicion = 0
totalmarcador = ""
totalsaldo = 0

# inicializar las variables
imagendeck = []
imagendeck1 = []


def setimagen(nombre, x, y):  # carga la imagen
    global imagen  # Declaro el uso de una variable global
    img = Image.open(nombre)  # cargo la imagen mandada como parametro
    # establezco sus dimensiones y la propiedad antialiasado
    img.thumbnail((x, y), Image.ANTIALIAS)
    return ImageTk.PhotoImage(img)
    # imagen = ImageTk.PhotoImage(img) #la convierto a un formato soportado por los widgets de tkinter
    # return imagen

# Metodo para centrar la ventana principal


def center(toplevel):
    toplevel.update_idletasks()
    w = toplevel.winfo_screenwidth()
    h = toplevel.winfo_screenheight()
    size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
    x = w/2 - size[0]/2
    y = h/2 - size[1]/2
    toplevel.geometry("%dx%d+%d+%d" % (size + (x, y)))


def switch():
    if BotonEnviar["state"] == NORMAL:
        BotonStart["state"] = NORMAL
        main()
    else:
        BotonStart["state"] = DISABLED



# Creacion de la ventana
ventana = Tk()
ventana.title("BlackJack")
ventana.resizable(0, 0)
contenedor = Frame(ventana, width=1000, height=700)
contenedor.pack(fill="y", expand=True)
center(ventana)
ventana.iconbitmap(".\Poker Cards\Images\Poker Icon 1.ico")


# Etitulo =Label(contenedor,text="BlackJack", font=("Arial",40,"bold"))
# Etitulo.place(x=370,y=20)

# codigo para la imagen de portada
DeckDir = ".\\" + "Poker Cards\Images\logo.png"
imagendeck.append(setimagen(DeckDir, 580, 630))
Decklabel = Label(contenedor, image=imagendeck[0])
Decklabel.place(x=205, y=20)

# codigo para ingresar la IP
labelIP = Label(contenedor, text="IP Address", font=("Arial", 15))
labelIP.place(x=300, y=320)
ip = StringVar()
entryIP = Entry(contenedor, textvariable=ip)
entryIP.place(x=420, y=320)
entryIP.config(width=20, font=("Arial", 15))
#entryIP.insert(0, "19")

# codigo para ingresar el Host
labelHost = Label(contenedor, text="Host", font=("Arial", 15))
labelHost.place(x=360, y=360)
host = int()
entryHost = Entry(contenedor, textvariable=host)
entryHost.place(x=420, y=360)
entryHost.config(width=20, font=("Arial", 15))
entryHost.insert(0, "55")


# crear el boton de PEnviar datos
BotonEnviar = Button(contenedor, text="Enviar", font=(
    "Arial", 15), width=12, height=1, bg="#c5ad3d", command=switch)
BotonEnviar.place(x=460, y=400)

# codigo para ingresar el nombre del jugador
labelentry = Label(contenedor, text="Nombre", font=("Arial", 15))
labelentry.place(x=330, y=460)
nombre = StringVar()
entrynombre = Entry(contenedor, textvariable=nombre)
entrynombre.place(x=420, y=460)
entrynombre.config(width=20, font=("Arial", 15))

# codigo para ingresar el numero de la C.C.
labelSaldo = Label(contenedor, text="Saldo:", font=("Arial", 15))
labelSaldo.place(x=330, y=500)
entrySaldo = Entry(contenedor)
entrySaldo.place(x=420, y=500)
entrySaldo.config(width=20, font=("Arial", 15))


# crear el boton de PLAY
BotonStart = Button(contenedor, text="Jugar", font=(
    "Arial", 14), width=12, height=1, bg="#c5ad3d", state=DISABLED)
BotonStart.place(x=460, y=560)
BotonStart.config(command=lambda: Marcador(str(nombre.get())))


# frame para colocar las cartas
framecartas = Frame(contenedor)
framecartas.place_forget()

framemarcador = Frame(contenedor, bg="#373731")
framemarcador.place_forget()

framemarcador1 = Frame(contenedor, bg="#373731")
framemarcador1.place_forget()

framecartas1 = Frame(contenedor)
framecartas1.place_forget()



def ReiniciarJuego():

    global saldo

    opcion = tkMessageBox.askyesno("Retry?", "Quisieras volver a Jugar?")

    if(opcion==True):
        if saldo > 0:
            global indice, puntajetotal, contadorposicion, totalmarcador, jugador , crupier, totalmarcador1, mazo, saldoLabel
            del labelsarray[:]
            del imagenes[:]
            indice = 0
            puntajetotal = 0
            contadorposicion = 0
            totalmarcador.config(text = "    ")
            totalmarcador1.config(text = "   ")
            jugador.mano = []
            crupier.mano = []
            Decklabel1["state"] = NORMAL
            Decklabel2["state"] = NORMAL
            mazo = []
            

            for pinta in allsymbols:
                for valor in allcards:
                    mazo.append(valor+pinta)
            
            
            carta = random.choice(mazo)
            crupier.mano.append(carta)

            imagenes.append(setimagen(DirCartas+carta+".png", 150, 180))
            labelcartas = Label(framecartas1, image=imagenes[indice])
            # labelcartas.grid(row = 1, column = numerocolumna, padx = 10, pady = 10)
            labelcartas.place(x=contadorposicion, y=0)
            indice += 1

        else:
            tkMessageBox.showinfo("SIN SALDO!", "No puede seguir apostando, saldo es de 0 ")
            ventana.destroy()
        

saldo = 0

def Marcador(nombre):

    global labelentry, BotonOK, entrynombre, Botoniniciar, BotonStart, Decklabel, Decklabel1,Decklabel2 
    global nombrejugador, TextoBoton, totalmarcador  , saldoLabel , saldomarcador, saldo
    global allcards, allsymbols, indice, mazo
    # nombrejugador = nombre
    
    saldo = entrySaldo.get()

    BotonStart.destroy()
    entrynombre.destroy()
    Decklabel.destroy()
    labelentry.destroy()
    BotonEnviar.destroy()
    labelSaldo.destroy()
    entrySaldo.destroy()
    labelIP.destroy()
    entryIP.destroy()
    labelHost.destroy()
    entryHost.destroy()
    # frame para colocar las cartas
    framecartas.place(width=800, height=210, x=18, y=440)

    framemarcador.config(bd=5, relief="ridge")
    framemarcador.place(width=200, height=110, x=18, y=320)

    framecartas1.place(width=680, height=210, x=18, y=110)

    # Marcador Crupier -------------------------------------------------------------

    framemarcador1.config(bd=5, relief="ridge")
    framemarcador1.place(width=200, height=90, x=18, y=10)

    titulomarcador = Label(framemarcador1, text="Marcador", font=(
        "Arial", 12, "bold"), fg="#c5ad3d", bg="#373731")
    titulomarcador.place(x=50, y=3)

    j1marcador = Label(framemarcador1, text="Crupier",
                       font=("Arial", 12), bg="#373731", fg="white")
    j1marcador.place(x=10, y=25)

    j1marcador = Label(framemarcador1, text="Puntaje:",
                       font=("Arial", 12), bg="#373731", fg="white")
    j1marcador.place(x=10, y=50)

    #----------------------------------------------------------------------#

    # Marcador Jugador

    titulomarcador = Label(framemarcador, text="Marcador", font=(
        "Arial", 12, "bold"), fg="#c5ad3d", bg="#373731")
    titulomarcador.place(x=50, y=3)

    j1marcador = Label(framemarcador, text="Jugador 1:",
                       font=("Arial", 12), bg="#373731", fg="white")
    j1marcador.place(x=10, y=25)

    j1marcador = Label(framemarcador, text="Puntaje:",
                       font=("Arial", 12), bg="#373731", fg="white")
    j1marcador.place(x=10, y=50)

    saldomarcador = Label(framemarcador, text="Saldo:",
                       font=("Arial", 12), bg="#373731", fg="white")
    saldomarcador.place(x=10, y=70)

    saldomarcador = Label(contenedor, text="La apuesta es de 100", font=("Arial", 14), fg="black")
    saldomarcador.place(x=250, y=20)

    saldoLabel = Label(framemarcador, text=saldo, font=("Arial", 12), bg="#373731", fg="white")
    saldoLabel.place(x=100, y=70)

    nombremarcador = Label(framemarcador, text=nombre, font=(
        "Arial", 12), bg="#373731", fg="white")
    nombremarcador.place(x=100, y=25)

    #-------------------------------------------------------------------#

    # --------------------- Frame Para Crupier--------------------------

    card = random.choice(allcards)
    palo = random.choice(allsymbols)
    carta = random.choice(mazo)

    print("TAMANO Antes DE BORRA")
    print(len(mazo))

    mazo.remove(carta)

    print("TAMANO DESPUES DE BORRA")
    print(len(mazo))

    crupier.mano.append(carta)

    imagenes.append(setimagen(DirCartas+carta+".png", 150, 180))
    labelcartas = Label(framecartas1, image=imagenes[indice])
    # labelcartas.grid(row = 1, column = numerocolumna, padx = 10, pady = 10)
    labelcartas.place(x=contadorposicion, y=0)
    indice += 1

    # --------------- Imagen de las Cartas ---------------------
    DeckDir = ".\\" + "/Poker Cards/Images/Deck.png"
    imagendeck.append(setimagen(DeckDir, 180, 180))
    Decklabel = Label(contenedor, image=imagendeck[1])
    Decklabel.place(x=840, y=10)

    # -----------------------Botones Para el jugador-----------------------------------

    DeckDir = ".\\" + "/Poker Cards/Images/carta.png"
    imagendeck.append(setimagen(DeckDir, 80, 40))
    Decklabel2 = Button(contenedor, image=imagendeck[2], text="Pedir Carta", compound="top", command=pedirCarta)
    Decklabel2.place(x=890, y=400)

    DeckDir = ".\\" + "/Poker Cards/Images/plantarse.png"
    imagendeck.append(setimagen(DeckDir, 80, 40))
    Decklabel1 = Button(contenedor, image=imagendeck[3], text="  Plantarse ", compound="top", command=plantarse)
    Decklabel1.place(x=890, y=480)

    
    

    DeckDir = ".\\" + "/Poker Cards/Images/salida.png"
    imagendeck.append(setimagen(DeckDir, 80, 40))
    Decklabel = Button(
        contenedor, image=imagendeck[4], text="     Salir      ", compound="top", command=cerrar)
    Decklabel.place(x=890, y=560)

    # ----------------------------------------------------------------------------------------

    
def addCrupier(carta):
    global DirCartas, imagenes, indice, contadorposicion , totalmarcador

    totalmarcador = Label(framemarcador1, text=contar_mano(crupier.mano), font=("Arial", 13), fg="white", bg="#373731")
    totalmarcador.place(x=70, y=50)

    imagenes.append(setimagen(DirCartas+carta+".png", 150, 180))
    labelcartas = Label(framecartas1, image=imagenes[indice])
    # labelcartas.grid(row = 1, column = numerocolumna, padx = 10, pady = 10)
    labelcartas.place(x=contadorposicion, y=0)
    indice += 1
    contadorposicion += 130

    time.sleep(2)

def plantarse():

    global crupier, jugador, indice, mazo, contadorposicion , Decklabel1 ,Decklabel2, totalsaldo, saldo

    
    if len(jugador.mano) >= 2:
        contadorposicion = 130

        while (contar_mano(crupier.mano) < contar_mano(jugador.mano) and contar_mano(crupier.mano) < 21):



            carta = random.choice(mazo)

            print("TAMANO Antes DE BORRA")
            print(len(mazo))

            mazo.remove(carta)

            print("TAMANO DESPUES DE BORRA")
            print(len(mazo))

            crupier.mano.append(carta)

            print("total CRUPIER")
            print(contar_mano(crupier.mano))

            addCrupier(carta)


        if contar_mano(crupier.mano) > 21:
            tkMessageBox.showinfo(
                "GANO!", "Perdio la maquina!\nTotal: " + str(contar_mano(crupier.mano)))
            saldo = int(saldo) + 100
           

        elif contar_mano(crupier.mano) == contar_mano(jugador.mano):
            tkMessageBox.showinfo(
                "EMPATE!", "EMPATE!\nTotal: " + str(contar_mano(crupier.mano)))

        else:
            tkMessageBox.showinfo(
                "PERDIO!", "Gano la maquina!\nTotal: " + str(contar_mano(crupier.mano)))
            saldo = int(saldo) - 100
            

        Decklabel1["state"] = DISABLED
        Decklabel2["state"] = DISABLED
        
        saldoLabel = Label(framemarcador, text=saldo, font=("Arial", 12), bg="#373731", fg="white")
        saldoLabel.place(x=100, y=70)

        ReiniciarJuego()
    else:
        tkMessageBox.showinfo("Aviso","Tiene que tomar 2 cartas antes de plantarse")
    

def pedirCarta():

    global indice,  contadorposicion, totalmarcador , totalmarcador1
    global allcards, allsymbols, indice, jugador, saldo

    card = random.choice(allcards)
    palo = random.choice(allsymbols)
    carta = random.choice(mazo)

    print("TAMANO Antes EN JUGADOR DE BORRA")
    print(len(mazo))

    mazo.remove(carta)

    print("TAMANO DESPUES EN JUGADOR DE BORRA")
    print(len(mazo))

    jugador.mano.append(carta)

    print("total")
    print(contar_mano(jugador.mano))

    imagenes.append(setimagen(DirCartas+carta+".png", 150, 180))
    labelcartas = Label(framecartas, image=imagenes[indice])
    # labelcartas.grid(row = 1, column = numerocolumna, padx = 10, pady = 10)
    labelcartas.place(x=contadorposicion, y=0)

    contadorposicion += 130
    # numerocolumna+= 1
    indice += 1
    labelsarray.append(labelcartas)

    totalmarcador1 = Label(framemarcador, text=contar_mano(jugador.mano), font=("Arial", 13), fg="white", bg="#373731")
    totalmarcador1.place(x=70, y=50)

    # imagef = PhotoImage(file ="table.png")
    # fondo = Label(contenedor, image = imagef).place(x=0,y=0)

    # TextoBoton.set("Pedir Carta")
    # Botoniniciar = Button(contenedor, textvariable=TextoBoton, font=("Arial", 10), width=45, command = InicioJuego)
    # Botoniniciar.place(x=200, y=376)

    # Creacion de un Hilo para que tenga un minimo retraso entre cambio de texto
    # hilo=threading.Thread(target=mensaje, args=("Buenas, Jugadores, Vamos a empezar la Partida de BlackJack",))
    # hilo.start()
    # labelentry.config(text = "Buenas, Jugadores, Vamos a empezar la Partida de BlackJack")

    if contar_mano(jugador.mano) > 21:
        tkMessageBox.showinfo(
            "PERDIO!", "Perdio, la suma de las cartas es mayor a 21!\nTotal: " + str(contar_mano(jugador.mano)))
        saldo = int(saldo) - 100

        saldoLabel = Label(framemarcador, text=saldo, font=("Arial", 12), bg="#373731", fg="white")
        saldoLabel.place(x=100, y=70)
        ReiniciarJuego()

def cerrar():
    ventana.destroy()

ventana.mainloop()
