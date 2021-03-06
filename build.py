from pybuilder.core import use_plugin, init, Author

use_plugin("python.install_dependencies")
use_plugin("python.core")
use_plugin("python.unittest")
use_plugin("python.distutils")
use_plugin('copy_resources')
#use_plugin("python.coverage")

authors = [Author('Marco Hoyer', 'marco.hoyer@immobilienscout24.de')]
description = """Make squid a dynamic proxy by gathering auth information and acl from dynamodb
"""

name = 'squid-aws'
license = 'GNU GPL v3'
summary = 'squid-aws'
url = 'https://github.com/marco-hoyer/squid-aws
version = '0.1'

default_task = ['publish']

@init
def initialize(project):

    project.build_depends_on("mock")
    project.depends_on("boto")
    project.depends_on("unittest2")

    project.set_property('copy_resources_target', '$dir_dist')
    project.get_property('copy_resources_glob').append('setup.cfg')
    project.set_property('dir_dist_scripts', 'scripts')

@init(environments='teamcity')
def set_properties_for_teamcity_builds(project):
    import os
    project.set_property('teamcity_output', True)
    project.version = '%s-%s' % (project.version, os.environ.get('BUILD_NUMBER', 0))
    project.default_task = ['clean', 'install_build_dependencies', 'publish']
    project.set_property('install_dependencies_index_url', os.environ.get('PYPIPROXY_URL'))
    project.set_property('install_dependencies_use_mirrors', False)
    project.rpm_release = os.environ.get('RPM_RELEASE', 0)
