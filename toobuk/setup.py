rom setuptools import setup, find_packages
 
 
 
setup(name='toobuk',
      version='0.1',
      url='https://github.com/ramoi/toobuk',
      license='MIT',
      author='ramoi',
      author_email='ramoi@daum.net',
      description='웹크롤링을 도와줍니다.',
      packages=find_packages(exclude=['tests']),
      long_description=open('README.md').read(),
      zip_safe=False,
      setup_requires=['beautifulsoup4'],
      test_suite='nose.collector')