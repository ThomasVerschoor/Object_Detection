#ifndef DUST_ZERO_MQ_FACTORY_H
#define DUST_ZERO_MQ_FACTORY_H


#include <dust/module/transport_factory.h>

class ZMQFactory : public dust::TransportFactory {
public:
    dust::Transport *getTransport(dust::Configuration &configuration) override;
};


#endif //DUST_ZERO_MQ_FACTORY_H
