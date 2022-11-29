import os
import os.path

from setuptools import find_packages, setup

classifiers = [
    "Development Status :: 2 - Pre-Alpha",
    "Intended Audience :: Developers",
    "Intended Audience :: Science/Research",
    "License :: OSI Approved :: BSD License",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Topic :: Scientific/Engineering",
    "Topic :: Software Development",
]


def run_setup():
    """Get version from git, then install."""
    # load long description from README.md
    readme_file = "README.md"
    if os.path.exists(readme_file):
        long_description = open(readme_file, encoding="utf-8", errors="ignore").read()
    else:
        print("Could not find readme file to extract long_description.")
        long_description = ""
    setup(
        name="qualisys_udp",
        version="1.0.0",
        install_requires=[
            "qtm",
            "numpy",
        ],
        author="Ocean Perception - University of Southampton",
        author_email="miquel.massot-campos@soton.ac.uk",
        description="UDP broadcast server for qualisys with variable rate and added noise",  # noqa
        long_description=long_description,
        url="https://github.com/ocean-perception/qualisys_udp",
        packages=find_packages(where="src"),
        package_dir={"": "src"},
        classifiers=classifiers,
        license="BSD",
        entry_points={  # Optional
            "console_scripts": [
                "qualisys_udp = qualisys_udp.cli:main",
            ],
        },
    )


if __name__ == "__main__":
    run_setup()
