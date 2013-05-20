# -*- encoding=utf-8
from setuptools import setup, find_packages
from pkg_resources import require, DistributionNotFound
import sys
import os
src_dir = os.path.dirname(os.path.abspath(__file__)) + "/src"
sys.path.append(src_dir)
import money


def local_open(fname):
    return open(os.path.join(os.path.dirname(__file__), fname))

requirements = local_open('requirements.txt')
# Build the list of dependency to install
required_to_install = []
for dist in requirements.readlines():
    dist = dist.strip()
    try:
        require(dist)
    except DistributionNotFound:
        required_to_install.append(dist)

package_name = 'money'
url_schema = 'http://pypi.python.org/packages/source/d/%s/%s-%s.tar.gz'
download_url = url_schema % (package_name, package_name, money.__version__)
setup(
    name='money.py',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    version=money.__version__,
    description=money.__doc__,
    author=money.__author__,
    author_email=money.__contact__,
    url=money.__homepage__,
    license=money.__license__,
    download_url=download_url,
    long_description=local_open('README.md').read(),
    keywords=["money", "currency", "business",
              "cash", "enterprise", "e-commerce"],
    install_requires=required_to_install,
    include_package_data=True,
    classifiers=['Development Status :: 3 - Alpha',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: BSD License',
                 'Operating System :: MacOS :: MacOS X',
                 'Operating System :: OS Independent',
                 'Operating System :: POSIX',
                 'Operating System :: Unix',
                 'Programming Language :: Python',
                 'Programming Language :: Python :: 3.2',
                 'Programming Language :: Python :: 3.3',
                 'Topic :: Office/Business :: Financial',
                 'Topic :: Software Development :: Libraries :: Python Modules', ],
)
