import pygame
import random
from game import start_game
# Inicializar o Pygame
pygame.init()

# Configurações da tela
WIDTH, HEIGHT = 600, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bird Sort Game")
clock = pygame.time.Clock()

# Definição de cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (135, 206, 250)  # Cor de fundo igual ao menu principal
BUTTON_COLOR = (0, 255, 0)  # Cor do botão igual ao menu principal

# Definir fontes
font = pygame.font.SysFont(None, 48)

# Opções do menu
options = ["Play (Human)", "Play (AI)", "Quit"]
selected_option = 0

# Função para desenhar o menu
def draw_menu():
    screen.fill(BLUE)  # Cor de fundo igual ao menu principal
    mouse_pos = pygame.mouse.get_pos()  # Pega a posição do mouse

    # Título do jogo
    title_text = font.render("Bird Sort Game", True, BLACK)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 100))

    # Desenhar botões
    for i, option in enumerate(options):
        # Verifica se o mouse está sobre o botão
        button_width, button_height = 300, 60
        button_rect = pygame.Rect(WIDTH // 2 - button_width // 2, 300 + i * 100, button_width, button_height)

        # Se o mouse está sobre o botão, a cor do texto será cinza
        if button_rect.collidepoint(mouse_pos):
            color = GRAY  # Cor do texto quando o mouse está em cima
        else:
            color = BLACK  # Cor normal do texto

        # Renderizar o texto
        text = font.render(option, True, color)

        # Desenhar os botões
        pygame.draw.rect(screen, BUTTON_COLOR, button_rect)

        # Escrever o texto nos botões
        screen.blit(text, (button_rect.centerx - text.get_width() // 2, button_rect.centery - text.get_height() // 2))

    pygame.display.flip()

# Função principal
def main():
    from submenu import ai_submenu  # Importa a função do submenu de IA
    
    running = True
    while running:
        draw_menu()  # Desenhar o menu

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False  # Sair do jogo
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                # Verificar se algum botão foi clicado
                button_width, button_height = 300, 60
                button_rects = [
                    pygame.Rect(WIDTH // 2 - button_width // 2, 300 + i * 100, button_width, button_height)
                    for i in range(len(options))
                ]
                
                for i, button_rect in enumerate(button_rects):
                    if button_rect.collidepoint(mouse_pos):
                        # Lidar com a escolha de cada opção
                        if i == 0:  # "Play (Human)"
                            level = random.choice(['facil', 'medio', 'dificil'])
                            start_game(level)
                        elif i == 1:  # "Play (AI)"
                            ai_submenu()  # Iniciar o submenu de IA
                        elif i == 2:  # "Quit"
                            running = False  # Sair do jogo

    pygame.quit()

if __name__ == "__main__":
    main()
