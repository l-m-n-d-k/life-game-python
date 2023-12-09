import pygame
import sys
import copy

class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = 10
        self.top = 10
        self.cell_size = 30
        self.color = pygame.Color(255, 255, 255)
        self.cell_x = self.cell_y = None

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                coords = (x * self.cell_size + self.left, y * self.cell_size + self.top,
                          self.cell_size, self.cell_size)
                pygame.draw.rect(screen, self.color, coords, 1)

    def get_click(self, pos):
        self.cell_x = (pos[0] - self.left) // self.cell_size
        self.cell_y = (pos[1] - self.top) // self.cell_size
        if (pos[0] < self.left or
                pos[1] < self.top or
                pos[0] > self.left + self.cell_size * self.width or
                pos[1] > self.top + self.cell_size * self.height):
            self.cell_x = self.cell_y = None

class Life(Board):
    def __init__(self, width, height):
        super().__init__(width, height)

    def get_click(self, pos):
        super().get_click(pos)
        if self.cell_x is None:
            return
        self.board[self.cell_y][self.cell_x] = 1 - self.board[self.cell_y][self.cell_x]

    def render(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                coords = (x * self.cell_size + self.left, y * self.cell_size + self.top,
                          self.cell_size, self.cell_size)
                if self.board[y][x] == 1:
                    pygame.draw.rect(screen, (0, 255, 0), coords)
                pygame.draw.rect(screen, self.color, coords, 1)

    def next_move(self):
        new_board = copy.deepcopy(self.board)
        for y in range(self.height):
            for x in range(self.width):
                s = 0
                for dy in range(-1, 2):
                    for dx in range(-1, 2):
                        if y + dy < 0 or x + dx < 0:
                            continue
                        if y + dy >= self.height or x + dx >= self.width:
                            continue
                        if dx == 0 and dy == 0:
                            continue
                        s += self.board[y + dy][x + dx]
                if self.board[y][x] == 0:
                    if s == 3:
                        new_board[y][x] = 1
                    else:
                        new_board[y][x] = 0
                else:
                    if not (s == 3 or s == 2):
                        new_board[y][x] = 0
                    else:
                        new_board[y][x] = 1
        self.board = new_board

def main():
    pygame.init()
    pygame.display.set_caption("Жизнь")
    size = width, height = 470, 470
    screen = pygame.display.set_mode(size)

    running = True
    fps = 60
    v = 10
    ticks = 0
    start = False
    clock = pygame.time.Clock()
    life = Life(30, 30)
    life.set_view(10, 10, 15)
    while running:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                life.get_click(event.pos)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                start = not start
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
                v -= 1
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
                v += 1
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                start = not start
        life.render(screen)
        if start:
            ticks += 1
        if ticks >= v:
            life.next_move()
            ticks = 0
        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()

if __name__ == '__main__':
    sys.exit(main())
