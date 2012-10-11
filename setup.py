from setuptools import setup, find_packages

__long_description__ = open('README.rst').read()

setup(
    name='datautil',
    version=1.0,
    license='MIT',
    description='Very flexible date parsing and normalization utilities',
    long_description=__long_description__,
    author='Open Knowledge Foundation',
    author_email='info@okfn.org',
    url='http://github.com/okfn/flexidate/',
    install_requires=[
        # python-dateutil 2.0 has different _parse method, so stick to 1.4.1
        'python-dateutil>=1.0,<1.99',
        ],
    py_modules=['flexidate.py'],
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
