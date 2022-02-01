"""setup.py file."""

from setuptools import setup, find_packages
import re


with open("requirements.txt", "r") as fs:
    reqs = [r for r in fs.read().splitlines() if (
        len(r) > 0 and not r.startswith("#"))]

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

__author__ = "Eric Wu <vip@xdai.vip>"

# get version without importing
with open("napalm_h3c_comware/__init__.py", "r") as f:
    VERSION = str(re.search('__version__ = "(.+?)"', f.read()).group(1))


setup(
    name="napalm-h3c-comware",
    version=VERSION,
    author="Eric Wu",
    author_email="vip@xdai.vip",
    description="NAPALM driver for H3C Comware V7 network devices, over ssh.",
    license="Apache 2.0",
    long_description_content_type="text/markdown",
    long_description=long_description,
    url="https://github.com/napalm-automation-community/napalm-h3c-cw7-ssh/",
    project_urls={
        "Bug Tracker": "https://github.com/napalm-automation-community/napalm-h3c-cw7-ssh/issues",
    },
    classifiers=[
        "Topic :: Utilities",
        "License :: OSI Approved :: Apache Software License",
        "Development Status :: 4 - Beta",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
    ],
    packages=find_packages(exclude=("test*", "*demo.py")),
    include_package_data=True,  # declarations in MANIFEST.in
    install_requires=reqs,
)
