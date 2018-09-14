import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="adaptive-discretization",
    version="0.0.1",
    author="jimkon",
    author_email="kontzedakis_93@hotmail.com",
    description="A small package for adaptive discretization using trees",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jimkon/adaptive_discretization",
    packages=['adaptive-discretization']
    package_dir={'adaptive_discretization': 'adaptive_discretization'},
)
