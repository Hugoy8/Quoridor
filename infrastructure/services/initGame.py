from infrastructure.database.config import Database
from domain.launcher.launchScreen import LaunchScreen
from infrastructure.services.board import Board
from PIL import Image, ImageTk
import os
from tkinter import Tk

class InitGame:
    def __init__(self, board : Board, launcherScreen : LaunchScreen) -> None:
        self.board = board
        self.launchScreen = launcherScreen