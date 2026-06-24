import pygame
import random

class SnakeGameAI:
    def __init__(self):
        pygame.init()
        # Screen dimensions divisible by 20 (block size)
        self.w = 1000
        self.h = 500
        self.screen = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption("ANDOSH AI Snake")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 30)
        self.font1 = pygame.font.Font(None, 70)
        
        # Grid alignment configuration
        self.speed = 20  
        self.ai_mode = True
        self.reward = 0
        
        self.reset()

    def reset(self):
        self.x = self.w // 2
        self.y = self.h // 2
        self.dx = self.speed
        self.dy = 0
        self.score = 0
        self.reward = 0 
        
        # Generate initial food aligned to the 20x20 grid
        self.aplle_x = random.randint(0, (self.w - 20) // 20) * 20
        self.aplle_y = random.randint(0, (self.h - 20) // 20) * 20
        
        self.snake_body = [[self.x, self.y]]
        self.frame_iteration = 0 

    def play_step(self, action=None):
        self.frame_iteration += 1
        
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                   self.ai_mode = not self.ai_mode
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        keys = pygame.key.get_pressed()
        if self.ai_mode:
            if self.dx == self.speed and self.dy == 0:
                current_direction = 0 # Right
            elif self.dy == self.speed and self.dx == 0:
                current_direction = 1 # Down
            elif self.dx == -self.speed and self.dy == 0:
                current_direction = 2 # Left
            elif self.dy == -self.speed and self.dx == 0:
                current_direction = 3 # Up
                
            new_direction = current_direction
            
            if action == [1, 0, 0]:
                new_direction = current_direction
            elif action == [0, 1, 0]:
                new_direction = (current_direction + 1) % 4 # Turn Right
            elif action == [0, 0, 1]:
                new_direction = (current_direction - 1) % 4 # Turn Left
                
            if new_direction == 0:
                self.dx = self.speed; self.dy = 0  
            elif new_direction == 1:
                self.dx = 0; self.dy = self.speed  
            elif new_direction == 2:
                self.dx = -self.speed; self.dy = 0  
            elif new_direction == 3:
                self.dx = 0; self.dy = -self.speed  
        else:
            if keys[pygame.K_w] and self.dy == 0:
                self.dx = 0; self.dy = -self.speed
            if keys[pygame.K_s] and self.dy == 0:
                self.dx = 0; self.dy = +self.speed
            if keys[pygame.K_d] and self.dx == 0:
                self.dx = +self.speed; self.dy = 0 
            if keys[pygame.K_a] and self.dx == 0:
                self.dx = -self.speed; self.dy = 0  

        # Update snake head position
        self.x += self.dx
        self.y += self.dy
        self.snake_body.insert(0, [self.x, self.y])
        
        game_over = False
        self.reward = 0 
        
        # Collision detection (Walls or Self-eating)
        if (self.x >= self.w or self.x < 0 or self.y < 0 or self.y >= self.h) or (self.snake_body[0] in self.snake_body[1:]):
            game_over = True
            self.reward = -100  
            return game_over, self.score, self.reward
            
        # Food consumption and score update
        if abs(self.x - self.aplle_x) < 20 and abs(self.y - self.aplle_y) < 20:
            self.aplle_x = random.randint(1, 977)
            self.aplle_y = random.randint(1, 480)
            self.score += 1
            self.reward = 10
            self.frame_iteration = 0
        else:
            if not game_over:
                self.snake_body.pop() 
                
        # Check if the agent is stuck in an infinite loop
        if self.frame_iteration > len(self.snake_body) * 1000:
            game_over = True
            self.reward = -100
            return game_over, self.score, self.reward
            
        # Drawing elements on screen
        self.screen.fill((0, 0, 0)) 
        
        for block in self.snake_body:
            pygame.draw.rect(self.screen, (0, 255, 0), (block[0], block[1], 18, 18)) 
            
        pygame.draw.rect(self.screen, (255, 0, 0), (self.aplle_x, self.aplle_y, 18, 18))
        
        score_image = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_image, (1, 1))
        
        if game_over:
            text_image = self.font1.render("GAME OVER", True, (255, 0, 0)) 
            self.screen.blit(text_image, (380, 250)) 
            
        pygame.display.update()
        self.clock.tick(60) 
        
        return game_over, self.score, self.reward
           
