import sys
from cx_Freeze import setup, Executable

setup(
    name = "Bubble Rush",
    version = "1.0",
    description = "Assignment 1, 09/09/2016",
    executables = [Executable("Main.py", base = "Win32GUI")])