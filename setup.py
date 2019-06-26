#To install ROI-selector in the
# current environment, run:
#
#   > python setup.py install
import sys
from setuptools import setup
if sys.version_info < (2, 6) or (3, 0) <= sys.version_info < (3, 3):
    print('ROI-selevtor requires at least Python 2.6 or 3.3 to run.')
    sys.exit(1)

def get_requires():
    requires = ['numpy', 'opencv-python']
    if sys.version_info == (2, 6):
        requires += ['argparse']
    return requires
setup(
    name='ROI-selector',
    version='1.0.1',
    description="Tool for finding and extracting motion events in video files (e.g. security camera footage).",
    #long_description=open('package-info.rst').read(),
    author='KlucsikKP',
    author_email='klucsik.krisztian@gmail.com',
    #url='https://github.com/Breakthrough/DVR-Scan',
    license="BSD 2-Clause",
    keywords="video computer-vision analysis",
    install_requires=get_requires(),
    extras_require={
        #'GUI': ['gi'],
        #'VIDEOENC': ['moviepy']
    },
    packages=['roi_select'],
    #package_data={'': ['../LICENSE*', '../package-info.rst']},
    entry_points={"console_scripts": ["roi-select=roi_select:main"]},
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Environment :: Console :: Curses',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Multimedia :: Video',
        'Topic :: Multimedia :: Video :: Conversion',
        'Topic :: Multimedia :: Video :: Non-Linear Editor',
        'Topic :: Utilities'
    ]
)
