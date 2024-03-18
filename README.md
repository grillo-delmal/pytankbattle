# PyTankBattle

Multiplayer battle royale tank game that uses the pygame engine.

This is a port of the [Tanks](https://wiibrew.org/wiki/Tanks) game published in the Wii Homebrew Channel.

## How to use

### Run with python

First, remember to install the requirements

```sh
pip install -r requirements.txt
```

Then, you can run this code in your computer by running the `pytankbattle.py` script in the `src` Folder.

```sh
cd src
python pytankbattle.py
```

### Install using PIP

This requires the pygame library. To build and install run the following command:

```sh
pip install .
```

Then you can run the game by calling it on the terminal

```sh
pytankbattle
```

### Generate cx_Freeze binary release

If you want to generate a binary release (usable in Windows and Mac with a little fidling), you can use the following command :D

```sh
pip install --upgrade --pre --extra-index-url https://marcelotduarte.github.io/packages/ setuptools_git_versioning cx_Freeze
pip install -r requirements.txt

cd src
python freeze.py build_exe
```

## Wishlist

* Make maps and obstacles.
* Improve Mouse abstraction
* UI to customize consts.py
* Network play
