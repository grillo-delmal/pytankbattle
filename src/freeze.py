from cx_Freeze import setup, Executable
import setuptools_git_versioning

__version__ = str(setuptools_git_versioning.get_version(root=".."))

with open('VERSION', 'w') as version_file:
    version_file.write(__version__)

build_exe_options = {
    "packages": ["pygame"],
    "include_files": ["VERSION"]
}

setup(
    name="pyTankBattle",
    version=__version__,
    description="A multiplayer battle royale tank game using the pygame engine!",
    options={"build_exe": build_exe_options},
    executables=[Executable("pytankbattle.py", base="gui", target_name="pyTankBattle")],
)
