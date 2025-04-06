from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="speech2clipboard",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A tool to transcribe Hungarian speech to text and copy it to the clipboard",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/speech2clipboard",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "transformers>=4.26.0",
        "torch>=1.13.0",
        "sounddevice>=0.4.5",
        "numpy>=1.22.0",
        "pyperclip>=1.8.2",
        "PyQt5>=5.15.7",
        "librosa>=0.9.2",
        "python-dotenv>=0.21.0",
        "scipy>=1.9.0",
    ],
    entry_points={
        "console_scripts": [
            "speech2clipboard=src.main:main",
        ],
    },
) 