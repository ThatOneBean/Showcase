from sense_hat import SenseHat
from random import randint
from time import sleep

sense = SenseHat()
pipe_color = (0,255,0) 
bg_color = (0,0,0)        
birb_color = (200,200,0) 
lives = 3 
game_over = False
x = 0
y = 0

matrix = [[bg_color for column in range(8)] for row in range(8)]


def flatten(matrix):
    flattened = [pixel for row in matrix for pixel in row]
    return flattened


def gen_pipes(matrix):
    for row in matrix:
        row[-1] = pipe_color
    gap = randint(1, 6)
    matrix[gap][-1] = bg_color
    matrix[gap - 1][-1] = bg_color
    matrix[gap + 1][-1] = bg_color
    return matrix


def move_pipes(matrix):
    for row in matrix:
        for i in range(7):
            row[i] = row[i + 1]
        row[-1] = bg_color
    return matrix


def draw_birb(event):
    global y
    global x
    global game_over
    sense.set_pixel(x, y, bg_color)
    if event.action == "pressed":
        if event.direction == "up" and y > 0:
            y -= 1
        elif event.direction == "down" and y < 7:
            y += 1
        elif event.direction == "right" and x < 7:
            x += 1
        elif event.direction == "left" and x > 0:
            x -= 1
    sense.set_pixel(x, y, birb_color)
    if matrix[y][x] == pipe_color:
    
      if lives > 2:
        draw_lives = 3
      else:
        draw_lives = lives
    
      for i in range(draw_lives):
        sense.set_pixel(0,i, (200,200,200))
  
      game_over = lives < 0
    
def check_collision(matrix):
    if matrix[y][x] == pipe_color:
        return True
    else:
        return False


sense.stick.direction_any = draw_birb

while not game_over:
    matrix = gen_pipes(matrix)
    if check_collision(matrix):
        game_over = True
    for i in range(3):
        matrix = move_pipes(matrix)
        sense.set_pixels(flatten(matrix))
        sense.set_pixel(x, y, birb_color)
        if check_collision(matrix):
            game_over = True
        sleep(1)

sense.show_message('Game Over')