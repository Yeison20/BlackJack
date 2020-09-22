from tkinter import *
from PIL import Image, ImageTk
import os 
import random
import time
import threading
from tkinter import messagebox as tkMessageBox

#print carpetaraiz
carpetaraiz=os.path.dirname(__file__)

#directorio cartas
DirCartas = "."+"\\Poker Cards\\PNG\\"
allcards = ["A","2","3","4","5","6","7","8","9","10","J","Q","K"]
allsymbols = ["H","S","C","D"]
mazo = []

for pinta in allsymbols:
    for valor in allcards:
        mazo.append(valor+pinta)

labelsarray = []
imagenes = []
indice = 0
#numerocolumna = 1
puntajetotal = 0
contadorposicion = 0

#inicializar las variables
imagendeck = []
imagendeck1 = []



def setimagen(nombre,x,y): #carga la imagen
    global imagen #Declaro el uso de una variable global
    img = Image.open(nombre) #cargo la imagen mandada como parametro
    img.thumbnail((x, y), Image.ANTIALIAS) #establezco sus dimensiones y la propiedad antialiasado
    return ImageTk.PhotoImage(img)
    #imagen = ImageTk.PhotoImage(img) #la convierto a un formato soportado por los widgets de tkinter
    #return imagen

#Metodo para centrar la ventana principal 
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
        else:
            BotonStart["state"] = DISABLED



#Creacion de la ventana

ventana = Tk()
ventana.title("BlackJack")
ventana.resizable(0,0) 
contenedor = Frame(ventana, width = 1000, height = 700)
contenedor.pack(fill = "y", expand = True)
center(ventana)
ventana.iconbitmap(".\Poker Cards\Images\Poker Icon 1.ico")




#Etitulo =Label(contenedor,text="BlackJack", font=("Arial",40,"bold"))
#Etitulo.place(x=370,y=20)

#codigo para la imagen de portada
DeckDir = ".\\" + "Poker Cards\Images\logo.png"
imagendeck.append(setimagen(DeckDir,580,630))
Decklabel = Label(contenedor, image = imagendeck[0])
Decklabel.place(x=205,y=20)

#codigo para ingresar la IP
labelIP = Label(contenedor, text = "IP Address", font = ("Arial",15))
labelIP.place(x=300, y=320)
ip = StringVar()
entryIP = Entry(contenedor,textvariable = ip)
entryIP.place(x=420, y=320)
entryIP.config(width = 20,font = ("Arial",15))
entryIP.insert(0,"Hola ")

#codigo para ingresar el Host
labelHost = Label(contenedor, text = "Host", font = ("Arial",15))
labelHost.place(x=360, y=360)
host = int()
entryHost = Entry(contenedor, textvariable = host)
entryHost.place(x=420, y=360)
entryHost.config(width = 20,font = ("Arial",15))

#crear el boton de PEnviar datos
BotonEnviar = Button(contenedor, text = "Enviar", font = ("Arial", 15), width = 12, height=1, bg = "#c5ad3d", command=switch)
BotonEnviar.place(x=460, y=400)

#codigo para ingresar el nombre del jugador
labelentry = Label(contenedor, text = "Nombre", font = ("Arial",15))
labelentry.place(x=330, y=460)
nombre = StringVar()
entrynombre = Entry(contenedor, textvariable = nombre)
entrynombre.place(x=420, y=460)
entrynombre.config(width = 20,font = ("Arial",15))

#codigo para ingresar el numero de la C.C.
labelCedula = Label(contenedor, text = "Cedula:", font = ("Arial",15))
labelCedula.place(x=330, y=500)
cedula = StringVar()
entryCedula = Entry(contenedor, textvariable = cedula)
entryCedula.place(x=420, y=500)
entryCedula.config(width = 20,font = ("Arial",15))

#crear el boton de PLAY
BotonStart = Button(contenedor, text = "Jugar", font = ("Arial", 14), width = 12, height=1, bg = "#c5ad3d", state=DISABLED)
BotonStart.place(x=460, y=560)
BotonStart.config(command = lambda :Marcador(str(nombre.get())))

#frame para colocar las cartas 
framecartas = Frame(contenedor)
framecartas.place_forget()


