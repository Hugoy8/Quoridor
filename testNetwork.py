import pkg_resources

try:
    version = pkg_resources.get_distribution("threading").version
    print(f"Threading version: {version}")
except pkg_resources.DistributionNotFound:
    print("Threading is not installed.")