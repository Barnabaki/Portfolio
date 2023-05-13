import pygame as pg
from pygame import mixer
import math

pg.init()
mixer.init()

score_sound = pg.mixer.Sound("board_hit2.wav")
hit_sound = pg.mixer.Sound("hit_sound.wav")
damage_sound = pg.mixer.Sound("damage.mp3")
game_over_sound = pg.mixer.Sound("game_over.mp3")
main_music = pg.mixer.Sound("main_music.mp3")

mixer.music.set_volume(0.7)

clock = pg.time.Clock()

DIS_WIDTH = 1000
DIS_HEIGHT = 800
DIS = pg.display.set_mode((DIS_WIDTH, DIS_HEIGHT))

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

X = 20
Y = 400
counter = 0
acceleration = 1
speed = 10





class Boards:

    def __init__(self):
        self.X = 20
        self.Y = 400
        self.speed = 0
        

    def draw(self):
        board_thic = 20
        board_len = 100
        pg.draw.rect(DIS, WHITE, (self.X, int(self.Y), board_thic, board_len), border_radius=5)

class Ball:
    def __init__(self, board):
        self.X = 500
        self.Y = 400
        self.velocity = [5,5]
        self.board = board

    def draw(self):
        pg.draw.circle(DIS, WHITE, (self.X, self.Y), 15)


    def move(self, circle_draw, board_draw):
        global counter, acceleration
        board_rect = pg.Rect(self.board.X, self.board.Y, 20, 100)
        ball_rect = pg.Rect(self.X - 15, self.Y - 15, 30, 30)

        if ball_rect.colliderect(board_rect):
            self.velocity[0] *= -1
            counter += 1
            acceleration += 1
            pg.mixer.Channel(1).play(pg.mixer.Sound('hit_sound.wav'))
            pg.mixer.Channel(2).play(pg.mixer.Sound(score_sound))

        # Check if the object touches the border
        if self.X <= 20:
            self.velocity[0] *= -1
            pg.mixer.Sound.play(damage_sound)
            counter -= 1
            if counter < 0:
                pg.mixer.Channel(0).play(game_over_sound, 1)

        if self.X >= DIS_WIDTH - 20:
        # Change direction in x-axis
            self.velocity[0] *= -1
            pg.mixer.Channel(1).play(pg.mixer.Sound('hit_sound.wav'))
        # Change direction in y-axis by 45 degrees
            self.velocity[1] = math.copysign(self.velocity[0], self.velocity[1])

        if self.Y <= 0 or self.Y >= DIS_HEIGHT - 20:
        # Change direction in y-axis
            self.velocity[1] *= -1
            pg.mixer.Channel(1).play(pg.mixer.Sound('hit_sound.wav'))
        # Change direction in x-axis by 45 degrees
            self.velocity[0] = math.copysign(self.velocity[1], self.velocity[0])

        self.X += self.velocity[0] * acceleration
        self.Y += self.velocity[1] * acceleration

        if counter < 0:
            self.velocity = [0,0]



def main():
    board = Boards()
    ball = Ball(board)

    quit_game = False
    game_over = False

    while not quit_game:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                quit_game = True
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_g:
                    game_over = True
                if event.key == pg.K_UP:
                    board.speed = -speed
                elif event.key == pg.K_DOWN:
                    board.speed = speed
            elif event.type == pg.KEYUP:
                if event.key == pg.K_UP or event.key == pg.K_DOWN:
                    board.speed = 0

        board.Y += board.speed * acceleration

        if board.Y < 0:
            board.Y = 0
        elif board.Y > DIS_HEIGHT - 100:
            board.Y = DIS_HEIGHT - 100

        
        font = pg.font.SysFont("Verdana", 30)
        dis_score = font.render("Score: "+str(counter), True, WHITE)
        message = font.render("GAME OVER", True, WHITE)

        if counter < 0:
                game_over = True
                

        ball.move(Boards.draw, Ball.draw)

        
        if game_over == False:
            DIS.fill(BLACK)
            DIS.blit(dis_score,(10,10))

            board.draw()
            ball.draw()

        elif game_over == True:
            DIS.fill(BLACK)
            DIS.blit(dis_score,(10,10))
            DIS.blit(message, (370,DIS_HEIGHT/2))

            
                


        pg.display.update()
        clock.tick(60)

    pg.quit()

if __name__ == '__main__':
    main()
