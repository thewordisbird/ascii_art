import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ascii-art-theW0rdisbird", 
    version="0.0.1",
    author="Justin Bird",
    author_email="justin.h.bird@gmail.com",
    description="Convert .jpg's or .png's to ascii art.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JustinHBird/microblog",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'Pillow'
    ]
)