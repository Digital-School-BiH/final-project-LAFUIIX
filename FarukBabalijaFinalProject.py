import tkinter as tk
import random

# osnovne dimenzije
sirina = 600
visina = 400
velicina_polja = 20
brzina = 100
pocetna_duzina = 3

boja_pozadine = "black"
boja_zmije = "green"
boja_hrane = "red"

smjer = "desno"
poeni = 0

class Zmija:
    def __init__(self):
        self.koordinate = []
        self.kvadrati = []

        for i in range(pocetna_duzina):
            self.koordinate.append([0, 0])

        for x, y in self.koordinate:
            kvadrat = platno.create_rectangle(x, y, x + velicina_polja, y + velicina_polja, fill=boja_zmije)
            self.kvadrati.append(kvadrat)

class Hrana:
    def __init__(self):
        x = random.randint(0, (sirina // velicina_polja) - 1) * velicina_polja
        y = random.randint(0, (visina // velicina_polja) - 1) * velicina_polja
        self.pozicija = [x, y]

        platno.create_oval(x, y, x + velicina_polja, y + velicina_polja, fill=boja_hrane, tag="hrana")

def pokreni_potez(zmija, hrana):
    global poeni, brzina
    
    x, y = zmija.koordinate[0]

    if smjer == "gore":
        y -= velicina_polja
    if smjer == "dolje":
        y += velicina_polja
    if smjer == "lijevo":
        x -= velicina_polja
    if smjer == "desno":
        x += velicina_polja

    zmija.koordinate.insert(0, [x, y])

    novi = platno.create_rectangle(x, y, x + velicina_polja, y + velicina_polja, fill=boja_zmije)
    zmija.kvadrati.insert(0, novi)

    if x == hrana.pozicija[0] and y == hrana.pozicija[1]:
        platno.delete("hrana")
        hrana.__init__()

        poeni += 1
        labela_poeni.config(text=f"Poeni: {poeni}")

        if brzina > 20:
            brzina -= 3
            
    else:
        del zmija.koordinate[-1]
        platno.delete(zmija.kvadrati[-1])
        del zmija.kvadrati[-1]

    if provjeri_sudar(zmija):
        kraj_igre()
    else:
        prozor.after(brzina, pokreni_potez, zmija, hrana)

def promijeni_smjer(event):
    global smjer
    taster = event.keysym

    if taster == "Left" and smjer != "desno":
        smjer = "lijevo"
    if taster == "Right" and smjer != "lijevo":
        smjer = "desno"
    if taster == "Up" and smjer != "dolje":
        smjer = "gore"
    if taster == "Down" and smjer != "gore":
        smjer = "dolje"

def provjeri_sudar(zmija):
    x, y = zmija.koordinate[0]

    if x < 0 or x >= sirina or y < 0 or y >= visina:
        return True

    for dio in zmija.koordinate[1:]:
        if dio == [x, y]:
            return True

    return False

def kraj_igre():
    platno.delete("all")
    platno.create_text(sirina/2, visina/2, text="GAME OVER", fill="red", font=("Arial", 30))
    platno.create_text(sirina/2, visina/2 + 30, text=f"Poeni: {poeni}", fill="green", font=("Arial", 20))

# Glavni dio
prozor = tk.Tk()
prozor.title("ZMIJA")
prozor.resizable(False, False)

platno = tk.Canvas(prozor, bg=boja_pozadine, width=sirina, height=visina)
platno.pack()

labela_poeni = tk.Label(prozor, text=f"Poeni: {poeni}", font=("Arial", 14))
labela_poeni.pack()

prozor.update()
x_poz = (prozor.winfo_screenwidth() // 2) - (sirina // 2)
y_poz = (prozor.winfo_screenheight() // 2) - (visina // 2)
prozor.geometry(f"{sirina}x{visina}+{x_poz}+{y_poz}")

prozor.bind("<Key>", promijeni_smjer)

zmija = Zmija()
hrana = Hrana()
pokreni_potez(zmija, hrana)
