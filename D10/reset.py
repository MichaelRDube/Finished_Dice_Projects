import shutil
import os
import subprocess
import sys
import platform

if not os.path.exists('processed_images'):
    print('No directory \'processed_images\'.  Making now.')
    os.mkdir('processed_images')
if not os.path.exists('captured_images'):
    print('No directory \'captured_images\'.  Making now.')
    os.mkdir('captured_images')

for file in os.listdir('./processed_images'):
    shutil.move(os.path.join('./processed_images', file), './captured_images') 


if os.path.exists('__pycache__'):
    shutil.rmtree('__pycache__')

if os.path.exists('dice.db'):
    os.remove('dice.db')

python_cmd = "python3" if platform.system() != "Windows" else "python"
try:
    subprocess.run([python_cmd, 'dbSetup.py'], check=True)
except subprocess.CalledProcessError as e:
    print(f"An error occurred while running the script: {e}")
except FileNotFoundError:
    print(f"Could not find the Python interpreter '{python_cmd}'. Please check your Python installation.")
