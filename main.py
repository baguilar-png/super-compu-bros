import pygame, instrucciones, eleccionPersonajes, juego, archivos

def main():
    pygame.init()
    ANCHO = 1280
    ALTO = 720
    ventana = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Rectángulo con WASD")
    boton1 = pygame.rect(0, 0, 100)
    boton1.center = (1280 // 2, 720 // 2)
    reloj = pygame.time.Clock()
    ejecutando = True
    while ejecutando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
        teclas = pygame.key.get_pressed()
        ventana.fill((25, 30, 40))
        pygame.draw.rect(ventana, (80, 200, 255), (0, 0, 1280, 720))
        boton1 = pygame.draw.rect(ventana, (128, 128, 128), (boton1))
        pygame.display.flip()
        reloj.tick(60)

main()