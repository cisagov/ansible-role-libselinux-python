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
    if host.system_info.distribution in ["debian", "ubuntu", "kali"]:
        pkgs = ["python3-selinux"]
    elif host.system_info.distribution in ["amzn", "fedora"]:
        pkgs = ["python3-libselinux"]
    else:
        # This is an unknown OS, so force the test to fail
        raise ValueError(f"Unknown distribution {host.system_info.distribution}")

    for pkg in pkgs:
        assert host.package(pkg).is_installed
