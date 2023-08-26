import pygame
import math
import random

frameRate = 60

WIDTH, HEIGHT = 1366, 768

surface = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()

pygame.font.init()

# Creating Ball Class
class Ball:

    def __init__(self, x, y, speedX, speedY, size, color, isGrabbed=False):
        self.x = x
        self.y = y
        self.speedX = speedX
        self.speedY = speedY
        self.size = size
        self.isGrabbed = isGrabbed
        self.x2 = self.x
        self.y2 = self.y
        self.mass = math.pi * math.pow(self.size, 2)
        self.color = color
        self.accelerationX = 0
        self.accelerationY = 0

    def displayObj(self):
        circle = pygame.draw.circle(surface, self.color, [self.x, self.y], self.size)
        return circle

    def getToMousePos(self, mousePos, isGrabbed):
        if isGrabbed:
            self.x = mousePos[0]
            self.y = mousePos[1]


# Distance Formula
def distanceObj_Obj(objX, objY, objX2, objY2):
    distanceX = objX2 - objX
    distanceY = objY2 - objY
    distanceZ = math.sqrt(math.pow(distanceX, 2) + math.pow(distanceY, 2))
    return [distanceX, distanceY, distanceZ]

# Normalizing Vectors
def normalize(x, y):
    length = math.sqrt(x ** 2 + y ** 2)
    if length != 0:
        return x / length, y / length
    else:
        return 0, 0
    
def drawText(text, font, textCol, x, y):
    img = font.render(text, True, textCol)
    surface.blit(img, (x, y))

def gravitationalAcceleration(mass1, mass2, z):
    acceleration = (mass1 * mass2 * 100) / z ** 2
    return acceleration

# Game Font
font = pygame.font.SysFont("Arial", 20)

# Creating Object arrays for Obj access
ballObjs = []

# Physics States
gravitationalForce = 0
isCoulomb = False

