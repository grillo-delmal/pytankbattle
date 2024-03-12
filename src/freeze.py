from cx_Freeze import setup, Executable

build_exe_options = {
    "packages": ["pygame"]
}

setup(
    name="pyTankBattle",
    description="A multiplayer battle royale tank game using the pygame engine!",
    options={"build_exe": build_exe_options},
    executables=[Executable("pytankbattle.py", base="gui", target_name="pyTankBattle")],
)
