import re
from conans import ConanFile, CMake, tools

class SteamworksConan(ConanFile):
    name = "Steamworks"
    version = "1.42"
    url = "https://github.com/SteffenL/conan-steamworks.git"
    description = "Steamworks SDK"
    settings = {
        "os": ["Windows", "Linux", "Macos"],
        "arch": ["x86", "x86_64"]
    }
    license = "Apache-2.0"

    def configure(self):
        if self.settings.os == "Macos" and self.settings.arch != "x86":
            raise ValueError("Only x86 is supported for macOS")

    def build(self):
        url = "https://s3-eu-west-1.amazonaws.com/development.langnes/thirdparty/steamworks/steamworks_sdk_%s.zip" % self.version.replace(".", "")
        tools.get(url)

    def package(self):
        self.copy("*.h", "include", "sdk/public")

        os_name = str(self.settings.os)
        arch = str(self.settings.arch)
        to_copy = []

        if os_name == "Windows":
            to_copy += [
                (".dll", "bin"),
                (".lib", "lib")
            ]
        elif os_name == "Linux":
            to_copy += [
                (".so", "lib")
            ]
        elif os_name == "Macos":
            to_copy += [
                (".dylib", "lib")
            ]

        for ext, dst in to_copy:
            src = "/".join([s for s in [
                "sdk/redistributable_bin",
                self._make_steam_lib_dir_name(os_name, arch),
                self._make_steam_lib_base_name(os_name, arch) + ext
            ] if s])

            self.copy(src, dst=dst, keep_path=False)

    def package_info(self):
        os_name = str(self.settings.os)
        arch = str(self.settings.arch)
        self.cpp_info.libs = [self._make_steam_lib_import_name(os_name, arch)]

    def _make_steam_lib_dir_name(self, os_name, arch):
        return {
            "Windows": {
                "x86": "",
                "x86_64": "win64"
            },
            "Linux": {
                "x86": "linux32",
                "x86_64": "linux64"
            },
            "Macos": {
                "x86": "osx32"
            }
        }[os_name][arch]

    def _make_steam_lib_base_name(self, os_name, arch):
        return {
            "Windows": {
                "x86": "steam_api",
                "x86_64": "steam_api64"
            },
            "Linux": {
                "x86": "libsteam_api",
                "x86_64": "libsteam_api"
            },
            "Macos": {
                "x86": "libsteam_api"
            }
        }[os_name][arch]

    def _make_steam_lib_import_name(self, os_name, arch):
        name = self._make_steam_lib_base_name(os_name, arch)
        if os_name != "Windows":
            name = re.sub("^lib", "", name)
        return name
