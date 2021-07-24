import pygame
import sys
import random

pygame.init()

WIDTH = 800
HEIGHT = 600

RED = (255,0,0)
BLUE = (0,0,255)
YELLOW =(255,255,0)
BACKGROUND_COLOUR = (0,0,0)

player_size = 50
player_pos = [WIDTH/2,HEIGHT - 2*player_size]
enemy_size = 50
enemy_pos = [random.randint(0,WIDTH-enemy_size),0]
enemy_list = [enemy_pos]

SPEED = 10

score = 0
level = 1
score_count = 20

score_font = pygame.font.SysFont("monospace", 30)
#creating a screen
screen = pygame.display.set_mode((WIDTH,HEIGHT))

def game_level(SPEED,score,score_count,level):
    if(score > score_count):
        SPEED += 5
        score_count += 20
        level += 1
    
    return level

def create_enemies(enemy_list):
    delay = random.random()
    if(len(enemy_list) < 10) and(delay < 0.1):
        x_pos = random.randint(0, WIDTH-enemy_size)
        y_pos = 0
        #print(1)
        enemy_list.append([x_pos,y_pos])

def draw_enemies(enemy_list):
    for enemy_position in enemy_list:
        pygame.draw.rect(screen, BLUE,(enemy_position[0],enemy_position[1],enemy_size,enemy_size))
        #print(2)

#MANIPULATING ENEMY POSITON 
def drop_enemies(enemy_list,score):
    for indx,enemy_pos in enumerate(enemy_list):           
        if(enemy_pos[1] >= 0 and enemy_pos[1] < HEIGHT-enemy_size):
            enemy_pos[1] += 20
        else:
            enemy_list.pop(indx)
            score = score + 1
    return score

def detect_collision(player_pos, enemy_pos):
    p_x = player_pos[0]
    p_y = player_pos[1]

    e_x = enemy_pos[0]
    e_y = enemy_pos[1]

    if(e_x >= p_x and e_x < (p_x+player_size)) or (p_x >= e_x and p_x < (e_x+enemy_size)):
        if(e_y >= p_y and e_y < (p_y+player_size)) or (p_y >= e_y and p_y < (e_y+enemy_size)):
            return True
    return False

def collision_check(enemy_list, player_pos):
    for enemy_pos in enemy_list:
        if(detect_collision(enemy_pos,player_pos)):
            return True
    return False
#DEVELOPE A GAME LOOP
#FOR LOOP INSIDE WHILE TO TRACK GAMING ACTIVITIES OR EVENTS

game_over = False

#DEFINING A FRAME RATE TO STOP BLOCK GO CRAZY
clock = pygame.time.Clock()
while not game_over :

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            x = player_pos[0]
            y = player_pos[1]
            if event.key == pygame.K_b or event.key == pygame.K_LEFT:
                x -= player_size
            elif event.key == pygame.K_m or event.key == pygame.K_RIGHT:
                x += player_size
            player_pos = [x,y]

    screen.fill(BACKGROUND_COLOUR)
        # if(detect_collision(player_pos,enemy_pos)):
        #     game_over = True
        #     break

    #checking for collisions
    if(collision_check(enemy_list, player_pos)):
        game_over = True
        break

    create_enemies(enemy_list)
    draw_enemies(enemy_list)

    #displaying score board
    score = drop_enemies(enemy_list,score)  
    text = "Blocks Dodged: "+str(score)
    label = score_font.render(text, 1, YELLOW)
    screen.blit(label,((WIDTH-320),HEIGHT-40))

    #displaying level
    level = game_level(SPEED,score,score_count,level)
    text1 = "Level:" +str(level)
    label = score_font.render(text1,1,YELLOW)
    screen.blit(label,(20,HEIGHT-40))

    pygame.draw.rect(screen, RED, (player_pos[0],player_pos[1],player_size,player_size))
   
    clock.tick(SPEED)
    
    pygame.display.update()