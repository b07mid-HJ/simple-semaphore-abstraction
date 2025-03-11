from setuptools import setup, find_packages

setup(
    name="simple-semaphore-abstraction",
    version="0.1.2",
    packages=find_packages(),
    description="A simple abstraction library for semaphores in Python",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author="Ahmed Hajjem",
    author_email="ahmed.hajjem@etudiant-isi.utm.tn",
    url="https://github.com/b07mid-HJ/",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)