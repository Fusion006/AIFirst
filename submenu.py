import pygame
from main_menu import main  # Importa a função main do menu principal

# Inicializar o Pygame
pygame.init()

# Configurações da tela
WIDTH, HEIGHT = 600, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AI Submenu")

# Definição de cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (135, 206, 250)  # Cor de fundo igual ao menu principal
BUTTON_COLOR = (0, 255, 0)  # Cor do botão igual ao menu principal

# Definir fontes
font = pygame.font.SysFont(None, 36)

# Opções do submenu
options = ["DFS", "BFS", "ITERATIVE DEEPENING", "GREEDY SEARCH", "A*", "Back to Main Menu"]
selected_option = 0

# Função para desenhar o menu
def draw_menu():
    screen.fill(BLUE)  # Cor de fundo igual ao menu principal
    mouse_pos = pygame.mouse.get_pos()  # Pega a posição do mouse

    for i, option in enumerate(options):
        # Verifica se o mouse está sobre o botão
        button_width, button_height = 300, 60
        button_rect = pygame.Rect(WIDTH // 2 - button_width // 2, 200 + i * 100, button_width, button_height)

        # Se o mouse está sobre o botão, a cor do texto será cinza
        if button_rect.collidepoint(mouse_pos):
            color = GRAY  # Cor do texto quando o mouse está em cima
        else:
            color = BLACK if i != selected_option else GRAY  # Cor normal ou selecionada

        # Renderizar o texto
        text = font.render(option, True, color)

        # Desenhar os botões
        pygame.draw.rect(screen, BUTTON_COLOR, button_rect)

        # Escrever o texto nos botões
        screen.blit(text, (button_rect.centerx - text.get_width() // 2, button_rect.centery - text.get_height() // 2))

    pygame.display.flip()

# Função para o submenu de IA
def ai_submenu():
    global selected_option
    running = True
    while running:
        draw_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                # Verificar se algum botão foi clicado
                button_width, button_height = 300, 60
                button_rects = [
                    pygame.Rect(WIDTH // 2 - button_width // 2, 200 + i * 100, button_width, button_height)
                    for i in range(len(options))
                ]
                
                for i, button_rect in enumerate(button_rects):
                    if button_rect.collidepoint(mouse_pos):
                        # Lidar com a escolha de cada opção
                        if i == 5:  # Back to Main Menu
                            main()  # Chama a função main() do menu principal
                        # Adicione os casos para as outras opções do submenu se necessário

    pygame.quit()
