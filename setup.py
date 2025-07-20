from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="r2k-chateval",
    version="1.0.0",
    author="Rama Nagireddi",
    author_email="",
    description="Advanced Chatbot Evaluation Framework with multi-modal metric fusion and dynamic evaluation modes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/R2K-ChatEval",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Linguistic",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    keywords="chatbot evaluation nlp ai machine-learning metrics",
    project_urls={
        "Bug Reports": "https://github.com/your-username/R2K-ChatEval/issues",
        "Source": "https://github.com/your-username/R2K-ChatEval",
        "Documentation": "https://github.com/your-username/R2K-ChatEval/blob/main/README.md",
    },
)

