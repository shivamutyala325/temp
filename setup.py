from setuptools import find_packages,setup


e_dot='-e .'
def fetch_reqirements(path='./requirements.txt'):
    
    with open(path) as f:
       requirements=f.read().splitlines()

    if e_dot in requirements:
        requirements.remove(e_dot)

    return requirements
    

setup(
    name='mlpipeline1',
    version='0.0.1',
    author='shiva',
    author_email='shivamutyala325@gmail.com',
    packages=find_packages(),
    install_requires=fetch_reqirements()

)