from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    long_description = readme_file.read()

setup(
    name="minesweeper-py",
    version="1.0.0",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Ilya Kalinin",
    author_email="gerrux@yandex.ru",
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: END USERS/DESKTOP",
        "License :: OSI Approved :: MIT License",
    ],
    keywords="minesweeper game pygame",
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        "console_scripts": ["minesweeper=minesweeper:__main__"],
    },
    setup_requires=["pygame~=2.1.2"],
)