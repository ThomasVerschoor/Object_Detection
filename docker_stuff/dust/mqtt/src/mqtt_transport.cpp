#include <cstring>
#include <utility>
#include "mqtt_transport.h"

MQTTTransport::MQTTTransport(std::string host, uint16_t port, std::string topic, std::string username, std::string password, bool publish, int qos)
        : Transport("mqtt"), host(std::move(host)), port(port),
          topic(std::move(topic)), username(std::move(username)),
          password(std::move(password)), publish(publish),
          qos(qos) {}

void MQTTTransport::connect() {
    mosquitto_lib_init();

    this->client = mosquitto_new(nullptr, true, this);
    if (!this->client) {
        fprintf(stderr, "Error: Out of memory.\n");
        exit(1);
    }

    mosquitto_connect_callback_set(this->client, [](struct mosquitto *mosquitto, void *transportPtr, int) {
        auto transport = (static_cast<MQTTTransport *>(transportPtr));
        if (!transport->publish) {
            mosquitto_subscribe(mosquitto, nullptr, transport->topic.c_str(), transport->qos);
        }
    });

    if (!username.empty()) {
        mosquitto_username_pw_set(this->client, username.c_str(), !password.empty() ? password.c_str() : nullptr);
    }

    if (mosquitto_connect(this->client, host.c_str(), port, 60)) {
        fprintf(stderr, "Unable to connect.\n");
        exit(1);
    }
    int loop = mosquitto_loop_start(this->client);
    if (loop != MOSQ_ERR_SUCCESS) {
        fprintf(stderr, "Unable to start loop: %i\n", loop);
        exit(1);
    }
    if (!publish) {
        mosquitto_message_callback_set(this->client, &MQTTTransport::on_message);
    }
}

void MQTTTransport::disconnect() {
    mosquitto_disconnect(this->client);
    mosquitto_loop_stop(this->client, false);
    mosquitto_destroy(this->client);
    mosquitto_lib_cleanup();

    this->client = nullptr;
}

void MQTTTransport::sendData(const std::vector<uint8_t> &payload) {
    if (publish) {
        mosquitto_publish(this->client, nullptr, topic.c_str(), static_cast<int>(payload.size()), payload.data(), qos, false);
    }
}

void MQTTTransport::on_message(struct mosquitto *, void *transport, const struct mosquitto_message *message) {
    std::vector<uint8_t> data(message->payloadlen);
    std::memcpy(data.data(), message->payload, message->payloadlen);
    (static_cast<MQTTTransport *>(transport))->getReceiveCallback()(data);
}

void MQTTTransport::flush() {

}
