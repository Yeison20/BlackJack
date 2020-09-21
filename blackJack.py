import random

#Clase carta: esta calse sirve para crear las cartas con su correspodiente palo  y valor
class Carta:
    def __init__(self, p , v):
        self.pinta = p
        self.valor = v
    
    def get_valor(self):
        if(self.valor in ["J", "Q", "K"]):
            return 10
        return self.valor

#Clase mazo: esta clase sirve para crear el total de cartas que hay en un mazo en esta caso son 52
class Mazo:
    def __init__(self):
        self.mazo = []
        for pinta in ['♥','♦','♣','♠']:
            for valor in range(2, 11):
                self.mazo.append(Carta(pinta,valor))
            for valor in ["J" , "Q" , "K" , "A"]:
                self.mazo.append(Carta(pinta,valor))
        random.shuffle(self.mazo)

    def mostrar_mazo(self):
        for c in self.mazo:
            print(str(c.valor) + c.pinta)
    
    def dar_una_carta(self, j):
        j.recibir_carta(self.mazo[0])
        self.mazo.remove(self.mazo[0])        


#clase jugador: se crea un jugador para asignarle cartas, mostrar las cartas del jugador y tener la suma de las cartas del jugador
class Jugador:
    def __init__(self):
        self.mano = []
        self.nombre = ""
        self.cedula = ""

    def recibir_carta(self, c):
        self.mano.append(c)

    def mostrar_mano(self):
        for c in self.mano:
            print(str(c.valor) + c.pinta , end = " ")
        print("-> " + str(self.contar_mano()))
    
    def mostrar_mano_string(self):
        cadena = ""
        for c in self.mano:
            cadena = cadena + str(c.valor) + c.pinta + " "
        cadena = cadena + "-> " + str(self.contar_mano())
        return cadena

    def contar_mano(self):
        contador = 0
        ases = 0
        for c in self.mano:
            if(c.get_valor() == "A"):
                ases += 1
            else:
                contador += c.get_valor()
        contador += ases
        ases_usados = 0
        while(contador <= 11 and ases_usados < ases):
            contador += 10
            ases_usados += 1 
        return contador

"""
m = Mazo()

j = Jugador()
pc = Jugador()


m.dar_una_carta(j)
m.dar_una_carta(j)

m.dar_una_carta(pc)

print("MANO JUGADOR  " + j.mostrar_mano_string())
while(j.contar_mano() < 21):
   
    print("Mano PC  " + pc.mostrar_mano_string())
    print("\n¿Qué desea hacer (JUGADOR) ?")
    print("1. Pedir carta")
    print("2. Plantarse")
    r = int(input())
    if(r == 1):
        m.dar_una_carta(j)
    if(r == 2):
        break
    print("MANO JUGADOR  " + j.mostrar_mano_string())

m.dar_una_carta(pc)
print("Mano PC  " + pc.mostrar_mano_string())

if j.contar_mano() <= 21 :
    while (pc.contar_mano() <= j.contar_mano() or pc.contar_mano() < 21 ):
        m.dar_una_carta(pc)
        print("Mano PC  " + pc.mostrar_mano_string())

    if pc.contar_mano() > 21 :
        print("\nMano PC  " + pc.mostrar_mano_string())
        print("Perdio la maquina")

    elif pc.contar_mano() == j.contar_mano() :
        print("\nMano PC  " + pc.mostrar_mano_string())
        print("\nMANO JUGADOR  " + j.mostrar_mano_string())
        print("EMPATE")

    else :
        print("\nMano PC  " + pc.mostrar_mano_string())
        print("Gano La Maquina")
        
else :
    print("\nMano PC  " + pc.mostrar_mano_string())
    print("Gano la Maquina")
"""