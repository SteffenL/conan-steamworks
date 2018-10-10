#include <steam/steam_api.h>

#include <iostream>

int main() {
    SteamAPI_Init();
    SteamAPI_Shutdown();
    std::cout << "Steam API works!" << std::endl;
    return 0;
}
