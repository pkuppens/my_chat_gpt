from setuptools import find_packages, setup

setup(
    name="my_chat_gpt",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        "openai>=1.0.0",
        "PyGithub>=2.0.0",
        "python-dotenv>=1.0.0",
        "requests>=2.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=8.0.0",
            "pytest-mock>=3.0.0",
            "pytest-cov>=4.0.0",
        ],
    },
    python_requires=">=3.11",
)
