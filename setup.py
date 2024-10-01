from setuptools import find_packages, setup

import geonode_datacite


def read_file(path: str):
    with open(path, "r") as file:
        return file.read()


setup_requires = [
    "wheel",
]

setup(
    name="geonode-datacite",
    version=geonode_datacite.__version__,
    url=geonode_datacite.__url__,
    description=geonode_datacite.__doc__,
    long_description="A GeoNode 4.4+ app that generates DOIs https://datacite.org/create-dois/",
    long_description_content_type="text/markdown",
    author=geonode_datacite.__author__,
    author_email=geonode_datacite.__email__,
    platforms="any",
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django :: 4.2",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=["requests==2.31.0"],
)
