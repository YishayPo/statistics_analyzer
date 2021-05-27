import subprocess
import sys

import pkg_resources


class ModulesImports():
    def __init__(self, packages_list):
        self.__required_packages_list = packages_list

    def install(self, package):
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        except ImportError:
            raise RuntimeError

    def install_list(self):
        try:
            installed_packages_list = {pkg.key for pkg in pkg_resources.working_set}
            missing_packages_list = self.__required_packages_list - installed_packages_list
            for module in missing_packages_list:
                self.install(module)
        except Exception as e:
            raise RuntimeError(e)


if __name__ == '__main__':
    modules = {"pillow", "Image", "pandas", 'numpy', 'Path', 'uuid', 'matplotlib', 'openpyxl',
               "PyDrive", "google-auth", "google-api-python-client",
               "google-api-core", "google-auth",
               "google-auth-httplib2", "google-auth-oauthlib", "xlrd",
               "googleapis-common-protos", "oauthlib", "oauth2client", "uritemplate"}
    mi = ModulesImports(modules)
    mi.install_list()
