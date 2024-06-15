from pygame import *
from random import randint
from time import time as timer

img_background = "galaxy.jpg"
img_player = "rocket.png"
img_ufo = "ufo.png"
img_asteroid = "asteroid.png"
img_bullet = "bullet.png"

win_height = 700
win_width = 700

lost = 0
goals = [6, 12, 18, 24]
health = 3

window = display.set_mode((win_height, win_width))
display.set_caption("Space Shooter")
background = transform.scale(image.load(img_background), (win_height, win_width))


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed

        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed 
        if keys[K_d] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self): 
        global total_bullets
        bullet =Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, 15)
        bullets.add(bullet)
        total_bullets += 1

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()
        
# create the player
player = Player(img_player, 5, win_height - 100, 80, 100, 10)

# creating the enemies
ufos = sprite.Group()
def create_ufos():
    for i in range(3):
        ufo = Enemy(img_ufo, randint(80, win_width - 80), -40, 80, 50, randint(1,7))
        ufos.add(ufo)

asteroids = sprite.Group()
def create_asteroids():
    for i in range(3):
        asteroid = Enemy(img_asteroid, randint(80, win_width - 80), -40, 80, 50, randint(1,7))
        asteroids.add(asteroid)

bullets = sprite.Group()

font.init()
font1 = font.Font(None, 80)
win = font1.render("YOU WIN!", True, (255, 255, 255))
lose = font1.render("YOU LOSE!", True, (255, 255, 255))
pause = font1.render("pause", True, (255, 255, 255))


font2 = font.Font(None, 36)

font3 = font.Font(None, 50)

finish = False
real_time = False
num_fire = 0
run = True
FPS = 60
clock = time.Clock()
score = 0
level = 0
current_point = 0
game_status = None
bullet_hit = 0
total_bullets = 0
start_time = timer()
current_bullet = 0
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
            
        elif e.type == KEYDOWN:
            if e.key == K_SPACE and num_fire < goals[level] + 1:
                player.fire()
                num_fire += 1
            if e.key == K_r and finish ==True:
                finish = False
                real_time = False
                num_fire = 0
                run = True
                FPS = 60
                clock = time.Clock()
                score = 0
                level = 0
                current_point = 0
                game_status = None
                bullet_hit = 0
                total_bullets = 0
                start_time = timer()
                current_bullet = 0
            if e.key == K_x and finish ==True:
                run = False
            if e.key == K_p:
                if game_status == None:
                    game_status = "pause"
                    finish = True
                elif game_status == "pause":
                    game_status = None
                    finish = False
    if not finish:
        window.blit(background, (0,0))
        player.update()
        ufos.update()
        asteroids.update()
        bullets.update()

        player.reset()
        ufos.draw(window)
        asteroids.draw(window)
        bullets.draw(window)
        
        
        if (len(ufos) == 0 and len(asteroids) == 0) and current_point <= goals[level]:
            create_ufos()
            create_asteroids()
            
            
        if sprite.groupcollide(ufos, bullets, True, True):
            score += 1
            current_point += 1 
            bullet_hit += 1
            current_bullet = (goals[level] + 1) - num_fire
            

        if sprite.groupcollide(asteroids, bullets, True, True):
            score += 1
            current_point += 1  
            bullet_hit += 1  
            current_bullet = (goals[level] + 1) - num_fire
            

        if (current_point == goals[level] and num_fire <= goals[level] + 2) and (len(ufos) == 0 and len(asteroids) == 0):
            num_fire = 0
            if level < 3:
                level += 1
                current_point = 0
                current_bullet = 0
        
            
                


       
        if (len(ufos) == 0 and len(asteroids) == 0) and (level == 3 and current_point == goals[level]):
            finish = True
            # window.blit(win, (200, 200))
            game_status = 'win'
            stop_time = timer()

        if num_fire == goals[level] + 1 and (len(ufos) != 0 or len(asteroids) != 0) and len(bullets) == 0:
            finish = True
            # window.blit(lose, (200, 200))
            game_status = 'lose'
            stop_time = timer()


        text = font2.render("Score: " + str(score), 1, (255, 255, 255)) 
        window.blit(text, (10, 20))

        text_bullets = font2.render("Bullets: " + str((goals[level] + 1) - num_fire), 1, (255, 255, 255))
        window.blit(text_bullets, (10, 50))
        
        text_level = font2.render("Level: " + str(level + 1), 1, (255, 255, 255))
        window.blit(text_level, (10, 80))

    else:
        window.blit(background, (0,0))
        if game_status == "win":
            window.blit(win, (200, 200))

        elif game_status == "lose":
            window.blit(lose, (200, 200))

        elif game_status == "pause":
            window.blit(pause,((200, 200)))
        
        
        try:
            text_time = font2.render("Time Finish: " + str(round(stop_time - start_time, 0)) + " seconds", 1, (255, 255, 255))
            window.blit(text_time, (220, 270))
            text_accuracy = font2.render("Accuracy: " + str(round((bullet_hit/total_bullets) * 100, 2)) + " %", 1, (255, 255, 255))
            window.blit(text_accuracy, (220, 300))

            text_point = font2.render("Score: " + str(score), 1, (255, 255, 255))
            window.blit(text_point, (220, 330))

            text_passed = font2.render("Enemies Passed: " + str(lost), 1, (255, 255, 255))
            window.blit(text_passed, (220, 360))
        except:
            pass
        

        restart_text = font3.render("press r to restart the game" , True, (255, 255, 255))
        window.blit(restart_text, (130, 500))

        restart_text = font3.render("press x to exit the game" , True, (255, 255, 255))
        window.blit(restart_text, (150, 550))

    display.update()
    clock.tick(FPS)
