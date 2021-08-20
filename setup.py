from setuptools import setup, find_packages

setup(
    name='oanda-broker-cli',
    version='0.0.1',
    packages=find_packages('src/app'),
    package_dir={'': 'src/app'},
    entry_points= {
        'console_scripts': [
            'ob-accounts = account:main',
            'ob-instruments = instrument:main',
            'ob-trades = trade:main'
        ]
    })

