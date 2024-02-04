from setuptools import setup, find_packages

setup(
    name='Whisker_Plot',
    version='0.1.0',
    author='Utkarsh Kumar',
    author_email='kumarutkarsh641@gmail.com',
    description='A utility for chain analysis and generating whisker plots.',
    packages=find_packages(),
    install_requires=[
        'getdist',
        'natsort',
        # Add other dependencies as needed
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)