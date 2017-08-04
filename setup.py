from setuptools import setup

setup(
    name='proxypool',
    version='V2.0.0',
    packages=['proxypool', 'proxypool.schedule'],
    url='https://github.com/WiseDoge/ProxyPool',
    license='apache 2.0',
    author='wisedoge',
    author_email='wisedoge@outlook.com',
    description='A Cross-platform proxy pool.',
    py_modules=['run'],
    include_package_data=True,
    platforms='any',
    install_requires=[
        'aiohttp',
        'requests',
        'bs4',
        'flask',
        'redis',
        'lxml'
    ],
    entry_points={
        'console_scripts': ['proxypool_run=run:cli']
    },
    classifiers=[
        'Environment :: Console',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython'
    ]
)
