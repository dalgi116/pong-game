import pygame, math, random
pygame.init()

singlePlayerMode = True
fps = 60
width, height = 1100, 700
backgroundColor = (53, 40, 232)

ballWidth, ballHeight = 30, 30
startBallSpeed = 3
ballAcceleration = 0.5

deskWidth, deskHeight = 20, 120
deskSpeed = 5

rightScores = pygame.USEREVENT + 1
leftScores = pygame.USEREVENT + 2
window = pygame.display.set_mode((width, height))
background = pygame.Rect(0, 0, width, height)
ball = pygame.transform.scale(pygame.image.load("assets/circle.png"), (ballWidth, ballHeight))
if singlePlayerMode:
    deskLeft = pygame.transform.scale(pygame.image.load("assets/rectangle.png"), (deskWidth, height))
else:
    deskLeft = pygame.transform.scale(pygame.image.load("assets/rectangle.png"), (deskWidth, deskHeight))
deskRight = pygame.transform.scale(pygame.image.load("assets/rectangle.png"), (deskWidth, deskHeight))
textFont = pygame.font.SysFont("arial", 60)

def accelerate(xSpeed, ySpeed):
    if xSpeed > 0:
        xSpeed += ballAcceleration
    if xSpeed < 0:
        xSpeed -= ballAcceleration
    if ySpeed > 0:
        ySpeed += ballAcceleration
    if ySpeed < 0:
        ySpeed -= ballAcceleration
    return xSpeed, ySpeed

def newPoint(ballR, deskLeftR, deskRightR, leftPoints, rightPoints, hits):
    ballR.x, ballR.y = width/2 - ballWidth/2, height/2 - ballHeight/2
    if singlePlayerMode:
        deskLeftR.x, deskLeftR.y = 10, 0
    else:
        deskLeftR.x, deskLeftR.y = 10, height/2 - deskHeight/2
    deskRightR.x, deskRightR.y = width - deskWidth - 10, height/2 - deskHeight/2
    hits = 0
    xSpeed, ySpeed = getstartBallSpeed(startBallSpeed)
    drawWindow(ballR, deskLeftR, deskRightR, leftPoints, rightPoints, hits)
    pygame.time.delay(2000)
    return hits, xSpeed, ySpeed

def moveBall(ballR, xSpeed, ySpeed, deskLeftR, deskRightR, hits):
    if ballR.y <= 0:
        ySpeed = abs(ySpeed)
    if ballR.y + ballHeight >= height:
        ySpeed = - abs(ySpeed)
    if ballR.colliderect(deskLeftR):
        xSpeed = abs(xSpeed)
        hits += 1
        xSpeed, ySpeed = accelerate(xSpeed, ySpeed)
    if ballR.colliderect(deskRightR):
        xSpeed = - abs(xSpeed)
        xSpeed, ySpeed = accelerate(xSpeed, ySpeed)


    if ballR.x + ballWidth <= 0:
        pygame.event.post(pygame.event.Event(rightScores))
    if ballR.x >= width:
        pygame.event.post(pygame.event.Event(leftScores))

    ballR.x += xSpeed
    ballR.y += ySpeed
    return xSpeed, ySpeed, hits

def moveLeft(keysPressed, deskLeftR):
    if keysPressed[pygame.K_w] and deskLeftR.y > 0:
        deskLeftR.y -= deskSpeed
    if keysPressed[pygame.K_s] and deskLeftR.y < height - deskHeight:
        deskLeftR.y += deskSpeed

def moveRight(keysPressed, deskRightR):
    if keysPressed[pygame.K_UP] and deskRightR.y > 0:
        deskRightR.y -= deskSpeed
    if keysPressed[pygame.K_DOWN] and deskRightR.y < height - deskHeight:
        deskRightR.y += deskSpeed

def getstartBallSpeed(startBallSpeed):
    list = [startBallSpeed, -startBallSpeed]
    xSpeed = random.choice(list)
    ySpeed = random.choice(list)
    return xSpeed, ySpeed

def drawWindow(ballR, deskLeftR, deskRightR, leftPoints, rightPoints, hits):
    pygame.draw.rect(window, backgroundColor, background)
    window.blit(ball, (ballR.x, ballR.y))
    window.blit(deskLeft, (deskLeftR.x, deskLeftR.y))
    window.blit(deskRight, (deskRightR.x, deskRightR.y))

    if singlePlayerMode:
        pointsText = textFont.render(str(hits), 1, (255, 255, 255))
    else:
        pointsText = textFont.render(str(leftPoints) + " : " + str(rightPoints), 1, (255, 255, 255))
    window.blit(pointsText, (width/2 - pointsText.get_width()/2, 10))

    pygame.display.update()

def main():
    leftPoints = 0
    rightPoints = 0
    hits = 0
    xSpeed, ySpeed = getstartBallSpeed(startBallSpeed)

    ballR = pygame.Rect(width/2 - ballWidth/2, height/2 - ballHeight/2, ballWidth, ballHeight)
    if singlePlayerMode:
        deskLeftR = pygame.Rect(10, 0, deskWidth, height)
    else:
        deskLeftR = pygame.Rect(10, height/2 - deskHeight/2, deskWidth, deskHeight)
    deskRightR = pygame.Rect(width - deskWidth - 10, height/2 - deskHeight/2, deskWidth, deskHeight)

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == rightScores:
                rightPoints += 1
                hits, xSpeed, ySpeed = newPoint(ballR, deskLeftR, deskRightR, leftPoints, rightPoints, hits)
            if event.type == leftScores:
                leftPoints += 1
                hits, xSpeed, ySpeed = newPoint(ballR, deskLeftR, deskRightR, leftPoints, rightPoints, hits)

        keysPressed = pygame.key.get_pressed()
        if not singlePlayerMode:
            moveLeft(keysPressed, deskLeftR)
        moveRight(keysPressed, deskRightR)

        xSpeed, ySpeed, hits = moveBall(ballR, xSpeed, ySpeed, deskLeftR, deskRightR, hits)

        drawWindow(ballR, deskLeftR, deskRightR, leftPoints, rightPoints, hits)


main()
pygame.quit()