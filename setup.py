from distutils.core import setup

short_description = "I'm just a dumdum."

long_description = \
"""
dumdum dumdum dumdum dumdum dumdum dumdum dumdum dumdum dumdum
dumdum dumdum dumdum dumdum dumdum dumdum dumdum dumdum dumdum
dumdum dumdum dumdum dumdum dumdum dumdum dumdum dumdum dumdum
dumdum dumdum dumdum dumdum dumdum dumdum dumdum dumdum dumdum
dumdum dumdum dumdum dumdum dumdum dumdum dumdum dumdum dumdum
dumdum dumdum dumdum dumdum dumdum dumdum dumdum dumdum dumdum
dumdum dumdum dumdum dumdum dumdum dumdum dumdum dumdum dumdum
dumdum dumdum dumdum dumdum dumdum dumdum dumdum dumdum dumdum
"""

classifiers = ['Development Status :: 1 - Planning',
               'License :: OSI Approved :: MIT License',
               'Operating System :: OS Independent',
               'Intended Audience :: Science/Research',
               'Topic :: Scientific/Engineering :: Visualization',
               'Topic :: Scientific/Engineering :: Physics',
               'Topic :: Scientific/Engineering :: Mathematics',
               'Topic :: Scientific/Engineering :: Information Analysis',
               'Programming Language :: Python',
               'Programming Language :: Python :: 2',
               'Programming Language :: Python :: 2.7',
               'Programming Language :: Python :: 3',
               'Programming Language :: Python :: 3.4',
               'Programming Language :: Python :: 3.5',
               'Programming Language :: Python :: 3.6']

with open('requirements.txt') as f:
    requirements_lines = f.readlines()
install_requires = [r.strip() for r in requirements_lines]

# now call setup
setup(name='dummy',
      version='1.0.0',
      description=short_description,
      long_description=long_description,
      classifiers=classifiers,
      url='https://github.com/dumdum/dummy',
      author='Dum Master',
      author_email='dumdum@gmail.com',
      license='MIT',
      platforms='any',
      packages=['dummy'],
      install_requires=install_requires)
