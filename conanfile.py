import re
from conans import ConanFile, CMake, tools
import boto3

class SteamworksConan(ConanFile):
    name = "Steamworks"
    version = "1.44"
    url = "https://github.com/SteffenL/conan-steamworks.git"
    description = "Steamworks SDK"
    settings = {
        "os": ["Windows", "Linux", "Macos"],
        "arch": ["x86", "x86_64"]
    }
    license = "Apache-2.0"

    _checksums = {
        "1.42": "7695f8e183bef16dc2e663ffbdfad2248ae266bce8ff42066a3e88e1d54f0f42",
        "1.43": "600b4e8a098fe4c9f496b39889860b4932253e6a68f3243c408d621ac7f3ebdd",
        "1.44": "6f7b85bfe1bf032f1a1d743db30c43d31d04010e127e134e9b5a98b8ebe37372"
    }
    _s3_region = "eu-north-1"
    _s3_bucket = "private.resources.development.langnes"
    _s3_path = "thirdparty/steamworks/steamworks_sdk_%s.zip" % version.replace(".", "")

    def configure(self):
        if self.settings.os == "Macos" and self.settings.arch != "x86":
            raise ValueError("Only x86 is supported for macOS")

    def build(self):
        checksum = SteamworksConan._checksums[self.version]
        akid = tools.get_env("LANGNES_AWS_ACCESS_KEY_ID")
        sak = tools.get_env("LANGNES_AWS_SECRET_ACCESS_KEY")

        local_path = "sdk.zip"
        s3 = boto3.client("s3", region_name=SteamworksConan._s3_region, aws_access_key_id=akid, aws_secret_access_key=sak)
        s3.download_file(SteamworksConan._s3_bucket, SteamworksConan._s3_path, local_path)
        tools.check_sha256(local_path, checksum)
        tools.unzip(local_path)

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
