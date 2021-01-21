#ifndef DUST_MQTT_FACTORY_H
#define DUST_MQTT_FACTORY_H


#include <dust/module/transport_factory.h>

class MQTTFactory : public dust::TransportFactory {
public:
    dust::Transport *getTransport(dust::Configuration &configuration) override;
};


#endif //DUST_MQTT_FACTORY_H
