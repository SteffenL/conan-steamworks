import re
from conans import ConanFile, CMake, tools

class SoftactivateConan(ConanFile):
    name = "SoftActivateLicensingSDK"
    version = "2.3.1"
    url = "https://github.com/SteffenL/conan-softactivate-licensing-sdk.git"
    description = "SoftActivate Licensing SDK"
    settings = {
        "os": ["Windows"],
        "arch": ["x86", "x86_64"]
    }
    options = {
        "shared": [True]
    }
    default_options = "shared=True"

    def build(self):
        url = "https://s3-eu-west-1.amazonaws.com/development.langnes/thirdparty/softactivate/licensing_sdk_%s.zip" % self.version
        tools.get(url)

    def package(self):
        arch = {
            "x86": "Win32",
            "x86_64": "x64"
        }[str(self.settings.arch)]

        self.copy("*.h", dst="include", src="include")
        self.copy("Licensing.lib", dst="lib", src="lib/%s/Release" % arch, keep_path=False)
        self.copy("Licensing.dll", dst="bin", src="bin/%s/Release" % arch, keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["Licensing"]
