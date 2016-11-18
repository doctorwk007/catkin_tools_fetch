import os
import sys
from stat import ST_MODE
from distutils import log
from setuptools import setup
from setuptools.command.install import install

# Setup installation dependencies
install_requires = [
    'catkin-pkg > 0.2.9',
    'catkin_tools >= 0.4.2',
    'setuptools',
]
if sys.version_info[0] == 2 and sys.version_info[1] <= 6:
    install_requires.append('argparse')

# Figure out the resources that need to be installed
this_dir = os.path.abspath(os.path.dirname(__file__))
osx_resources_path = os.path.join(
    this_dir,
    'catkin_tools',
    'notifications',
    'resources',
    'osx',
    'catkin build.app')


class PermissiveInstall(install):
    def run(self):
        install.run(self)
        if os.name == 'posix':
            for file in self.get_outputs():
                # all installed files should be readable for anybody
                mode = ((os.stat(file)[ST_MODE]) | 0o444) & 0o7777
                log.info("changing permissions of %s to %o" % (file, mode))
                os.chmod(file, mode)

version_str = '0.0.1'
github_url = 'https://github.com/niosus/catkin_tools_fetch'

setup(
    name='catkin_tools_fetch',
    packages=['catkin_tools_fetch'],
    version=version_str,
    install_requires=install_requires,
    author='Igor Bogoslavskyi',
    author_email='igor.bogoslavskyi@uni-bonn.de',
    maintainer='Igor Bogoslavskyi',
    maintainer_email='igor.bogoslavskyi@uni-bonn.de',
    keywords=['catkin', 'catkin_tools'],
    license="BSD",
    url=github_url,
    download_url=github_url + '/tarball/' + version_str,
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
    ],
    description="A new verb 'fetch' for catkin_tools",
    long_description="""
Provides a new verb 'fetch' for catkin_tools. Allows fetching dependencies of
the packages found inside the catkin workspace.
""",
    test_suite='tests',
    entry_points={
        'catkin_tools_fetch.commands.catkin.verbs': [
            'fetch = catkin_tools_fetch:description',
        ],
    },
    cmdclass={'install': PermissiveInstall},
)
