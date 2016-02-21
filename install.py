#!/usr/bin/env python


# Mostly copied from wg-buildfarm by Tully Foote

from optparse import OptionParser
import sys
import subprocess
import platform

def run_cmd(cmd, quiet=True, extra_args=None, feed=None):
    args = {'shell': True}
    if quiet:
        args['stderr'] = args['stdout'] = subprocess.PIPE
    if feed is not None:
        args['stdin'] = subprocess.PIPE
    if extra_args is not None:
        args.update(extra_args)
    p = subprocess.Popen(cmd, **args)
    if feed is not None:
        p.communicate(feed)
    return p.wait()

def get_ubuntu_version():
    return platform.dist()[2]

def is_ubuntu():
    return platform.dist()[0] == 'Ubuntu'

def configure_puppet():
    """
    Configure puppet in the system slave
     - Install puppet and git
     - donwload repo
     - run puppet
    """

    # do stuff with slave
    # first, install puppet
    print "updating apt"
    if run_cmd('apt-get update'):
        return False

    print "installing puppet and stdlib module"
    # No module package in precise
    # Deprecated package in pre
    if get_ubuntu_version() == 'precise':
        if run_cmd('wget https://apt.puppetlabs.com/puppetlabs-release-precise.deb'):
            return False
        if run_cmd('sudo dpkg -i puppetlabs-release-precise.deb'):
            return False
        if run_cmd('sudo apt-get install -y puppet'):
            return False
        if run_cmd('sudo puppet module install puppetlabs-stdlib'):
            return False
    else:
        if run_cmd('apt-get install -y puppet puppet-module-puppetlabs-stdlib'):
            return False

    print "stopping puppet"
    # stop puppet
    if run_cmd('service puppet stop'):
        return False

    print "Clearing /etc/puppet"
    if run_cmd('rm -rf /etc/puppet'):
        return False

    print "cloning puppet repo"
    if run_cmd('git clone https://github.com/j-rivero/osrf_puppet_jenkins.git  /etc/puppet'):
        return False

    print "running puppet apply site.pp"
    if run_cmd('puppet apply /etc/puppet/manifests/site.pp', quiet=False):
        return False
 
    return True


parser = OptionParser()

if not is_ubuntu():
    print("Not ubuntu systems are not supported")
    sys.exit(-1)

configure_puppet()
