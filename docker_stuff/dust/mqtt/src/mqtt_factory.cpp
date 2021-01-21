#include "mqtt_factory.h"
#include "mqtt_transport.h"

dust::Transport *MQTTFactory::getTransport(dust::Configuration &configuration) {
    configuration.assertHas({"host", "port", "topic"});

    auto host = configuration.getString("host").value();
    auto port = configuration.getUnsignedInt16("port").value();
    auto topic = configuration.getString("topic").value();
    auto username = configuration.getString("username").value_or("");
    auto password = configuration.getString("password").value_or("");
    auto publish = configuration.getBool("publish").value_or(false);
    auto qos = configuration.getInt("qos").value_or(0);
    return new MQTTTransport(host, port, topic, username, password, publish, qos);
}
