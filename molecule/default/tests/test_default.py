"""Module containing the tests for the default scenario."""

# Standard Python Libraries
import os

# Third-Party Libraries
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ["MOLECULE_INVENTORY_FILE"]
).get_hosts("all")


def test_packages(host):
    """Test that the appropriate packages were installed."""
    pkgs = None
    print()
    if (
        host.system_info.distribution == "debian"
        and host.system_info.codename == "stretch"
    ):
        pkgs = ["python-selinux", "python3-selinux"]
    elif (
        host.system_info.distribution == "debian"
        or host.system_info.distribution == "ubuntu"
        or host.system_info.distribution == "kali"
    ):
        pkgs = ["python3-selinux"]
    elif host.system_info.distribution == "fedora":
        pkgs = ["python3-libselinux"]
    elif host.system_info.distribution == "amzn":
        pkgs = ["libselinux-python"]
    else:
        # This is an unknown OS, so force the test to fail
        assert False

    for pkg in pkgs:
        assert host.package(pkg).is_installed
