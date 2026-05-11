# Space invaders

<p align="center">
  <img src="assets/banner.png" alt="Space Invaders Banner" width="800"/>
</p>

## About
This project is a clone of the classic game space invaders designed by [Tomohiro Nishikado](https://en.wikipedia.org/wiki/Tomohiro_Nishikado) and developed by Taito company.
It is built with **python** and **pygame**, using **modular software architecture** and **object-orientated-design**.
The goal of this project is to demonstrate my ability to design and implement software systems.

### Game Description:
An alien fleet is coming. The player controlls the last defence turret and must destroy the aggressors before they reach Earth. Each wave becomes more dangerous the closer it comes to Earth, needing timing and precision to survive. 

## Install
Installation steps:
1. Install python
2. Download or clone the project
3. navigate to the project direcotry
4. setup python virtual environment, venv
5. activate the venv
6. install pygame-ce with pip

Navigate to the project dir:
``` sh
cd <Project dir> # replace <Project dir> with the full directory path in which the project is
python -m venv <dir> # replace <dir> with the desired venv direcory name
```

Linux venv activation:
``` sh
source <dir>/bin/activate # activates the venv
```

Windows  venv activation:
``` sh
source <dir>/scripts/activate # activates the venv
```

Install pygame-ce:
``` sh
python -m pip install pygame-ce # install pygame from Pypi
```

## How to play:
To run the game, navigate to the project directory, activate the venv and execute this command:
``` sh
python main.py
```

