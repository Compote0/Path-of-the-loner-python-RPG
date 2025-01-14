import pygame
from src.encounter import encounter

def start_game(screen, mode):
    if mode == "PVE":
        encounter(screen, mode="PVE")
    elif mode == "PVP":
        print("PVP not implemented yet.")
