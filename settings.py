import pygame
from pathlib import Path


pygame.init()

WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
display = pygame.Surface((screen.width, screen.height)) 
pygame.display.set_caption("Bob The Destroyer")
R = 3


def imgload(*path, columns=1, rows=1, scale=R):
    image = pygame.transform.scale_by(
        pygame.image.load(Path(*path)).convert_alpha(), scale
    )
     
    if columns * rows == 1: 
        return image
    else:
        frame_width = image.get_width() / columns
        frame_height = image.get_height() / rows

    ret = []
    if columns > 1 and rows == 1:  # if image is divided into columns
        for i in range(columns):
            sub = image.subsurface(
                i * frame_width,
                0,
                frame_width,
                frame_height,
            )
            ret.append(sub)

    elif rows > 1 and columns == 1:  # if image is divided into rows
        for i in range(rows):
            sub = image.subsurface(
                0,
                i * frame_height,
                frame_width,
                frame_height,
            )
            ret.append(sub)

    elif columns > 1 and rows > 1:  # if image is divided two-dimensinally
        ret = []
        for i in range(rows):
            row = image.subsurface(
                0, i * frame_height, image.get_width(), frame_height
            )
            row_sheet = []
            for j in range(columns):
                frame = row.subsurface(
                    j * frame_width,
                    0,
                    frame_width,
                    frame_height,
                )
                row_sheet.append(frame)

            ret.append(row_sheet)

    return ret
    