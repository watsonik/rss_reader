"""
Allow users use the reader without python installation, just with CLI.
"""
from setuptools import setup, find_packages

setup(
    name='rss_reader',
    version='5.0',
    author='Ihar Sakun',
    author_email='watsonik@gmail.com',
    description='Pure Python command-line RSS reader',
    packages=find_packages(),
    install_requires=['feedparser==6.0.10', 'dateparser==1.1.1', 'dominate==2.7.0', 'xhtml2pdf==0.2.8',
                      'colored==1.4.3'],
    entry_points={
        'console_scripts': 'rss_reader = main_reader.rss_reader:main'
    }
)
