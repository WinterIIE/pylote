"""This module implements Models used to play Belote game."""

import random

class Player:
    """This class implements players."""
    def __init__(self, name, hand=[]):
        self.name = name
        self.hand = list(hand)

class Card:
    """This class implements cards."""
    #dictionnaire de cartes
    CARD_DICT = {
        7 : '7',
        8 : '8',
        9 : '9',
        10 : '10',
        11 : 'Valet',
        12 : 'Dame',
        13 : 'Roi',
        14 : 'As'
    }

    #Declaration des valeurs & couleurs
    def __init__(self, valeur, couleur):
        self.valeur = valeur
        self.couleur = couleur

    #Affichage d'une carte (comprehensible)
    def __repr__(self):
        return f"{self.CARD_DICT.get(self.valeur)} de {self.couleur}"

class Game:
    """This class implements a game of belote."""

    #dictionnaire valeurs atouts
    POINTS_ATOUT = {
        7 : 0,
        8 : 0,
        9 : 14,
        10 : 10,
        11 : 20,
        12 : 3,
        13 : 4,
        14 : 11
    }

    #dictionnaire valeurs sans atouts
    POINTS_SANS_ATOUT = {
        7 : 0,
        8 : 0,
        9 : 0,
        10 : 10,
        11 : 2,
        12 : 3,
        13 : 4,
        14 : 11
    }

    #Declaration des atouts & Score & Paquet de cartes & players
    def __init__(self, players, trump=None, score=(0,0), cards=None, position=0):
        self.players = players
        self.trump = trump
        self.score = score
        if cards is None:
            self.cards = self.create_deck()
        else:
            self.cards = cards
        self.position = position

    #creation d'un jeu de cartes
    def create_deck(self):
        cards = []
        for i in ['Coeur', 'Carreau', 'Pique', 'Trefle']:
            for j in range(7,15):
                cards.append(Card(j,i))
        random.shuffle(cards)
        return cards

    #couper le jeu de cartes
    def cut_deck(self, index):
        self.cards = self.cards[index:] + self.cards[:index]

    #distribuer le jeu de cartes
    def distri_deck(self, reversed=False):
        if reversed:
            for i in range(4):
                self.players[(self.position + i) % 4].hand += self.cards[:2]
                self.cards = self.cards[2:]

            for i in range(4):
                self.players[(self.position + i) % 4].hand += self.cards[:3]
                self.cards = self.cards[3:]

        else:
            for i in range(4):
                self.players[self.position + i % 4].hand += self.cards[:3]
                self.cards = self.cards[3:]

            for i in range(4):
                self.players[self.position + i % 4].hand += self.cards[:2]
                self.cards = self.cards[2:]

#lancement du Jeu
game = Game([Player('Tristan'), Player('Alexis'), Player('Baptiste'), Player('Tiffany')])
#game = Game(["Tristan", "Alexis"], Coeur, (100, 0), cards)
print(game.cards)
print(f"Le jeu comporte {len(game.cards)} cartes.")
print(f"Les joueurs en jeu sont {', '.join([game.players[i].name for i in range(4)])}.")
print(f"L'atout est {game.trump}.")
print(f"Le score actuel est de: {game.score[0]} pour Nous et {game.score[1]} pour Eux.")

game.distri_deck(True)
for i in range(4):
    print(f"Le jeu de {game.players[i].name} est {game.players[i].hand}.")
