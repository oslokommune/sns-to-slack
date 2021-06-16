from setuptools import setup, find_packages

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="sns-to-slack",
    version="0.1.0",
    author="Origo Dataplattform",
    author_email="dataplattform@oslo.kommune.no",
    description="Sends messages and alerts to Slack",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/oslokommune/sns-to-slack",
    packages=find_packages(),
    install_requires=["prison", "requests"],
)
