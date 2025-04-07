import pygame, sys
pygame.init()

class Button:
    def __init__(self, text, width, height, pos, elevation, screen, gui_font):
        self.screen = screen
        self.gui_font = gui_font

        self.top_rect = pygame.Rect(pos, (width, height))
        self.top_color = '#FFFFFFFF'

        self.bottom_rect = pygame.Rect(pos, (width, elevation))
        self.bottom_color = '#dbd4d2'

        self.pressed = False
        self.clicked = False  # Flag for detecting single clicks

        self.elevation = elevation
        self.dynamic_elevation = elevation
        self.original_y_pos = pos[1]

        self.text_surf = gui_font.render(text, True, '#000000')
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)

    def draw(self):
        # Elevation effect
        self.top_rect.y = self.original_y_pos - self.dynamic_elevation
        self.text_rect.center = self.top_rect.center

        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elevation

        pygame.draw.rect(self.screen, self.bottom_color, self.bottom_rect, border_radius=12)
        pygame.draw.rect(self.screen, self.top_color, self.top_rect, border_radius=12)
        self.screen.blit(self.text_surf, self.text_rect)

    def update(self, events):
        mouse_pos = pygame.mouse.get_pos()
        self.clicked = False  

        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = '#D74B4B'
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.dynamic_elevation = 0
                    self.pressed = True
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.dynamic_elevation = self.elevation
                    if self.pressed:
                        self.clicked = True  
                        self.pressed = False
        else:
            self.dynamic_elevation = self.elevation
            self.top_color = '#FFFFFFFF'
            self.pressed = False


        

#class card_vis:
    #def __init__(self,rank,suit):

"""
def main():


    screen = pygame.display.set_mode((600,800))
    pygame.display.set_caption('BLACKJACK')
    gui_font = pygame.font.Font(None,30)
    card = pygame.image.load(f'cards/fronts/png_96_dpi/{card.suit}_{card.rank}.png')
    
    play_button = Button('Play!',200,40,(200,250),screen,gui_font)

    while True:
        screen.fill('#35654D')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break
        screen.fill('#35654D')
        play_button.draw()

        pygame.display.update()
    pygame.quit()

main()
"""
    





    

    



