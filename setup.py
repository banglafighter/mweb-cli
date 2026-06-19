from setuptools import setup, find_packages
import os
import pathlib

CURRENT_DIR = pathlib.Path(__file__).parent
README = (CURRENT_DIR / "README.md").read_text()

env = os.environ.get('source')


def get_dependencies():
    dependency = [
        "GitPython==3.1.50"
    ]

    if env and env == "code":
        return dependency

    return dependency + ["mw-common", "mw-file-content"]


setup(
    name='mweb-cli',
    version='0.0.1',
    url='https://github.com/banglafighter/mweb-cli',
    license='Apache 2.0',
    author='Bangla Fighter',
    author_email='banglafighter.com@gmail.com',
    description='Command line interface tools for MWeb application, which make MWeb work easy and automatic from terminal or CMD.',
    long_description=README,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=get_dependencies(),
    py_modules=["mweb_cli_bsw"],
    entry_points={'console_scripts': ['mwebcli=mweb_cli.cli.mweb_cli_bsw:bsw']},
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
    ]
)
