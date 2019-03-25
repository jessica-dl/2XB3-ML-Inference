from setuptools import setup, find_packages

setup(name='ml_inference',
      version='0.1',
      packages=find_packages(),
      description='ML Inference server for CS 2XB3',
      install_requires=[
          'flask',
          'numpy'
      ],
      zip_safe=False)
