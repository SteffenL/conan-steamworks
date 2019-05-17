import re
from conans import ConanFile, CMake, tools
import boto3

class SoftactivateConan(ConanFile):
    name = "SoftActivateLicensingSDK"
    version = "2.3.1"
    url = "https://github.com/SteffenL/conan-softactivate-licensing-sdk.git"
    description = "SoftActivate Licensing SDK"
    settings = {
        "os": ["Windows"],
        "arch": ["x86", "x86_64"],
        "build_type": ["Debug", "Release"]
    }

    _checksums = {
        "2.3.1": "bc79760bfd7fcd145d5a248c2c33d2ad798581616cc4beafa4178219657012b2"
    }
    _s3_region = "eu-north-1"
    _s3_bucket = "private.resources.development.langnes"
    _s3_path = "thirdparty/softactivate/licensing_sdk_%s.zip" % version

    def build(self):
        checksum = SoftactivateConan._checksums[self.version]
        akid = tools.get_env("LANGNES_AWS_ACCESS_KEY_ID")
        sak = tools.get_env("LANGNES_AWS_SECRET_ACCESS_KEY")

        local_path = "sdk.zip"
        s3 = boto3.client("s3", region_name=SoftactivateConan._s3_region, aws_access_key_id=akid, aws_secret_access_key=sak)
        s3.download_file(SoftactivateConan._s3_bucket, SoftactivateConan._s3_path, local_path)
        tools.check_sha256(local_path, checksum)
        tools.unzip(local_path, "sdk")

    def package(self):
        arch = {
            "x86": "Win32",
            "x86_64": "x64"
        }[str(self.settings.arch)]

        self.copy("*.h", dst="include", src="sdk/include")
        self.copy("Licensing.lib", dst="lib", src="sdk/lib/%s/%s" % (arch, self.settings.build_type), keep_path=False)
        self.copy("Licensing.dll", dst="bin", src="sdk/bin/%s/%s" % (arch, self.settings.build_type), keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["Licensing"]
