import pkg_resources

try:
    version = pkg_resources.get_distribution("pydub").version
    print("pydub version:", version)
except pkg_resources.DistributionNotFound:
    print("pydub is not installed")
