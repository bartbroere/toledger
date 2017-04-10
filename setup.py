from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name='ToLedger',
    version='1.0',
    description='Convert bank statements to Ledger',
    long_description=readme(),
    keywords=["ledger", "convert", "conversion", "bank", "ing", "nl", "accounting", "command", "commandline", "cli"],
    packages=['toledger'],
    url='https://github.com/bartbroere/toledger/',
    license='MIT',
    author='Bart Broere',
    author_email='mail@bartbroere.eu',
    install_requires=['docopt'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Office/Business :: Financial',
        'Topic :: Utilities',
    ],
)
