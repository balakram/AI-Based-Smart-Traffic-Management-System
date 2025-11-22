# src/simulation.py
"""
Traffic intersection simulation with AI-based adaptive green time controller.

Run: python src/simulation.py

Dependencies: pygame, numpy
"""

import random
import time
import threading
import pygame
import sys
import os

from ai_controller import start_controller

# -----------------------------
# Config - toggle AI here
USE_AI = True

defaultGreen = {0:20, 1:20, 2:20, 3:20}
defaultRed = 150
defaultYellow = 5

shared_state = {
    'defaultGreen': defaultGreen,
}

signals = []
noOfSignals = 4
currentGreen = 0
nextGreen = (currentGreen+1)%noOfSignals
currentYellow = 0

speeds = {'car':2.25, 'bus':1.8, 'truck':1.8, 'bike':2.5}

x = {'right':[0,0,0], 'down':[755,727,697], 'left':[1400,1400,1400], 'up':[602,627,657]}
y = {'right':[348,370,398], 'down':[0,0,0], 'left':[498,466,436], 'up':[800,800,800]}

vehicles = {'right': {0:[], 1:[], 2:[], 'crossed':0}, 'down': {0:[], 1:[], 2:[], 'crossed':0},
            'left': {0:[], 1:[], 2:[], 'crossed':0}, 'up': {0:[], 1:[], 2:[], 'crossed':0}}

vehicleTypes = {0:'car', 1:'bus', 2:'truck', 3:'bike'}
directionNumbers = {0:'right', 1:'down', 2:'left', 3:'up'}

signalCoods = [(530,230),(810,230),(810,570),(530,570)]
signalTimerCoods = [(530,210),(810,210),(810,550),(530,550)]

stopLines = {'right': 590, 'down': 330, 'left': 800, 'up': 535}
defaultStop = {'right': 580, 'down': 320, 'left': 810, 'up': 545}

stoppingGap = 15
movingGap = 15

shared_state.update({
    'stopLines': stopLines,
    'vehicles': vehicles,
    'directionNumbers': directionNumbers
})

class TrafficSignal:
    def __init__(self, red, yellow, green):
        self.red = red
        self.yellow = yellow
        self.green = green
        self.signalText = ""

pygame.init()
simulation = pygame.sprite.Group()

