import os
import shutil

for root, dirs, files in os.walk("./PL1DUmT", topdown=False):
    for name in files:
        if name.__contains__("Java Programming for Beginners"):
            shutil.move('PL1DUmT/'+name, 'Intro/'+name)
        else:
            shutil.move('PL1DUmT/'+name, 'OOP/'+name)