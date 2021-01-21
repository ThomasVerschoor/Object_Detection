#ifndef DUST_MQTT_TRANSPORT_H
#define DUST_MQTT_TRANSPORT_H


#include <dust/module/transport.h>
#include <mosquitto.h>

class MQTTTransport : public dust::Transport {
private:
    std::string host;
    uint16_t port;
    std::string topic;
    std::string username;
    std::string password;
    int qos;

    bool publish;

    mosquitto *client = nullptr;

    static void on_message(struct mosquitto *client, void *userData, const struct mosquitto_message *message);

public:
    MQTTTransport(std::string host, uint16_t port, std::string topic, std::string username, std::string password, bool publish, int qos);

    void connect() override;

    void disconnect() override;

    void sendData(const std::vector<uint8_t> &payload) override;

    void flush() override;
};


#endif //DUST_MQTT_TRANSPORT_H
