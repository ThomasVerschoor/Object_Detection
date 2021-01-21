#include <iostream>
#include <vector>
#include <dust/core.h>

int main(int argc, char *argv[]) {
    std::vector<uint8_t> payload;

    payload.push_back(0x00);
    payload.push_back(0x01);
    payload.push_back(0x02);
    payload.push_back(0x03);
    payload.push_back(0x04);
    payload.push_back(0x05);
    payload.push_back(0x06);
    payload.push_back(0x07);

    dust::Core communication("publisher-block", ".");
    auto cycleThread = communication.cycleForever();
    communication.setup();

    communication.parseConfigurationFile("../example/resources/configuration.json");
    communication.connect();

    for (int i = 0; i < 10; ++i) {
        std::this_thread::sleep_for(std::chrono::seconds(1));
        communication.publish("publish-zmq", payload);
    }

    std::this_thread::sleep_for(std::chrono::seconds(1));

    communication.disconnect();
    communication.cycleStop();
    cycleThread.join();

    return 0;
}
