#include <iostream>
#include <dust/core.h>

int main(int argc, char *argv[]) {
    dust::Core communication("subscriber-block", ".");
    communication.setup();
    std::thread cycleThread = communication.cycleForever();

    communication.parseConfigurationFile("../example/resources/configuration.json");
    communication.connect();

    communication.registerListener("subscription-channel", [](const std::vector<uint8_t> &payload) {
        std::cout << "received message with payload of " << payload.size() << " bytes" << std::endl;
    });

    std::this_thread::sleep_for(std::chrono::seconds(10));

    communication.disconnect();
    communication.cycleStop();
    cycleThread.join();

    return 0;
}
