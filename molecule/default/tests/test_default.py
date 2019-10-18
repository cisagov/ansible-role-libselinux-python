"""Module containing the tests for the default scenario."""

import os
import pytest

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ["MOLECULE_INVENTORY_FILE"]
).get_hosts("all")


@pytest.mark.parametrize(
    "pkg,fedora_pkg", [("libselinux-python", "python2-libselinux")]
)
def test_packages(host, pkg, fedora_pkg):
    """Test that the appropriate packages were installed."""
    if host.system_info.distribution == "fedora":
        assert host.package(fedora_pkg).is_installed
    else:
        assert host.package(pkg).is_installed
