import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="UzbekStemmer",
    version="0.2.0",
    author="Maksud Sharipov, Ulugbek Salaev, Allabergan Yuldashev, Jasur Sobirov",
    author_email="ulugbek0302@gmail.com",
    description="Uzbek Stemmer for Python",
    long_description="The Uzbek stemming algorithm was created by [Maksud Sharipov, Ulugbek Salaev, Allabergan Yuldashev, Jasur Sobirov]. It stems all Uzbek words and it is not included any lexicon.",
    long_description_content_type="Uzbek Stemmer for Python",
    url="https://github.com/UlugbekSalaev/UzbekStemmer",
    project_urls={
        "Bug Tracker": "https://github.com/UlugbekSalaev/UzbekStemmer",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)