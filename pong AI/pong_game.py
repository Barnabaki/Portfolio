import pygame as pg

pg.init()
clock = pg.time.Clock()

DIS_WIDTH = 1000
DIS_HEIGHT = 800
DIS = pg.display.set_mode((DIS_WIDTH, DIS_HEIGHT))

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

X = 20
Y = 400
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
        self.velocity = 5
        self.board = board

    def draw(self):
        pg.draw.circle(DIS, WHITE, (self.X, self.Y), 15)

    def move(self):
        if self.X <= self.board.X + 35 and self.board.Y <= 400 <= self.board.Y + 100:
            self.velocity *= -1
        elif self.X >= DIS_WIDTH - 20:
            self.velocity = -3

        self.X += self.velocity

def main():
    board = Boards()
    ball = Ball(board)
    quit_game = False

    while not quit_game:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                quit_game = True

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    board.speed = -speed
                elif event.key == pg.K_DOWN:
                    board.speed = speed
            elif event.type == pg.KEYUP:
                if event.key == pg.K_UP or event.key == pg.K_DOWN:
                    board.speed = 0

        board.Y += board.speed

        if board.Y < 0:
            board.Y = 0
        elif board.Y > DIS_HEIGHT - 100:
            board.Y = DIS_HEIGHT - 100

        ball.move()

        DIS.fill(BLACK)
        board.draw()
        ball.draw()
        pg.display.update()
        clock.tick(60)

    pg.quit()

if __name__ == '__main__':
    main()
