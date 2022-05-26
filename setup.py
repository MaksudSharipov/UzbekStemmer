import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="UzbekStemmer",
    version="0.2.6",
    author="Maksud Sharipov, Ulugbek Salaev, Ollabergan Yuldashev, Jasur Sobirov",
    author_email="maqsbek72@gmail.com, ulugbek0302@gmail.com, ollaberganyuldashov@gmail.com",
    description="Uzbek Stemmer for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data = True,
    url="https://github.com/MaksudSharipov/UzbekStemmer",
    project_urls={
        "Bug Tracker": "https://github.com/MaksudSharipov/UzbekStemmer",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.9",
    install_requires=[
        "nltk",
        "lxml",
    ]
)