def Marcador(nombre):

    
        
    global labelentry, BotonOK, entrynombre, Botoniniciar, BotonStart, Decklabel
    global nombrejugador, TextoBoton, totalmarcador
    global allcards, allsymbols, indice, mazo
    #nombrejugador = nombre

   
    
    BotonStart.destroy()
    entrynombre.destroy()
    Decklabel.destroy()
    labelentry.destroy()
    BotonEnviar.destroy()
    labelCedula.destroy()
    entryCedula.destroy()
    labelIP.destroy()
    entryIP.destroy()
    labelHost.destroy()
    entryHost.destroy()
    #frame para colocar las cartas 
    framecartas.place(width=800, height=210, x=18, y=430)
  
    #Marcador Crupier -------------------------------------------------------------
    framemarcador1 = Frame(contenedor , bg="#373731")
    framemarcador1.config(bd=5, relief="ridge")
    framemarcador1.place(width=200, height=90, x=18, y=10)
   

    titulomarcador = Label(framemarcador1, text = "Marcador",font = ("Arial",12, "bold") , fg="#c5ad3d" ,bg="#373731")
    titulomarcador.place(x=50 , y= 3)

    j1marcador = Label(framemarcador1, text = "Crupier", font = ("Arial",12), bg="#373731" , fg="white")
    j1marcador.place(x=10 , y= 25)

    j1marcador = Label(framemarcador1, text = "Puntaje:", font = ("Arial",12), bg="#373731" , fg="white")
    j1marcador.place(x=10 , y= 50)

    #----------------------------------------------------------------------#

    #Marcador Jugador
    framemarcador = Frame(contenedor , bg="#373731")
    framemarcador.config(bd=5, relief="ridge")
    framemarcador.place(width=200, height=90, x=18, y=320)

    titulomarcador = Label(framemarcador, text = "Marcador",font = ("Arial",12, "bold") , fg="#c5ad3d" ,bg="#373731")
    titulomarcador.place(x=50 , y= 3)

    j1marcador = Label(framemarcador, text = "Jugador 1:", font = ("Arial",12), bg="#373731" , fg="white")
    j1marcador.place(x=10 , y= 25)

    j1marcador = Label(framemarcador, text = "Puntaje:", font = ("Arial",12), bg="#373731" , fg="white")
    j1marcador.place(x=10 , y= 50)

    nombremarcador = Label(framemarcador, text = nombre, font = ("Arial",12), bg="#373731" , fg="white")
    nombremarcador.place(x=100 , y= 50)

    #-------------------------------------------------------------------#

    #--------------------- Frame Para Crupier--------------------------
    framecartas1 = Frame(contenedor)
    framecartas1.place(width=680, height=210, x=18, y=110)

    card = random.choice(allcards)
    palo = random.choice(allsymbols)
    carta = random.choice(mazo)

    print("TAMANO Antes DE BORRA")
    print(len(mazo))

    mazo.remove(carta)

    print("TAMANO DESPUES DE BORRA")
    print(len(mazo))

    imagenes.append(setimagen(DirCartas+carta+".png", 150, 180))
    labelcartas = Label(framecartas1, image = imagenes[indice])
    #labelcartas.grid(row = 1, column = numerocolumna, padx = 10, pady = 10)
    labelcartas.place(x=contadorposicion, y = 0)
    indice += 1
    
   



    
    #--------------- Imagen de las Cartas ---------------------
    DeckDir = ".\\" + "/Poker Cards/Images/Deck.png"
    imagendeck.append(setimagen(DeckDir,180,180))
    Decklabel = Label(contenedor, image = imagendeck[1])
    Decklabel.place(x=840,y=10)


    #-----------------------Botones Para el jugador-----------------------------------

    DeckDir = ".\\" + "/Poker Cards/Images/carta.png"
    imagendeck.append(setimagen(DeckDir,80,40))
    Decklabel = Button(contenedor, image = imagendeck[2] , text="Pedir Carta", compound="top" , command = pedirCarta)
    Decklabel.place(x=890,y=400)

    DeckDir = ".\\" + "/Poker Cards/Images/plantarse.png"
    imagendeck.append(setimagen(DeckDir,80,40))
    Decklabel = Button(contenedor, image = imagendeck[3] , text="  Plantarse ", compound="top")
    Decklabel.place(x=890,y=480)

    DeckDir = ".\\" + "/Poker Cards/Images/salida.png"
    imagendeck.append(setimagen(DeckDir,80,40))
    Decklabel = Button(contenedor, image = imagendeck[4] , text="     Salir      ", compound="top")
    Decklabel.place(x=890,y=560)

    #----------------------------------------------------------------------------------------

  

    


def pedirCarta():

    global indice,  contadorposicion
    global allcards, allsymbols, indice
   

    card = random.choice(allcards)
    palo = random.choice(allsymbols)
    carta = random.choice(mazo)

    print("TAMANO Antes EN JUGADOR DE BORRA")
    print(len(mazo))

    mazo.remove(carta)

    print("TAMANO DESPUES EN JUGADOR DE BORRA")
    print(len(mazo))


    imagenes.append(setimagen(DirCartas+carta+".png", 150, 180))
    labelcartas = Label(framecartas, image = imagenes[indice])
    #labelcartas.grid(row = 1, column = numerocolumna, padx = 10, pady = 10)
    labelcartas.place(x=contadorposicion, y = 0)

    contadorposicion+=130
    #numerocolumna+= 1
    indice+=1
    labelsarray.append(labelcartas)

    #imagef = PhotoImage(file ="table.png")
    #fondo = Label(contenedor, image = imagef).place(x=0,y=0)

    #TextoBoton.set("Pedir Carta")
    #Botoniniciar = Button(contenedor, textvariable=TextoBoton, font=("Arial", 10), width=45, command = InicioJuego)
    #Botoniniciar.place(x=200, y=376)

    #totallabel = Label(framemarcador, text = "Total:", font = ("Arial",10,"bold"), bg = "grey")
    #totallabel.grid(row=3, column = 1, sticky = "E" )

    #totalmarcador = Label(framemarcador, text= str(puntajetotal), font=("Arial", 10, "bold"), bg="grey")
    #totalmarcador.grid(row=3, column=2, sticky="W")

    # Creacion de un Hilo para que tenga un minimo retraso entre cambio de texto
    #hilo=threading.Thread(target=mensaje, args=("Buenas, Jugadores, Vamos a empezar la Partida de BlackJack",))
    #hilo.start()
    #labelentry.config(text = "Buenas, Jugadores, Vamos a empezar la Partida de BlackJack")
    

    
ventana.mainloop()