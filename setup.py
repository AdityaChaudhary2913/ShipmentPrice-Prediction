# This file help us to build a particular project as a package
# This file is used to install the package in the system
# This file is used to install the dependencies of the project
# Module is a simple .py file
# Package is a directory which contains multiple modules with __init__.py file
# Library is a collection of packages
# We can use setup.py file also for trigerring requirements.txt, execute "python3 setup.py install"
# If we want to trigger setup.py from requirements.txt, execute "pip3 install -r requirements.txt"
# Artifacts stores the output of ML pipeline

from setuptools import find_packages,setup
from typing import List

HYPEN_E_DOT='-e.'

def get_requirements(file_path:str)->List[str]:
    requirements=[]
    with open(file_path) as file_obj:
        requirements=file_obj.readlines()
        requirements=[req.replace("\n","") for req in requirements]
    
    if HYPEN_E_DOT in requirements:
        requirements.remove(HYPEN_E_DOT)
    return requirements


setup(
    name='Shipment Price Prediction',
    version='0.0.1',
    author='AdityaChaudhary2913',
    author_mail='adityachaudhary1306@gmail.com',
    install_requirements=[],
    packages=find_packages() 
)