from setuptools import setup
from setuptools.command.install import install


class PostInstallCommand(install):
    def run(self):
        """
        Run installer and post install if required
        """
        super().do_egg_install()


setup(name='2-measure.it',
      version='0.0',
      description='2-measure.it',
      author='Bogdan Irinel, Pricop Mihai',
      author_email='mihai@falcontrading.ro',
      url='falcontrading.ro',
      cmdclass={'install': PostInstallCommand},
      install_requires=[
          'numpy',
          'rubik==0.3',
          'opencv-python',
          'pillow',
          'pdf2image',
      ],
      dependency_links=['http://git.falcon.zone/falcon/rubik/-/archive/master/rubik-master.tar.gz#egg=rubik-0.3'],
      )
