from setuptools import setup, find_packages
 
 
 
setup(name='toobuk',
      version='0.0.2',
      url='https://github.com/ramoi/toobuk',
      license='MIT',
      author='이민기',
      author_email='ramoi@daum.net',
      description='웹크롤링을 도와줍니다.',
      packages=find_packages(exclude=['test','statist']),
      long_description=open('README.md', 'rt', encoding='UTF8').read(),
      zip_safe=False,
      setup_requires=['beautifulsoup4 >= 4.0.0'] )