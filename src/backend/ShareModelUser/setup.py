from setuptools import setup, find_packages

setup(
    name="UserModel",
    version="0.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        # Dependencias de tu paquete
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
