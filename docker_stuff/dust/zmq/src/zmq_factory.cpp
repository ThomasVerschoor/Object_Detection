#include "zmq_factory.h"
#include "zmq_transport.h"

dust::Transport *ZMQFactory::getTransport(dust::Configuration &configuration) {
    configuration.assertHas({"publish", "topic"});

    bool publisher = configuration.getBool("publish").value();
    std::string topic = configuration.getString("topic").value();
    bool hostServer = configuration.getBool("host_server").value_or(false);
    int timeout = configuration.getInt("timeout").value_or(2500);

    std::string address;
    if (configuration.has({"host"})) {
        address = configuration.getString("host").value();
    } else {
        configuration.assertHas({"protocol", "address"});
        std::string protocol = configuration.getString("protocol").value();
        address = protocol + "://" + configuration.getString("address").value();
        if (configuration.has({"port"})) {
            address += ":" + std::to_string(configuration.getUnsignedInt("port").value());
        }
    }

    return new ZMQTransport(publisher, hostServer, address, topic, timeout);
}
