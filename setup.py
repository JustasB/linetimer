import setuptools

with open("Readme.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="linetimer",
    version="0.1.2",
    author="Justas Birgiolas",
    author_email="justas@asu.edu",
    description="A small Python class to quickly measure the time taken while executing a block of indented lines",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/justasb/linetimer",
    packages=setuptools.find_packages(),
    include_package_data = True,
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
