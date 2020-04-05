"""This module implements Models used to play Belote game."""

import random

class Player:
    """This class implements players."""
    def __init__(self, name, hand=[]):
        self.name = name
        self.hand = list(hand)

    def controle_couleur(self, couleur):
        bool = False
        for card in self.hand:
            if card.couleur == couleur:
                bool = True
                break
        return bool

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
    def __init__(self, players, trump=None, score=(0,0), cards=None, position=0, dealer=None, tour=0, pli=[]):
        self.players = players
        self.trump = trump
        self.score = score
        if cards is None:
            self.cards = self.create_deck()
        else:
            self.cards = cards
        self.position = position
        self.dealer = dealer
        self.tour = tour
        self.pli = pli

    def set_trump(self, trump):
        self.trump = trump

    def set_dealer(self,dealer):
        self.dealer = dealer

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
                self.players[(self.position + i) % 4].hand += self.cards[:3]
                self.cards = self.cards[3:]

            for i in range(4):
                self.players[(self.position + i) % 4].hand += self.cards[:2]
                self.cards = self.cards[2:]

    def distri_deck_sec(self):
            for i in range(4):
                if self.players[(self.position + i) % 4].name == self.dealer.name:
                    self.players[(self.position + i) % 4].hand += self.cards[:2]
                    self.cards = self.cards[2:]
                else:
                    self.players[(self.position + i) % 4].hand += self.cards[:3]
                    self.cards = self.cards[3:]

    # jeu de carte retabli si aucun joueur ne choisit l atout.
    def redistri(self):
        for i in range(4):
            self.cards += self.players[(self.position + i) % 4].hand
        tour += 1
        if tour == 3:
            self.position = (self.postion + 1) % 4
            tour = 0

    # carte d'atout donnee au dealer
    def distri_carte_atout(self):
        self.dealer.hand.append(self.cards.pop(0))

    #inserer une carte dans le pli
    def add_to_pli(self, index):
        self.pli.append(self.players.hand.pop(index))
        if len(self.pli)==4:
            self.win_pli()

    #gerer le gagnant du pli
    def win_pli(self):
        return self.controle_atout()

    #controle atouts
    def controle_atout(self):
        atout = [card for card in self.pli if card.couleur == self.trump]
        if len(atout) != 0:
            atout_max = max(atout, key=lambda x: self.POINTS_ATOUT[x.valeur])
            if [self.POINTS_ATOUT[card.valeur] for card in atout].count(self.POINTS_ATOUT[atout_max.valeur]) > 1:
                atout_max = max(atout, key=lambda x: x.valeur)
            return self.pli.index(atout_max)
        else:
            return self.controle_prems_couleur()

    #controle premiere couleur jouee
    def controle_prems_couleur(self):
        couleur_pli = [card for card in self.pli if card.couleur == self.pli[0].couleur]
        couleur_max = max(couleur_pli, key=lambda x: self.POINTS_SANS_ATOUT[x.valeur])
        if [self.POINTS_SANS_ATOUT[card.valeur] for card in couleur_pli].count(self.POINTS_SANS_ATOUT[couleur_max.valeur]) > 1:
            couleur_max = max(couleur_pli, key=lambda x: x.valeur)
        return self.pli.index(couleur_max)

#lancement du Jeu
game = Game([Player('Tristan'), Player('Alexis'), Player('Baptiste'), Player('Tiffany')])

#Affichage des initialisation
print(game.cards)
print(f"Le jeu comporte {len(game.cards)} cartes.")
print(f"Les joueurs en jeu sont {', '.join([game.players[i].name for i in range(4)])}.")
print(f"L'atout est {game.trump}.")
print(f"Le score actuel est de: {game.score[0]} pour Nous et {game.score[1]} pour Eux.")
print(f"Celui qui commence est {game.players[game.position].name}.")
print(f"Le dealer est {game.dealer}.")

game.distri_deck(True)
game.set_dealer(game.players[1])
game.set_trump('Carreau')
game.distri_carte_atout()
game.distri_deck_sec()

game.pli = [Card(7,'Coeur'),Card(8,'Coeur'),Card(14,'Trefle'),Card(10,'Pique')]
print(f"Le gagnant du pli est {game.players[game.win_pli()].name}.")

game.pli = [Card(7,'Coeur'),Card(8,'Coeur'),Card(14,'Trefle'),Card(10,'Carreau')]
print(f"Le gagnant du pli est {game.players[game.win_pli()].name}.")

game.pli = [Card(7,'Coeur'),Card(8,'Coeur'),Card(7,'Carreau'),Card(8,'Carreau')]
print(f"Le gagnant du pli est {game.players[game.win_pli()].name}.")

for i in range(4):
    print(f"La taille du jeu de {game.players[i].name} est {len(game.players[i].hand)}.")
