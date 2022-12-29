import sys, pygame

pygame.init()
#muestro ventana
size =800, 600
screen= pygame.display.set_mode(size)

pygame.display.set_caption("Juego Ball")
#Variables
width, height = 800, 600
speed = [1, 1]
white = 255, 255, 255

#creA UNA IMAGEN Y OBTENGO SU RECTANGULO
ball = pygame.image.load("ball1.png")
ballrect = ball.get_rect()
#CREO UN OBJETO IMAGEN DE BATE Y OBTENGO SU RECTANGULO
bate = pygame.image.load("bate2.jpg")
baterect = bate.get_rect()
#bate en centro de pantalla
baterect.move_ip(400, 260)
#comenzamos bucle de juego
run=True
while run:
    pygame.time.delay(0)
    #capturamos eventos que se han producido
    for event in pygame.event.get():
        #si el vento es saalir de la ventana, terminamos
        if event.type == pygame.QUIT: run= False

#Compruebo si se ha pulsado alguna tecla
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        baterect=baterect.move(0, -1)
    if keys[pygame.K_DOWN]:
        baterect=baterect.move(0, 1)

 #Compryebo si hay colision
    if baterect.colliderect(ballrect):
         speed[0] = - speed[0]               

        #MUEVO  LA PELOTA
    ballrect = ballrect.move(speed)
    #compreubo si la pelota llega a los limites de la ventana
    if ballrect.left < 0 or ballrect.right > width:
        speed[0] = -speed[0]
    if ballrect.top < 0 or ballrect.bottom > height:
        speed[1] = -speed[1]   
        #pinto el fondo de blanco, dibujo pelota y actualizo 
    screen.fill(white)
    screen.blit(ball, ballrect)
    pygame.display.flip()

    #salgo de pygame
pygame.quit()


       