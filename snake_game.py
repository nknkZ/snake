import pygame
import random
import time
import math
from pygame import mixer

# Initialize Pygame and mixer
pygame.init()
mixer.init()

# Colors
WHITE = (255, 255, 255)
RED = (255, 50, 50)
GREEN = (50, 255, 50)
BLUE = (50, 50, 255)
BACKGROUND = (230, 230, 250)  # Light lavender background
# Game settings
WINDOW_SIZE = 800
GRID_SIZE = 20
GRID_COUNT = WINDOW_SIZE // GRID_SIZE

# Create window
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Hungry Snake Adventure! 🐍")

class Snake:
    def __init__(self, window_size):
        self.window_size = window_size
        self.length = 1
        # Ensure snake starts aligned to grid
        start_x = (window_size // GRID_SIZE // 2) * GRID_SIZE
        start_y = (window_size // GRID_SIZE // 2) * GRID_SIZE
        self.positions = [(start_x, start_y)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = GREEN
        self.score = 0
        self.base_speed = 1.2
        self.speed = self.base_speed
        self.food_collected = {}

    def get_head_position(self):
        return self.positions[0]

    def update(self):
        cur = self.get_head_position()
        x, y = self.direction
        new_x = (cur[0] + (x*GRID_SIZE)) % self.window_size
        new_y = (cur[1] + (y*GRID_SIZE)) % self.window_size
        new = (new_x, new_y)
        
        if new in self.positions[3:]:
            return False
        
        self.positions.insert(0, new)
        if len(self.positions) > self.length:
            self.positions.pop()
        return True

    def update_window_size(self, new_size):
        ratio = new_size / self.window_size
        self.positions = [(int(x * ratio), int(y * ratio)) for x, y in self.positions]
        self.window_size = new_size

    def draw(self, surface):
        for i, p in enumerate(self.positions):
            pygame.draw.rect(surface, self.color, 
                           (p[0], p[1], GRID_SIZE-1, GRID_SIZE-1))
            # Draw eyes on the head
            if i == 0:  # Head of the snake
                # Left eye
                pygame.draw.circle(surface, BLUE, 
                                 (p[0] + 5, p[1] + 5), 2)
                # Right eye
                pygame.draw.circle(surface, BLUE, 
                                 (p[0] + 15, p[1] + 5), 2)

    def update_speed(self):
        # Increase speed with score
        self.speed = self.base_speed + (self.score // 20) * 0.5

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.food_types = [
            {'color': (255, 0, 0), 'type': 'apple', 'points': 1},
            {'color': (255, 0, 127), 'type': 'strawberry', 'points': 1},
            {'color': (222, 184, 135), 'type': 'chicken', 'points': 1},
            {'color': (255, 165, 0), 'type': 'orange', 'points': 1},
            {'color': (255, 255, 0), 'type': 'banana', 'points': 1},
            {'color': (128, 0, 128), 'type': 'grapes', 'points': 1},
            {'color': (210, 180, 140), 'type': 'cookie', 'points': 1},
            {'color': (255, 192, 203), 'type': 'ice_cream', 'points': 1},
            {'color': (70, 130, 180), 'type': 'fish', 'points': 1},
            {'color': (218, 165, 32), 'type': 'chips', 'points': 1}
        ]
        self.current_food = random.choice(self.food_types)
        self.randomize_position()

    def draw(self, surface):
        x, y = self.position
        if self.current_food['type'] == 'ice_cream':
            # Draw cone
            pygame.draw.polygon(surface, (210, 180, 140),  # Cone color
                              [(x + GRID_SIZE//2, y + GRID_SIZE),
                               (x + 2, y + GRID_SIZE//2),
                               (x + GRID_SIZE - 2, y + GRID_SIZE//2)])
            # Draw ice cream scoops
            pygame.draw.circle(surface, self.current_food['color'],
                             (x + GRID_SIZE//2, y + GRID_SIZE//3),
                             GRID_SIZE//3)
            # Add shine
            pygame.draw.circle(surface, (255, 255, 255),
                             (x + GRID_SIZE//2 - 2, y + GRID_SIZE//3 - 2), 2)

        elif self.current_food['type'] == 'fish':
            # Draw fish body (centered)
            pygame.draw.ellipse(surface, self.current_food['color'],
                              (x, y + GRID_SIZE//4, GRID_SIZE, GRID_SIZE//2))
            # Draw tail (adjusted position)
            pygame.draw.polygon(surface, self.current_food['color'],
                              [(x, y + GRID_SIZE//2),
                               (x - GRID_SIZE//4, y + GRID_SIZE//4),
                               (x - GRID_SIZE//4, y + GRID_SIZE*3//4)])
            # Draw eye
            pygame.draw.circle(surface, (0, 0, 0),
                             (x + GRID_SIZE*3//4, y + GRID_SIZE//2), 2)

        elif self.current_food['type'] == 'chips':
            # Draw multiple chips
            for i in range(3):
                pygame.draw.rect(surface, self.current_food['color'],
                               (x + i*4, y + i*2, GRID_SIZE//3, GRID_SIZE-4))
            # Add some "salt" dots
            for _ in range(4):
                salt_x = x + random.randint(0, GRID_SIZE-2)
                salt_y = y + random.randint(0, GRID_SIZE-2)
                pygame.draw.circle(surface, (255, 255, 255),
                                 (salt_x, salt_y), 1)
        if self.current_food['type'] == 'apple':
            # Draw apple body
            pygame.draw.circle(surface, self.current_food['color'],
                             (x + GRID_SIZE//2, y + GRID_SIZE//2), 
                             GRID_SIZE//2 - 1)
            # Draw stem
            pygame.draw.rect(surface, (101, 67, 33),
                           (x + GRID_SIZE//2 - 1, y + 2, 3, 5))
            # Draw leaves (two leaves for better appearance)
            pygame.draw.ellipse(surface, (34, 139, 34),
                              (x + GRID_SIZE//2 + 2, y + 3, 6, 4))
            pygame.draw.ellipse(surface, (34, 139, 34),
                              (x + GRID_SIZE//2 - 7, y + 4, 6, 4))
            # Add shine detail
            pygame.draw.circle(surface, (255, 255, 255),
                             (x + GRID_SIZE//2 - 3, y + GRID_SIZE//2 - 3), 2)
        
        elif self.current_food['type'] == 'strawberry':
            # Draw strawberry body
            pygame.draw.polygon(surface, self.current_food['color'],
                              [(x + GRID_SIZE//2, y + 2),
                               (x + GRID_SIZE - 2, y + GRID_SIZE - 2),
                               (x + 2, y + GRID_SIZE - 2)])
            # Draw seeds (more organized pattern)
            for i in range(4):
                for j in range(4):
                    pygame.draw.circle(surface, (255, 255, 200),
                                     (x + 6 + i*4, y + 8 + j*4), 1)
            # Draw leaves at top
            pygame.draw.polygon(surface, (34, 139, 34),
                              [(x + GRID_SIZE//2, y + 2),
                               (x + GRID_SIZE//2 + 5, y - 2),
                               (x + GRID_SIZE//2 - 5, y - 2)])
            
        elif self.current_food['type'] == 'chicken':
            # Draw drumstick
            pygame.draw.circle(surface, self.current_food['color'],
                             (x + GRID_SIZE//2, y + GRID_SIZE//2), 
                             GRID_SIZE//2 - 1)
            # Draw stick part
            pygame.draw.rect(surface, self.current_food['color'],
                           (x + GRID_SIZE//2, y + GRID_SIZE//2,
                            GRID_SIZE//2, GRID_SIZE//3))
            # Draw bone end
            pygame.draw.circle(surface, (255, 255, 255),
                             (x + GRID_SIZE - 3, y + GRID_SIZE - 3), 4)
            # Add "cooked" effect
            pygame.draw.arc(surface, (139, 69, 19),
                          (x + 5, y + 5, GRID_SIZE-10, GRID_SIZE-10),
                          0, 3.14, 2)

        elif self.current_food['type'] == 'orange':
            # Draw orange body
            pygame.draw.circle(surface, self.current_food['color'],
                             (x + GRID_SIZE//2, y + GRID_SIZE//2), 
                             GRID_SIZE//2 - 1)
            # Draw leaf
            pygame.draw.ellipse(surface, (34, 139, 34),
                              (x + GRID_SIZE//2 - 2, y + 2, 6, 4))
            # Add segments
            for angle in range(0, 360, 45):
                end_x = x + GRID_SIZE//2 + int(8 * math.cos(math.radians(angle)))
                end_y = y + GRID_SIZE//2 + int(8 * math.sin(math.radians(angle)))
                pygame.draw.line(surface, (255, 140, 0),
                               (x + GRID_SIZE//2, y + GRID_SIZE//2),
                               (end_x, end_y), 1)

        elif self.current_food['type'] == 'banana':
            # Draw banana shape
            pygame.draw.arc(surface, self.current_food['color'],
                          (x, y, GRID_SIZE, GRID_SIZE),
                          0, 3.14, 5)
            pygame.draw.arc(surface, (255, 215, 0),  # Slightly darker for depth
                          (x + 2, y + 2, GRID_SIZE-4, GRID_SIZE-4),
                          0, 3.14, 5)

        elif self.current_food['type'] == 'grapes':
            # Draw multiple grape circles
            for i in range(3):
                for j in range(3):
                    if (i+j) % 2 == 0:
                        pygame.draw.circle(surface, self.current_food['color'],
                                         (x + 6 + i*5, y + 6 + j*5), 3)
            # Add leaves
            pygame.draw.polygon(surface, (34, 139, 34),
                              [(x + GRID_SIZE//2, y),
                               (x + GRID_SIZE//2 + 4, y + 4),
                               (x + GRID_SIZE//2 - 4, y + 4)])

        elif self.current_food['type'] == 'cookie':
            # Draw cookie base
            pygame.draw.circle(surface, self.current_food['color'],
                             (x + GRID_SIZE//2, y + GRID_SIZE//2), 
                             GRID_SIZE//2 - 1)
            # Add chocolate chips
            for i in range(5):
                chip_x = x + 5 + random.randint(0, GRID_SIZE-10)
                chip_y = y + 5 + random.randint(0, GRID_SIZE-10)
                pygame.draw.circle(surface, (60, 30, 10),
                                 (chip_x, chip_y), 2)

    def randomize_position(self):
        # Ensure food aligns with grid
        self.position = (
            random.randint(1, (WINDOW_SIZE//GRID_SIZE)-2) * GRID_SIZE,
            random.randint(1, (WINDOW_SIZE//GRID_SIZE)-2) * GRID_SIZE
        )

class FoodManager:
    def __init__(self, window_size):
        self.window_size = window_size
        self.foods = []
        # Initialize with 3 foods
        while len(self.foods) < 3:
            new_food = Food()
            # Ensure food aligns with grid
            new_food.position = (
                random.randint(1, (self.window_size//GRID_SIZE)-2) * GRID_SIZE,
                random.randint(1, (self.window_size//GRID_SIZE)-2) * GRID_SIZE
            )
            # Check for overlap with existing foods
            if not any(f.position == new_food.position for f in self.foods):
                self.foods.append(new_food)

    def draw(self, surface):
        for food in self.foods:
            food.draw(surface)

    def check_collision(self, snake_pos):
        for i, food in enumerate(self.foods):
            # Create collision rects for more accurate detection
            food_rect = pygame.Rect(food.position[0], food.position[1], 
                                  GRID_SIZE, GRID_SIZE)
            snake_rect = pygame.Rect(snake_pos[0], snake_pos[1], 
                                   GRID_SIZE, GRID_SIZE)
            
            if food_rect.colliderect(snake_rect):
                eaten_food = food.current_food
                # Create new food to replace eaten one
                new_food = Food()
                attempts = 0
                while attempts < 100:
                    new_pos = (
                        random.randint(1, (self.window_size//GRID_SIZE)-2) * GRID_SIZE,
                        random.randint(1, (self.window_size//GRID_SIZE)-2) * GRID_SIZE
                    )
                    # Make sure new food doesn't overlap with existing ones
                    if not any(f.position == new_pos for f in self.foods):
                        new_food.position = new_pos
                        self.foods[i] = new_food
                        return eaten_food
                    attempts += 1
        return None

    def update_window_size(self, new_size):
        self.window_size = new_size
        # Adjust food positions for new window size
        for food in self.foods:
            food.position = (
                min(food.position[0], new_size - GRID_SIZE),
                min(food.position[1], new_size - GRID_SIZE)
            )

class Eagle:
    def __init__(self, window_size, position=None):
        self.grid_size = GRID_SIZE
        self.width = GRID_SIZE * 2
        self.height = GRID_SIZE * 2
        self.window_size = window_size
        # Generate random position that's not in the center where snake starts
        self.position = self.generate_random_position(window_size)
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.base_speed = 0.2
        self.speed = self.base_speed

    def generate_random_position(self, window_size):
        # Calculate center zone to avoid (where snake starts)
        center = window_size // 2
        safe_distance = 4 * GRID_SIZE  # Keep eagles away from snake's starting position
        
        while True:
            x = random.randint(0, (window_size - self.width) // GRID_SIZE) * GRID_SIZE
            y = random.randint(0, (window_size - self.height) // GRID_SIZE) * GRID_SIZE
            
            # Check if position is far enough from center
            if abs(x - center) > safe_distance or abs(y - center) > safe_distance:
                return (x, y)

    @staticmethod
    def create_formation(window_size, count):
        eagles = []
        for _ in range(count):
            new_eagle = Eagle(window_size)
            # Ensure eagles don't overlap with each other
            while any(Eagle.check_overlap(new_eagle, existing_eagle) for existing_eagle in eagles):
                new_eagle = Eagle(window_size)
            eagles.append(new_eagle)
        return eagles

    @staticmethod
    def check_overlap(eagle1, eagle2):
        # Create rectangles for collision detection
        rect1 = pygame.Rect(eagle1.position[0], eagle1.position[1], 
                          eagle1.width + GRID_SIZE, eagle1.height + GRID_SIZE)
        rect2 = pygame.Rect(eagle2.position[0], eagle2.position[1], 
                          eagle2.width + GRID_SIZE, eagle2.height + GRID_SIZE)
        return rect1.colliderect(rect2)

    def update(self):
        x, y = self.direction
        new_x = self.position[0] + (x * GRID_SIZE * self.speed)
        new_y = self.position[1] + (y * GRID_SIZE * self.speed)
        
        # Adjust boundary checking for larger size
        if new_x < 0:
            new_x = self.window_size - self.width
        elif new_x > self.window_size - self.width:
            new_x = 0
            
        if new_y < 0:
            new_y = self.window_size - self.height
        elif new_y > self.window_size - self.height:
            new_y = 0
            
        self.position = (new_x, new_y)
        
        # Change direction randomly
        if random.random() < 0.02:  # 2% chance to change direction
            self.direction = random.choice([UP, DOWN, LEFT, RIGHT])

    def draw(self, surface):
        # Draw larger eagle
        eagle_rect = pygame.Rect(self.position[0], self.position[1], 
                               self.width, self.height)
        pygame.draw.rect(surface, (139, 69, 19), eagle_rect)  # Brown color
        
        # Draw wings (larger)
        wing_width = self.width // 2
        wing_height = self.height // 2
        
        # Left wing
        pygame.draw.ellipse(surface, (165, 42, 42),  # Brown-red color
                          (self.position[0] - wing_width//2,
                           self.position[1] + wing_height//2,
                           wing_width, wing_height))
        
        # Right wing
        pygame.draw.ellipse(surface, (165, 42, 42),
                          (self.position[0] + self.width - wing_width//2,
                           self.position[1] + wing_height//2,
                           wing_width, wing_height))
        
        # Draw eyes (larger)
        eye_radius = 4  # Bigger eyes
        # Left eye
        pygame.draw.circle(surface, WHITE,
                         (self.position[0] + self.width//4,
                          self.position[1] + self.height//4), eye_radius)
        # Right eye
        pygame.draw.circle(surface, WHITE,
                         (self.position[0] + 3*self.width//4,
                          self.position[1] + self.height//4), eye_radius)
        
        # Draw beak (larger)
        beak_points = [
            (self.position[0] + self.width//2, self.position[1] + self.height//4),
            (self.position[0] + self.width//3, self.position[1] + self.height//2),
            (self.position[0] + 2*self.width//3, self.position[1] + self.height//2)
        ]
        pygame.draw.polygon(surface, (255, 165, 0), beak_points)  # Orange beak

    def update_speed(self, score):
        # Increase eagle speed with score
        self.speed = self.base_speed + (score // 10) * 0.1

def show_death_screen(surface, death_type, window_size):
    font_large = pygame.font.Font(None, min(64, int(window_size / 10)))
    surface.fill(BACKGROUND)
    
    if death_type == "eagle":
        # Draw eagle eating snake scene
        eagle_size = min(window_size // 2, 200)  # Size of eagle image
        
        # Draw large eagle (centered, top half)
        eagle_pos = (window_size//2 - eagle_size//2, window_size//4)
        pygame.draw.rect(surface, (139, 69, 19), 
                        (eagle_pos[0], eagle_pos[1], eagle_size, eagle_size))
        
        # Draw eagle's wings
        wing_width = eagle_size * 0.7
        wing_height = eagle_size * 0.4
        # Left wing
        pygame.draw.ellipse(surface, (165, 42, 42),
                          (eagle_pos[0] - wing_width//3,
                           eagle_pos[1] + wing_height,
                           wing_width, wing_height))
        # Right wing
        pygame.draw.ellipse(surface, (165, 42, 42),
                          (eagle_pos[0] + eagle_size - wing_width*2//3,
                           eagle_pos[1] + wing_height,
                           wing_width, wing_height))
        
        # Draw snake being eaten (dangling from eagle's beak)
        snake_color = (50, 255, 50)  # Green
        snake_segments = [(eagle_pos[0] + eagle_size//2, eagle_pos[1] + eagle_size*0.7)]
        for i in range(5):  # Wavy snake body
            x = snake_segments[0][0] + math.sin(i/2) * 20
            y = snake_segments[0][1] + i * 20
            snake_segments.append((x, y))
        
        for i in range(len(snake_segments)-1):
            pygame.draw.line(surface, snake_color, 
                           snake_segments[i], snake_segments[i+1], 10)
        
        # Draw eagle's eyes (angry)
        eye_size = eagle_size * 0.1
        pygame.draw.line(surface, (0, 0, 0),
                        (eagle_pos[0] + eagle_size//3, eagle_pos[1] + eagle_size//3),
                        (eagle_pos[0] + eagle_size//3 - eye_size, eagle_pos[1] + eagle_size//3 - eye_size), 5)
        pygame.draw.line(surface, (0, 0, 0),
                        (eagle_pos[0] + eagle_size*2//3, eagle_pos[1] + eagle_size//3),
                        (eagle_pos[0] + eagle_size*2//3 + eye_size, eagle_pos[1] + eagle_size//3 - eye_size), 5)
        
    else:  # self collision
        # Draw dizzy snake
        snake_size = min(window_size // 2, 200)
        center_x = window_size // 2
        center_y = window_size // 2
        
        # Draw coiled snake body
        for i in range(0, 360, 20):
            radius = snake_size//3 - i//8
            x = center_x + math.cos(math.radians(i)) * radius
            y = center_y + math.sin(math.radians(i)) * radius
            pygame.draw.circle(surface, GREEN, (int(x), int(y)), 10)
        
        # Draw dizzy eyes (X X)
        eye_size = 15
        # Left eye
        pygame.draw.line(surface, BLUE,
                        (center_x - 30 - eye_size, center_y - eye_size),
                        (center_x - 30 + eye_size, center_y + eye_size), 4)
        pygame.draw.line(surface, BLUE,
                        (center_x - 30 - eye_size, center_y + eye_size),
                        (center_x - 30 + eye_size, center_y - eye_size), 4)
        # Right eye
        pygame.draw.line(surface, BLUE,
                        (center_x + 30 - eye_size, center_y - eye_size),
                        (center_x + 30 + eye_size, center_y + eye_size), 4)
        pygame.draw.line(surface, BLUE,
                        (center_x + 30 - eye_size, center_y + eye_size),
                        (center_x + 30 + eye_size, center_y - eye_size), 4)
        
        # Draw dizzy stars
        for i in range(5):
            angle = i * (360/5)
            star_x = center_x + math.cos(math.radians(angle)) * snake_size//1.5
            star_y = center_y + math.sin(math.radians(angle)) * snake_size//1.5
            pygame.draw.circle(surface, (255, 255, 0), (int(star_x), int(star_y)), 5)

    pygame.display.flip()
    pygame.time.wait(4000)  # Wait 4 seconds

def show_game_over(surface, score, food_collected, window_size, death_type):
    # Show death animation first
    show_death_screen(surface, death_type, window_size)
    
    # Then show collection screen (without "Game Over" text)
    running = True
    font_large = pygame.font.Font(None, min(64, int(window_size / 10)))
    font_small = pygame.font.Font(None, min(36, int(window_size / 15)))
    
    # Create restart button
    button_width = min(200, int(window_size / 3))
    button_height = min(50, int(window_size / 10))
    button_rect = pygame.Rect(window_size//2 - button_width//2,
                             window_size - button_height - 20,
                             button_width, button_height)

    while running:
        surface.fill(BACKGROUND)
        
        # Score text
        score_text = font_large.render(f'Score: {score}', True, (0, 0, 0))
        score_rect = score_text.get_rect()
        score_rect.centerx = window_size//2
        score_rect.top = window_size//8
        surface.blit(score_text, score_rect)
        
        # Food collection display
        y_offset = score_rect.bottom + 20
        title = font_small.render('Food Collected:', True, (0, 0, 0))
        surface.blit(title, (window_size//6, y_offset))
        
        # Create two columns for food display
        col_width = window_size // 2
        max_rows = (button_rect.top - y_offset - 30) // 30
        
        # Sort and display food items
        sorted_foods = sorted(food_collected.items(), key=lambda x: x[0])
        temp_food = Food()
        
        for i, (food_type, count) in enumerate(sorted_foods):
            col = i // max_rows
            row = i % max_rows
            
            x_offset = window_size//6 + (col * col_width)
            current_y = y_offset + 30 + (row * 30)
            
            food_info = next((f for f in temp_food.food_types if f['type'] == food_type), None)
            if food_info:
                temp_food.current_food = food_info
                temp_food.position = (x_offset, current_y)
                temp_food.draw(surface)
                
                food_name = food_type.replace('_', ' ').title()
                food_text = font_small.render(f"{food_name} x {count}", True, (0, 0, 0))
                surface.blit(food_text, (x_offset + GRID_SIZE + 10, current_y))

        # Draw restart button
        pygame.draw.rect(surface, (100, 200, 100), button_rect)
        pygame.draw.rect(surface, (50, 150, 50), button_rect, 3)
        restart_text = font_small.render('Play Again', True, (0, 0, 0))
        restart_rect = restart_text.get_rect()
        restart_rect.center = button_rect.center
        surface.blit(restart_text, restart_rect)
        
        pygame.display.flip()
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    return True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    return True

    return False

def calculate_window_size(score):
    min_size = WINDOW_SIZE // 2  # Half of max size (300)
    max_size = WINDOW_SIZE       # Max size (600)
    
    # Change window size every 20 points instead of continuously
    size_steps = 4  # Number of size increases
    points_per_step = 20  # Points needed for each size increase
    
    if score >= size_steps * points_per_step:
        return max_size
        
    current_step = score // points_per_step
    size_per_step = (max_size - min_size) / size_steps
    
    return int(min_size + (current_step * size_per_step))

def main():
    pygame.init()
    current_window_size = WINDOW_SIZE // 2  # Start with exact half size
    screen = pygame.display.set_mode((current_window_size, current_window_size))
    pygame.display.set_caption('Snake Game')
    
    running = True
    while running:
        clock = pygame.time.Clock()
        last_update = time.time()
        snake = Snake(current_window_size)
        food_manager = FoodManager(current_window_size)
        eagles = Eagle.create_formation(current_window_size, 2)
        eagle_count = 2
        game_over = False

        while not game_over:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    game_over = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and snake.direction != DOWN:
                        snake.direction = UP
                    elif event.key == pygame.K_DOWN and snake.direction != UP:
                        snake.direction = DOWN
                    elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                        snake.direction = LEFT
                    elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                        snake.direction = RIGHT

            # Update game state
            if time.time() - last_update > 1/snake.speed:
                # Update eagles
                for eagle in eagles:
                    eagle.update()
                
                # Update snake and check collisions
                if not snake.update():
                    game_over = True
                    death_type = "self"
                    continue

                # Check eagle collisions
                snake_head = snake.get_head_position()
                for eagle in eagles:
                    eagle_rect = pygame.Rect(eagle.position[0], eagle.position[1], 
                                           eagle.width, eagle.height)
                    snake_rect = pygame.Rect(snake_head[0], snake_head[1], 
                                           GRID_SIZE-1, GRID_SIZE-1)
                    if eagle_rect.colliderect(snake_rect):
                        game_over = True
                        death_type = "eagle"
                        break

                last_update = time.time()

            # Update speeds based on score
            snake.update_speed()
            for eagle in eagles:
                eagle.update_speed(snake.score)

            # Check food collision
            eaten_food = food_manager.check_collision(snake.get_head_position())
            if eaten_food:
                snake.length += 1
                snake.score += eaten_food['points']
                if eaten_food['type'] not in snake.food_collected:
                    snake.food_collected[eaten_food['type']] = 0
                snake.food_collected[eaten_food['type']] += 1
                
                # Add new eagle every 30 points
                if len(eagles) < snake.score // 30 + 2:  # +2 for initial eagles
                    new_eagle = Eagle(current_window_size)
                    # Ensure new eagle doesn't overlap with existing eagles
                    attempts = 0
                    while attempts < 100 and any(Eagle.check_overlap(new_eagle, existing_eagle) for existing_eagle in eagles):
                        new_eagle = Eagle(current_window_size)
                    eagles.append(new_eagle)

                # Update window size
                new_window_size = calculate_window_size(snake.score)
                if new_window_size != current_window_size:
                    current_window_size = new_window_size
                    screen = pygame.display.set_mode((current_window_size, current_window_size))
                    snake.update_window_size(current_window_size)
                    food_manager.window_size = current_window_size
                    for eagle in eagles:
                        eagle.window_size = current_window_size

            # Draw everything
            screen.fill(BACKGROUND)
            snake.draw(screen)
            food_manager.draw(screen)
            for eagle in eagles:
                eagle.draw(screen)
            draw_score(screen, snake.score)
            
            pygame.display.flip()
            clock.tick(60)

        if game_over:
            running = show_game_over(screen, snake.score, snake.food_collected, current_window_size, death_type)

    pygame.quit()

def draw_score(surface, score):
    font = pygame.font.Font(None, 36)
    text = font.render(f'Score: {score}', True, (0, 0, 0))
    surface.blit(text, (10, 10))

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

if __name__ == "__main__":
    main() 