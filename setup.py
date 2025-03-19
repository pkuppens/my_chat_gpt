from setuptools import find_packages, setup


def read_requirements(filename):
    with open(filename) as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]


setup(
    name="my_chat_gpt",
    version="0.1.1",
    packages=find_packages(),
    install_requires=read_requirements("requirements-base.txt"),
    extras_require={
        "dev": read_requirements("requirements-dev.txt"),
        "proxy": read_requirements("requirements-proxy.txt"),
    },
    python_requires=">=3.11",
)
