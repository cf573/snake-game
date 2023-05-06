import pygame
import random
import pygame.mixer
import pygame_gui

pygame.mixer.init()
move_sound = pygame.mixer.Sound('ji.mp3')
eating_sound = pygame.mixer.Sound('jini.mp3')
yisound = pygame.mixer.Sound('yigeyou.wav')
pygame.font.init()
font = pygame.font.Font(None, 36)

#set window size and caption
window_size = (640,480)
caption = "Snake Game"
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption(caption)

#set gui manager
#gui_manager = pygame_gui.UIManager(window_size)

# Create a Pygame GUI button
'''start_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((200, 200), (100, 50)),
    text='Start',
    manager=gui_manager)'''

class Snake:
    def __init__(self):
        self.x = 400
        self.y = 300
        self.size = 10
        self.speed = 0.1
        self.length = 10
        self.direction = 'right'
        self.body = [(self.x,self.y)]
        
    def move(self):
        # Update Snake position based on direction
        if self.direction == "right":
            new_head = [self.body[0][0] + self.speed, self.body[0][1]]
        elif self.direction == "left":
            new_head = [self.body[0][0] - self.speed, self.body[0][1]]
        elif self.direction == "up":
            new_head = [self.body[0][0], self.body[0][1] - self.speed]
        elif self.direction == "down":
            new_head = [self.body[0][0], self.body[0][1] + self.speed]

        self.body.insert(0, new_head)
        
        
        # Remove tail if Snake is too long
        if len(self.body) > self.length:
            self.body.pop()
        
    def draw(self, surface):
        
        # Draw Snake body on surface
        
        for segment in self.body:
            
            pygame.draw.rect(surface, (255, 255, 0), (segment[0], segment[1], self.size, self.size))

class Food:
    def __init__(self):
        # Initialize food position and size
        self.x = random.randrange(40,window_size[0]-20, 10)
        self.y = random.randrange(40,window_size[1]-20, 10)
        self.size = 10
    
    def draw(self, surface):
        # Draw food on surface
        pygame.draw.rect(surface, (255, 0, 0), (self.x, self.y, self.size, self.size))

snake = Snake()
food = Food()
score = 0
# Game loop

game_over = False
while not game_over:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        '''if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == start_button:
                    # Start the game here
                    print("Starting game...")
        gui_manager.process_events(event)'''
        if event.type == pygame.KEYDOWN:
            volume = move_sound.get_volume() + 1
            move_sound.set_volume(volume)
            move_sound.play()
            
            if event.key == pygame.K_LEFT and snake.direction != "right":
                snake.direction = "left"
            elif event.key == pygame.K_RIGHT and snake.direction != "left":
                snake.direction = "right"
            elif event.key == pygame.K_UP and snake.direction != "down":
                snake.direction = "up"
            elif event.key == pygame.K_DOWN and snake.direction != "up":
                snake.direction = "down"
    # Move Snake and update screen
    snake.move()
    if snake.body[0][0] < 0 or snake.body[0][0] >= window_size[0]:
        game_over = True
    elif snake.body[0][1] < 0 or snake.body[0][1] >= window_size[1]:
        game_over = True
    elif snake.body[0] in snake.body[1:]:
        game_over = True
    elif snake.body[0][0] == food.x and snake.body[0][1] == food.y:
        
        food = Food()
        snake.length += 1
        
        
    screen.fill((0,0,0))
    
    snake.draw(screen)
    food.draw(screen)
    
    font = pygame.font.SysFont("simhei", 32)
    score_text = font.render(f"Score: {score}", True, (255, 0, 0))
    screen.blit(score_text, (10, 10))
    if score == 2:
        font = pygame.font.SysFont("simhei", 100)
        score_text = font.render("太tmd能吃辣", True, (255, 0, 255))
        screen.blit(score_text, (50,50))
        eating_sound.set_volume(0.1)
        eating_sound.play()
        
    elif score == 3:
        font = pygame.font.SysFont("simhei", 100)
        score_text = font.render("别tmd吃了", True, (0, 255, 255))
        screen.blit(score_text, (50, 50))
        yisound.play()
    elif score == 4:
        font = pygame.font.SysFont("simhei", 100)
        score_text = font.render("说了不听是吧", True, (255, 255, 0))
        screen.blit(score_text, (100, 100))
    
    
    pygame.display.update()
    if abs(snake.body[0][0] - food.x)<= 5 and abs(snake.body[0][1]- food.y)<=5:
        food = Food()
        snake.speed += 0.01 
        snake.length += 100
        score += 1
    
     
# Quit Pygame
pygame.quit()