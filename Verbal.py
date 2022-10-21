import time
import random
import pygame as pg
englishwords = set()
with open("wordlist.txt", 'r') as f:
    lines = f.readlines()
    for line in lines:
        englishwords.add(line[:-1])

pg.init()

SCREENSIZE = 700
BUTTONSIZE = 100

SHOWNBUTTON = (140, 140, 220)
SHOWNBUTTONCLICKED = (170, 170, 255)
NOTSHOWNBUTTON = (220, 140, 140)
NOTSHOWNBUTTONCLICKED = (255, 170, 170)
EMPTY = (170, 170, 170)
BACKGROUND = (255, 255, 255)

FONT = pg.font.SysFont("timesnewroman.ttf", 72)
TEXT = (20, 20, 20)

class Game:
    def __init__(self, screensize = 700, buttonsize = 100):
        self.screen = pg.display.set_mode((screensize, screensize))
        self.screensize = screensize
        self.buttonsize = buttonsize
        self.score = 0
        self.state = "End" #End, Play
        self.words = set()
        self.shownwords = set()
        self.currentword = None #Word to check, string
        self.clicked = None #"shown", "notshown", None
    
    def initialize_wordset(self):
        self.words = englishwords

    def random_word(self):
        if self.currentword:
            self.shownwords.add(self.currentword)
        # 0.7 chance of a new word from self.words, 0.3 chance of a word from self.shownwords
        if random.random() < 0.7 or len(self.shownwords) < 4:
            self.currentword = random.choice(list(self.words))
        elif len(self.shownwords) > 3:
            self.currentword = random.choice(list(self.shownwords))
    
    def check(self): #True or False
        if self.currentword in self.shownwords:
            return self.clicked == "shown"
        else:
            return self.clicked == "notshown"

    def mousepostobox(self, pos):
        x, y = pos
        if not (x > self.screensize or x < 0 or y < 0 or y > self.screensize) and y >= self.screensize - self.buttonsize and y < self.screensize:
            if x < self.screensize / 2:
                self.clicked = "shown"
            else:
                self.clicked = "notshown"
        else:
            self.clicked = None

    def update(self):
        self.screen.fill(EMPTY)
        currentword_text = FONT.render(f"{self.currentword}", True, TEXT)
        currentword_rect = currentword_text.get_rect(center=(self.screensize//2, self.screensize/2 - currentword_text.get_height()))
        self.screen.blit(currentword_text, currentword_rect)


        pg.draw.rect(self.screen, SHOWNBUTTON, (0, self.screensize - self.buttonsize, self.screensize/2, self.buttonsize))
        pg.draw.rect(self.screen, NOTSHOWNBUTTON, (self.screensize/2, self.screensize - self.buttonsize, self.screensize/2, self.buttonsize))

        if self.clicked == "shown":
            pg.draw.rect(self.screen, SHOWNBUTTONCLICKED, (0, self.screensize - self.buttonsize, self.screensize/2, self.buttonsize))
        elif self.clicked == "notshown":
            pg.draw.rect(self.screen, NOTSHOWNBUTTONCLICKED, (self.screensize/2, self.screensize - self.buttonsize, self.screensize/2, self.buttonsize))
        
        shownbutton_text = FONT.render("Seen", True, TEXT)
        shownbutton_rect = shownbutton_text.get_rect(center=(self.screensize//4, self.screensize - self.buttonsize//2))
        self.screen.blit(shownbutton_text, shownbutton_rect)

        notshownbutton_text = FONT.render("New", True, TEXT)
        notshownbutton_rect = notshownbutton_text.get_rect(center=(3*self.screensize//4, self.screensize - self.buttonsize//2))
        self.screen.blit(notshownbutton_text, notshownbutton_rect)

        pg.display.update()


    def play(self):
        self.shownwords = set()
        while self.state == "Play":
            self.random_word()
            self.update()
            self.clicked = None
            self.update()
            while not self.clicked:
                for event in pg.event.get():
                    if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                        pg.quit()
                    elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                        self.mousepostobox(event.pos)
                        if self.clicked:
                            self.update()
                            if self.check():
                                self.score += 1
                                time.sleep(0.1)
                            else:
                                self.state = "End"
                                time.sleep(0.2)

    def menu(self):
        self.screen.fill(BACKGROUND)
        pressspace = FONT.render("Press space to play", True, TEXT)
        if self.score > 1:
            scorecount = FONT.render(f'Score: {self.score}', True, TEXT)
            self.screen.blit(scorecount, (10, 10))
        self.screen.blit(pressspace, (10, 10 + pressspace.get_height()))
        pg.display.update()
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
            elif event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                self.state = "Play"

    def run(self):
        self.initialize_wordset()
        while True:
            if self.state == "Play":
                self.score = 0
                self.play()
            elif self.state == "End":
                self.menu()

def main():
    game = Game(SCREENSIZE, BUTTONSIZE)
    game.run()

if __name__ == "__main__":
    main()


