from setuptools import setup, find_packages

setup(name='traylert',
      version='0.1',
      description='A very simple server monitoring tool.',
      url='https://github.com/IngoKl/Traylert',
      author='Ingo Kleiber',
      author_email='ingo@kleiber.me',
      license='MIT',
      install_requires=[
        'infi.systray',
        'win10toast',
        'flask',
        'pycryptodomex',
        'jsonpickle',
        'click'
      ],
      packages=find_packages(),
      include_package_data=True,
      entry_points={
          'console_scripts': [
              'Traylert = traylert.traylert_client:main'
          ]
      },
      zip_safe=False
)