from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='CommandCoinS',
    version='0.0.1',
    description='Personal finance tracker',
    long_description=readme,
    author='Starlinetor',
    author_email='eaccontent@gmail.com',
    url='https://github.com/starlinetor/CommandCoinS',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    install_requires=[
        'click',
    ],
    entry_points={
        'console_scripts': [
            'CommandCoinS=CommandCoinS.main:main',  # Adjust based on your actual structure
        ],
    },
    python_requires='>=3.6',
)
