from setuptools import setup

try:
    __long_description__ = open('README.rst').read()
except:
    __long_description__ = ''

setup(
    name='flexidate',
    version=1.0,
    license='MIT',
    description='Very flexible date parsing and normalization utilities',
    long_description=__long_description__,
    author='Akirato, Open Knowledge Foundation',
    author_email='info@okfn.org,nurendrachoudhary31@gmail.com',
    url='http://github.com/Akirato/flexidate_python3/',
    install_requires=[
        # python-dateutil 2.0 has different _parse method, so stick to 1.4.1
        'python-dateutil',
        ],
    packages=['flexidate'],
    zip_safe=False,
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)