running = True
while running:

    pygame.display.set_caption(str(clock.get_fps()))

    # EVENT HANDLERS
    events = []

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE:
                ball = Ball(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 0, 0, random.randint(10, 30), (
                    random.randint(1, 255), random.randint(1, 255), random.randint(1, 255)
                ))
                ballObjs.append(ball)

            if event.key == pygame.K_r:
                if (len(ballObjs) > 0):
                    ballObjs.pop()

            if event.key == pygame.K_q:
                isCoulomb = not isCoulomb

            if event.key == pygame.K_w:
                gravitationalForce+= 0.5

            if event.key == pygame.K_e:
                gravitationalForce-= 0.5

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT:
                events.append("leftClickDown")

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == pygame.BUTTON_LEFT:
                events.append("leftClickUp")

    for obj in ballObjs:
        accelerationX = 0
        accelerationY = gravitationalForce

        for obj2 in ballObjs:
            if obj2 != obj and ballObjs:
                distances = distanceObj_Obj(obj2.x, obj2.y, obj.x, obj.y)
                #print(distances)
                distance = distances[2]

                # Calculating Acceleration Due to Size of Obj
                accelerationDueObj = 0

                if (isCoulomb):
                    accelerationDueObj = gravitationalAcceleration(obj.size, obj2.size, distance)
                else:
                    accelerationDueObj = 0
                
                accelerationX += (-1 * (distances[0] / distances[2]) * accelerationDueObj) / obj.size
                accelerationY += (-1 * (distances[1] / distances[2]) * accelerationDueObj) / obj.size

                if obj.size + obj2.size >= distance:
                    # Alligning two Obj
                    overlap = (obj.size + obj2.size) - distance
                    dir_x, dir_y = normalize(obj2.x - obj.x, obj2.y - obj.y)
                    displacement_x = dir_x * overlap
                    displacement_y = dir_y * overlap
                    obj.x -= displacement_x
                    obj.y -= displacement_y
                    obj2.x += displacement_x
                    obj2.y += displacement_y

                    # calculate velocities before the collision
                    vx1 = obj.speedX
                    vy1 = obj.speedY
                    vx2 = obj2.speedX
                    vy2 = obj2.speedY

                    # calculate normal vector
                    nx = obj2.x - obj.x
                    ny = obj2.y - obj.y
                    nx, ny = normalize(nx, ny)

                    # calculate tangent vector
                    tx = -ny
                    ty = nx

                    # calculate dot products
                    dpTan1 = (vx1 * tx) + (vy1 * ty)
                    dpTan2 = (vx2 * tx) + (vy2 * ty)
                    dpNorm1 = (vx1 * nx) + (vy1 * ny)
                    dpNorm2 = (vx2 * nx) + (vy2 * ny)

                    # calculate conservation of kinetic energy
                    m1 = obj.mass
                    m2 = obj2.mass
                    v1 = ((dpNorm1 * (m1 - m2)) + 2 * m2 * dpNorm2) / (m1 + m2)
                    v2 = ((dpNorm2 * (m2 - m1)) + 2 * m1 * dpNorm1) / (m1 + m2)

                    # update velocities after the collision
                    obj.speedX = tx * dpTan1 + nx * v1
                    obj.speedY = ty * dpTan1 + ny * v1
                    obj2.speedX = tx * dpTan2 + nx * v2
                    obj2.speedY = ty * dpTan2 + ny * v2

        obj.accelerationX = accelerationX
        obj.accelerationY = accelerationY

    # OBJ DATAS1
    for obj in ballObjs:

        if (obj.x > WIDTH - obj.size or obj.x < 0 + obj.size) or (
                obj.y > HEIGHT - obj.size or obj.y < 0 + obj.size):

            if obj.x > WIDTH - obj.size:
                obj.x = WIDTH - obj.size
                obj.speedX *= -0.80
            elif obj.x < 0 + obj.size:
                obj.x = 0 + obj.size
                obj.speedX *= -0.80
            elif obj.y > HEIGHT - obj.size:
                obj.y = HEIGHT - obj.size
                obj.speedY *= -0.80
            elif obj.y < 0 + obj.size:
                obj.y = 0 + obj.size
                obj.speedY *= -0.80

        if not obj.isGrabbed:
            obj.speedY += obj.accelerationY
            obj.speedY += 0
            obj.speedX += obj.accelerationX
            obj.x += obj.speedX
            obj.y += obj.speedY

        if obj.isGrabbed:
            obj.x2 = obj.x
            obj.y2 = obj.y
            obj.getToMousePos(pygame.mouse.get_pos(), obj.isGrabbed)
            obj.speedX, obj.speedY = obj.x - obj.x2, obj.y - obj.y2

        if obj.displayObj().collidepoint(pygame.mouse.get_pos()):
            if "leftClickDown" in events:
                events.remove("leftClickDown")
                obj.isGrabbed = True
            elif "leftClickUp" in events:
                events.remove("leftClickUp")
                obj.isGrabbed = False

        ballObjsMomentum = []

    # DATA DISPLAYS
    surface.fill("white")

    # Display Game State
    drawText(f"Number Of Objects: {len(ballObjs)}", font, (0, 0, 0), 0, 0)
    drawText(f"Coulomb Force: {isCoulomb}", font, (0, 0, 0), 0, 30)
    drawText(f"Gravity Intensity: {gravitationalForce}", font, (0, 0, 0), 0, 60)

    # Display Controls
    drawText(f"Toggle Coulomb: Q", font, (0, 0, 0), 0, HEIGHT - 30)
    drawText(f"↓ Gravity: E", font, (0, 0, 0), 0, HEIGHT - 60)
    drawText(f"↑ Gravity: W", font, (0, 0, 0), 0, HEIGHT - 90)
    drawText(f"Remove Object: R", font, (0, 0, 0), 0, HEIGHT - 120)
    drawText(f"Create Object: SPACE", font, (0, 0, 0), 0, HEIGHT - 150)
    drawText(f"Drag Object: MOUSE DRAG", font, (0, 0, 0), 0, HEIGHT - 180)

    # Display Ball Objects
    for display in ballObjs:
        display.displayObj()

    pygame.display.update()
    clock.tick(frameRate)
