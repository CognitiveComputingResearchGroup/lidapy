from setuptools import setup, find_packages


setup(
    name="source",
    version="0.1.4",
    packages=find_packages(include=["source*"]),  # Explicitly include only your package
    exclude_package_data={"": ["Tests", "Configs"]},  # Exclude directories
    install_requires=[
        "requests",
    ],
    entry_points={
        'console_scripts': [
            'LIDAPY-cli=LIDAPY.cli:main',  # Define CLI entry point
        ],
    },
    author="Brian W Karimi, Katie Killian, Nicole Vadillo",
    description="A Python package for a cognitive modeling software, "
                "LIDA Framework, developed by the Cognitive Computing "
                "Research Group (“CCRG”) originally in java"
)