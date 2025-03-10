import pygame
import random

# Configurações do jogo
WIDTH, HEIGHT = 600, 800
BIRD_COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]  # Cores dos pássaros
BIRDS_PER_COLOR = 4  # Cada cor tem 4 pássaros
TOTAL_BIRDS = BIRDS_PER_COLOR * len(BIRD_COLORS)  # 16 pássaros no total

# Inicializar o Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jogo dos Pássaros")
clock = pygame.time.Clock()

font = pygame.font.Font(None, 36)

class Branch:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.birds = []

    def draw(self, screen):
        pygame.draw.rect(screen, (139, 69, 19), (self.x, self.y, 80, 150))
        for i, bird in enumerate(self.birds):
            pygame.draw.circle(screen, bird, (self.x + 40, self.y + 30 + i * 30), 15)

    def add_bird(self, color):
        if len(self.birds) < 4:
            self.birds.append(color)

    def remove_bird(self):
        if self.birds:
            return self.birds.pop()
        return None

    def is_complete(self):
        return len(self.birds) == 4 and all(b == self.birds[0] for b in self.birds)

# Funções de distribuição para cada nível
def distribuir_facil():
    branches = [Branch(100 + i * 100, 500) for i in range(5)]
    birds = BIRD_COLORS * 4  # 16 pássaros
    random.shuffle(birds)
    index = 0
    while index < len(birds):
        for branch in branches:
            if index < len(birds) and len(branch.birds) < 4:
                branch.add_bird(birds[index])
                index += 1
    return branches

def distribuir_medio():
    branches = [Branch(80 + i * 100, 500) for i in range(5)]
    birds = BIRD_COLORS * 4
    random.shuffle(birds)
    index = 0
    while index < len(birds):
        for branch in branches:
            if index < len(birds) and len(branch.birds) < 4:
                branch.add_bird(birds[index])
                index += 1
    return branches

def distribuir_dificil():
    branches = [Branch(60 + i * 100, 500) for i in range(5)]
    birds = BIRD_COLORS * 4
    random.shuffle(birds)
    index = 0
    while index < len(birds):
        for branch in branches:
            if index < len(birds) and len(branch.birds) < 4:
                branch.add_bird(birds[index])
                index += 1
    return branches

def start_game(level):
    if level == 'facil':
        branches = distribuir_facil()
    elif level == 'medio':
        branches = distribuir_medio()
    else:
        branches = distribuir_dificil()
    
    score = 0
    selected_branch = None
    running = True
    while running:
        screen.fill((135, 206, 250))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                for branch in branches:
                    if branch.x < x < branch.x + 80 and branch.y < y < branch.y + 150:
                        if selected_branch is None:
                            selected_branch = branch
                        else:
                            if selected_branch != branch:
                                bird = selected_branch.remove_bird()
                                if bird is not None:
                                    branch.add_bird(bird)
                            selected_branch = None
        
        # Remover galhos completos e aumentar o score
        new_branches = []
        for branch in branches:
            if branch.is_complete():
                score += 10
            else:
                new_branches.append(branch)
        branches = new_branches
        
        for branch in branches:
            branch.draw(screen)
        
        score_text = font.render(f"Score: {score}", True, (0, 0, 0))
        screen.blit(score_text, (WIDTH - 150, 20))
        
        pygame.display.flip()
        clock.tick(30)
    
    pygame.quit()

