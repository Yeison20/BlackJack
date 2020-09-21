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
labelsarray = []
imagenes = []
indice = 0
#numerocolumna = 1
puntajetotal = 0
contadorposicion = 0

#inicializar las variables
imagendeck = []



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
Decklabel.place(x=205,y=120)



#codigo para ingresar el nombre del jugador
labelentry = Label(contenedor, text = "Nombre del Jugador ", font = ("Arial",15))
labelentry.place(x=420, y=400)
nombre = StringVar()
entrynombre = Entry(contenedor, textvariable = nombre)
entrynombre.place(x=400, y=440)
entrynombre.config(width = 20,font = ("Arial",15))

#crear el boton de PLAY
BotonStart = Button(contenedor, text = "Start Game", font = ("Arial", 10), width = 20, height=2, bg = "#c5ad3d")
BotonStart.place(x=425, y=490)
BotonStart.config(command = lambda :Marcador(str(nombre.get())))


def Marcador(nombre):
    global labelentry, BotonOK, entrynombre, Botoniniciar, BotonStart, Decklabel
    global nombrejugador, TextoBoton, totalmarcador
    #nombrejugador = nombre
    BotonStart.destroy()
    entrynombre.destroy()
    Decklabel.destroy()
    labelentry.destroy()

    framemarcador = Frame(contenedor , bg="#373731")
    framemarcador.config(bd=5, relief="ridge")
    framemarcador.place(width=200, height=90, x=18, y=10)

    #frame para colocar las cartas 
    framecartas = Frame(contenedor)
    framecartas.place(width=680, height=210, x=18, y=417)


    titulomarcador = Label(framemarcador, text = "Partida",font = ("Arial",20, "bold") , fg="#c5ad3d" ,bg="#373731")
    titulomarcador.place(x=50 , y= 10)

    j1marcador = Label(framemarcador, text = "Jugador 1:", font = ("Arial",12), bg="#373731" , fg="white")
    j1marcador.place(x=10 , y= 50)

    nombremarcador = Label(framemarcador, text = nombre, font = ("Arial",12), bg="#373731" , fg="white")
    nombremarcador.place(x=100 , y= 50)

    DeckDir = ".\\" + "/Poker Cards/Images/Deck.png"
    imagendeck.append(setimagen(DeckDir,180,180))
    Decklabel = Label(contenedor, image = imagendeck[1])
    Decklabel.place(x=840,y=10)


    card = random.choice(allcards)
    palo = random.choice(allsymbols)
    carta = card+palo

    imagenes.append(setimagen(DirCartas+carta+".png", 150, 180))
    labelcartas = Label(framecartas, image = imagenes[indice])
    #labelcartas.grid(row = 1, column = numerocolumna, padx = 10, pady = 10)
    labelcartas.place(x=contadorposicion, y = 0)

    

    #TextoBoton.set("Pedir Carta")
    #Botoniniciar = Button(contenedor, textvariable=TextoBoton, font=("Arial", 10), width=45, command = InicioJuego)
    #Botoniniciar.place(x=200, y=376)

    totallabel = Label(framemarcador, text = "Total:", font = ("Arial",10,"bold"), bg = "grey")
    totallabel.grid(row=3, column = 1, sticky = "E" )

    totalmarcador = Label(framemarcador, text= str(puntajetotal), font=("Arial", 10, "bold"), bg="grey")
    totalmarcador.grid(row=3, column=2, sticky="W")

    # Creacion de un Hilo para que tenga un minimo retraso entre cambio de texto
    #hilo=threading.Thread(target=mensaje, args=("Buenas, Jugadores, Vamos a empezar la Partida de BlackJack",))
    #hilo.start()
    #labelentry.config(text = "Buenas, Jugadores, Vamos a empezar la Partida de BlackJack")

ventana.mainloop()