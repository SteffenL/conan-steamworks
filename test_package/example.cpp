#include <SoftActivate/licensing.h>

#include <iostream>

int main() {
    auto hid = KeyHelperA::GetCurrentHardwareId();
    std::cout << "Hardware ID: " << hid << std::endl;
    std::cout << "SoftActivate Licensing SDK  works!" << std::endl;
    return 0;
}
