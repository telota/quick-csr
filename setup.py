from setuptools import find_packages, setup
import sys


if sys.version_info < (3, 5):
    raise RuntimeError('Requires at least Python 3.5.')


setup(
    name="quick_csr",
    author="Frank Sachsenheim",
    author_email="funkyfuture@riseup.net",
    packages=find_packages(exclude=["tests"]),
    install_requires=['pyopenssl'],
    entry_points={
        "console_scripts": ("quick-csr = quick_csr.cli:main",),
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Environment :: MacOS X',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Natural Language :: English',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Topic :: Security :: Cryptography'
    ]
)
