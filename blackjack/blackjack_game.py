#blackjack
import pygame, sys, random
from gui import Button
pygame.init()

class Card:
    SUITS = ['hearts', 'diamonds', 'clubs', 'spades']
    RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace']

    def __init__(self, rank, suit):
        if rank not in Card.RANKS:
            raise ValueError(f"Invalid rank: {rank}")
        if suit not in Card.SUITS:
            raise ValueError(f"Invalid suit: {suit}")
        self.rank = rank
        self.suit = suit

    @property
    def value(self):
        if self.rank in ['jack', 'queen', 'king']:
            return 10
        elif self.rank == 'ace': #favor the higher value
            return 11 
        else:
            return int(self.rank)
        
    def __str__(self):
        return f"{self.rank} of {self.suit}"

class Deck:
    def __init__(self):
        self.cards = [Card(rank, suit) for suit in Card.SUITS for rank in Card.RANKS]

    def shuffle_deck(self):
        random.shuffle(self.cards)

class Player:
    def __init__(self):
        self.hand = []

    def get_score(self):
        score = 0
        aces = 0
        for card in self.hand:
            val = card.value
            if val == 11:
                aces += 1
            score += val
        soft = aces > 0
        while score > 21 and aces:
            score -= 10
            aces -= 1
        if aces == 0:
            soft = False
        return score, soft

    def bust(self):
        score, _ = self.get_score()
        return score > 21

class Shoe:
    def __init__(self, decks):
        self.decks = decks
        self.shoe = []
        self.new_shoe()

    def shuffle_shoe(self):
        random.shuffle(self.cards)

    def new_shoe(self):
        self.cards = []
        for _ in range(self.decks):
            singleD = Deck()
            singleD.shuffle_deck()
            self.cards.extend(singleD.cards)
        self.shuffle_shoe()
    
    def insert_cut_card(self):
        cut_position = random.randint(15, len(self.cards) - 15)
        self.cards.insert(cut_position, 'cut')

    def draw_card(self):
        card = self.cards.pop()
        if card == "cut":
            self.new_shoe()
            card = self.cards.pop()
            return card
        else:
            return card


class Blackjack:
    def __init__(self):
        self.shoe = Shoe(1)
        self.player = Player()
        self.dealer = Player()

    def play(self):
        #deal hands
        for i in range(2):
            self.player.hand.append(self.shoe.draw_card())
            self.dealer.hand.append(self.shoe.draw_card())

        #initail hands
        print("\nDealer's visible card:")
        print(f"  {self.dealer.hand[0]}")

        print("\nPlayer's cards:")
        for card in self.player.hand:
            print(f"  {card}")
        pscore, psoft = self.player.get_score()
        print(f"Player score: {pscore} {'(soft)' if psoft else ''}")

        #player action
        while True:
            pscore, psoft = self.player.get_score()
            if pscore > 21:
                break
            print("\nMake a choice (hit, stand, double): ")
            choice = input().strip().lower()
            if choice == 'hit':
                new_card = self.shoe.draw_card()
                self.player.hand.append(new_card)
                print(f"  Drew: {new_card}")
                pscore, psoft = self.player.get_score()
                print(f"New score: {pscore} {'(soft)' if psoft else ''}")
            elif choice == 'stand':
                break
            elif choice == 'double':
                new_card = self.shoe.draw_card()
                self.player.hand.append(new_card)
                print(f"  Drew: {new_card}")
                pscore, psoft = self.player.get_score()
                print(f"New score: {pscore} {'(soft)' if psoft else ''}")
                break
            else:
                print("Invalid choice. Please type 'hit', 'stand', or 'double'.")

        #dealer actions
        while True:
            dscore, dsoft = self.dealer.get_score()
            if dscore < 17 or (dscore == 17 and dsoft):
                self.dealer.hand.append(self.shoe.draw_card())
            else:
                break

        print("\nDealer's cards:")
        for card in self.dealer.hand:
            print(f"  {card}")
        dscore, dsoft = self.dealer.get_score()
        print(f"Dealer score: {dscore} {'(soft)' if dsoft else ''}")

        #showdown
        dscore, _ = self.dealer.get_score()
        pscore, _ = self.player.get_score()

        if not self.dealer.bust() and self.player.bust():
            print("Player loses.")
        elif self.dealer.bust() and not self.player.bust():
            print("Player wins!")
        elif dscore > pscore:
            print("Player loses.")
        elif dscore < pscore:
            print("Player wins!")
        else:
            print("Push.")

        #cleanup
        self.player.hand = []
        self.dealer.hand = []


def start_screen(screen):
    start_button = Button('PLAY',200,40,(200,250),4,screen,pygame.font.Font(None,30))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        start_button.update(pygame.event.get())
        start_button.draw()

        if start_button.clicked:
            game(screen)
        pygame.display.update()
    pygame.quit()

def game(screen):
    hit_button = Button('HIT',200,40,(100,250),4,screen,pygame.font.Font(None,30))
    stand_button = Button('STAND',200,40,(200,250),4,screen,pygame.font.Font(None,30))
    double_button = Button('DOUBLE',200,40,(300,250),4,screen,pygame.font.Font(None,30))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        hit_button.update(pygame.event.get())
        hit_button.draw()
        stand_button.update(pygame.event.get())
        stand_button.draw()
        double_button.update(pygame.event.get())
        double_button.draw()

        if hit_button.clicked:
            pass
        elif stand_button.clicked:
            pass
        elif double_button.clicked:
            pass
        pygame.display.update()
    pygame.quit()

def main():
    game = Blackjack()
    while True:
        game.play()
        again = input("\nPlay again? (y/n): ").strip().lower()
        if again != 'y':
            break

    screen = pygame.display.set_mode((600,600))
    pygame.display.set_caption('BLACKJACK')
    gui_font = pygame.font.Font(None,30)
    #card = pygame.image.load(f'cards/fronts/png_96_dpi/{card.suit}_{card.rank}.png')
    
    play_button = Button('Play!',200,40,(200,250),4,screen,gui_font)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill('#35654D')
        play_button.draw()
        pygame.display.update()
    pygame.quit()

main()