class Vehicle(pygame.sprite.Sprite):
    def __init__(self, lane, vehicleClass, direction_number, direction):
        pygame.sprite.Sprite.__init__(self)
        self.lane = lane
        self.vehicleClass = vehicleClass
        self.speed = speeds[vehicleClass]
        self.direction_number = direction_number
        self.direction = direction
        self.x = x[direction][lane-1] if lane>0 else x[direction][0]
        self.y = y[direction][lane-1] if lane>0 else y[direction][0]
        self.crossed = 0
        vehicles[direction][lane-1].append(self)
        self.index = len(vehicles[direction][lane-1]) - 1
        path = os.path.join('images', direction, vehicleClass + '.png')
        try:
            self.image = pygame.image.load(path).convert_alpha()
        except:
            self.image = pygame.Surface((30,15))
            self.image.fill((200,0,0))
        self.originalImage = self.image
        if (len(vehicles[direction][lane-1]) > 1 and 
            getattr(vehicles[direction][lane-1][self.index-1], 'crossed', 0) == 0):
            prev = vehicles[direction][lane-1][self.index-1]
            if direction == 'right':
                self.stop = prev.stop - prev.image.get_rect().width - stoppingGap
            elif direction == 'left':
                self.stop = prev.stop + prev.image.get_rect().width + stoppingGap
            elif direction == 'down':
                self.stop = prev.stop - prev.image.get_rect().height - stoppingGap
            elif direction == 'up':
                self.stop = prev.stop + prev.image.get_rect().height + stoppingGap
        else:
            self.stop = defaultStop[direction]
        if direction == 'right':
            temp = self.image.get_rect().width + stoppingGap
            x[direction][lane-1] -= temp
        elif direction == 'left':
            temp = self.image.get_rect().width + stoppingGap
            x[direction][lane-1] += temp
        elif direction == 'down':
            temp = self.image.get_rect().height + stoppingGap
            y[direction][lane-1] -= temp
        elif direction == 'up':
            temp = self.image.get_rect().height + stoppingGap
            y[direction][lane-1] += temp
        simulation.add(self)

    def render(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def move(self):
        global currentGreen, currentYellow
        dirn = self.direction
        rect = self.image.get_rect()
        if dirn == 'right':
            if self.crossed==0 and self.x + rect.width > stopLines[dirn]:
                self.crossed = 1
            if ((self.x + rect.width <= self.stop) or self.crossed==1 or (currentGreen==0 and currentYellow==0)):
                if self.index==0 or (self.x + rect.width) < (vehicles[self.direction][self.lane-1][self.index-1].x - movingGap):
                    self.x += self.speed
        elif dirn == 'down':
            if self.crossed==0 and self.y + rect.height > stopLines[dirn]:
                self.crossed = 1
            if ((self.y + rect.height <= self.stop) or self.crossed==1 or (currentGreen==1 and currentYellow==0)):
                if self.index==0 or (self.y + rect.height) < (vehicles[self.direction][self.lane-1][self.index-1].y - movingGap):
                    self.y += self.speed
        elif dirn == 'left':
            if self.crossed==0 and self.x < stopLines[dirn]:
                self.crossed = 1
            if ((self.x >= self.stop) or self.crossed==1 or (currentGreen==2 and currentYellow==0)):
                if self.index==0 or self.x > (vehicles[self.direction][self.lane-1][self.index-1].x + vehicles[self.direction][self.lane-1][self.index-1].image.get_rect().width + movingGap):
                    self.x -= self.speed
        elif dirn == 'up':
            if self.crossed==0 and self.y < stopLines[dirn]:
                self.crossed = 1
            if ((self.y >= self.stop) or self.crossed==1 or (currentGreen==3 and currentYellow==0)):
                if self.index==0 or self.y > (vehicles[self.direction][self.lane-1][self.index-1].y + vehicles[self.direction][self.lane-1][self.index-1].image.get_rect().height + movingGap):
                    self.y -= self.speed

def initialize():
    ts1 = TrafficSignal(0, defaultYellow, shared_state['defaultGreen'][0])
    signals.append(ts1)
    ts2 = TrafficSignal(ts1.yellow + ts1.green, defaultYellow, shared_state['defaultGreen'][1])
    signals.append(ts2)
    ts3 = TrafficSignal(defaultRed, defaultYellow, shared_state['defaultGreen'][2])
    signals.append(ts3)
    ts4 = TrafficSignal(defaultRed, defaultYellow, shared_state['defaultGreen'][3])
    signals.append(ts4)
    repeat()

def updateValues():
    for i in range(0, noOfSignals):
        if i == currentGreen:
            if currentYellow == 0:
                signals[i].green -= 1
            else:
                signals[i].yellow -= 1
        else:
            signals[i].red -= 1

def generateVehicles():
    dist = [25,50,75,100]
    while True:
        vehicle_type = random.randint(0,3)
        lane_number = random.randint(1,3)
        temp = random.randint(0,99)
        if temp < dist[0]:
            direction_number = 0
        elif temp < dist[1]:
            direction_number = 1
        elif temp < dist[2]:
            direction_number = 2
        else:
            direction_number = 3
        Vehicle(lane_number, vehicleTypes[vehicle_type], direction_number, directionNumbers[direction_number])
        time.sleep(1)

def repeat():
    global currentGreen, currentYellow, nextGreen
    while True:
        signals[currentGreen].green = shared_state['defaultGreen'][currentGreen]
        while signals[currentGreen].green > 0:
            updateValues()
            time.sleep(1)
        currentYellow = 1
        for i in range(0,3):
            for vehicle in vehicles[directionNumbers[currentGreen]][i]:
                vehicle.stop = defaultStop[directionNumbers[currentGreen]]
        while signals[currentGreen].yellow > 0:
            updateValues()
            time.sleep(1)
        currentYellow = 0
        signals[currentGreen].green = shared_state['defaultGreen'][currentGreen]
        signals[currentGreen].yellow = defaultYellow
        signals[currentGreen].red = defaultRed
        currentGreen = nextGreen
        nextGreen = (currentGreen + 1) % noOfSignals
        signals[nextGreen].red = signals[currentGreen].yellow + signals[currentGreen].green

def main():
    thread1 = threading.Thread(name="initialization", target=initialize)
    thread1.daemon = True
    thread1.start()

    thread2 = threading.Thread(name="generateVehicles", target=generateVehicles)
    thread2.daemon = True
    thread2.start()

    if USE_AI:
        if 'defaultGreen' not in shared_state:
            shared_state['defaultGreen'] = defaultGreen
        start_controller(shared_state, control_interval=2.0, min_green=6, max_green=40, smoothing_alpha=0.7)
        print("[MAIN] AI controller started.")

    screenWidth = 1400
    screenHeight = 800
    screenSize = (screenWidth, screenHeight)
    background = None
    try:
        background = pygame.image.load('images/intersection_1.png').convert()
    except:
        background = pygame.Surface(screenSize)
        background.fill((34,139,34))
    screen = pygame.display.set_mode(screenSize)
    pygame.display.set_caption("AI Traffic Simulation")

    try:
        redSignal = pygame.image.load('images/signals/red.png').convert_alpha()
        yellowSignal = pygame.image.load('images/signals/yellow.png').convert_alpha()
        greenSignal = pygame.image.load('images/signals/green.png').convert_alpha()
    except:
        redSignal = pygame.Surface((40,60))
        redSignal.fill((150,0,0))
        yellowSignal = pygame.Surface((40,60))
        yellowSignal.fill((200,200,0))
        greenSignal = pygame.Surface((40,60))
        greenSignal.fill((0,150,0))
    font = pygame.font.Font(None, 30)

    clock = pygame.time.Clock()
    global currentGreen, currentYellow

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.blit(background, (0,0))

        for i in range(0, noOfSignals):
            if i == currentGreen:
                if currentYellow == 1:
                    signals[i].signalText = signals[i].yellow
                    screen.blit(yellowSignal, signalCoods[i])
                else:
                    signals[i].signalText = signals[i].green
                    screen.blit(greenSignal, signalCoods[i])
            else:
                if signals[i].red <= 10:
                    signals[i].signalText = signals[i].red
                else:
                    signals[i].signalText = "---"
                screen.blit(redSignal, signalCoods[i])

        for i in range(0, noOfSignals):
            txt = font.render(str(signals[i].signalText), True, (255,255,255), (0,0,0))
            screen.blit(txt, signalTimerCoods[i])

        for vehicle in list(simulation):
            screen.blit(vehicle.image, [vehicle.x, vehicle.y])
            vehicle.move()

        if USE_AI:
            gtext = "AI green times: " + str(shared_state['defaultGreen'])
            gtxt = font.render(gtext, True, (255,255,255))
            screen.blit(gtxt, (10, 10))

        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()