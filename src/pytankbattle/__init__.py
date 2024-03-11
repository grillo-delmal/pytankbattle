# Copyright (c) 2023, Grillo del Mal
# 
# Distributed under the 2-Clause BSD License, see LICENSE file.

from .pytankbattle import PyTankBattle

def main():
    game = PyTankBattle()
    game.run()

if __name__ == "__main__":
    main()