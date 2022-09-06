from setuptools import setup, find_packages

setup(
    name='rss_reader',
    version='1.0',
    author='Ihar Sakun',
    author_email='watsonik@gmail.com',
    description='Pure Python command-line RSS reader',
    packages=find_packages(),
    install_requires=['feedparser==6.0.10', 'dateparser==1.1.1'],
    entry_points={
        'console_scripts': 'rss-reader = main_reader.rss_reader:main'
    }
)
