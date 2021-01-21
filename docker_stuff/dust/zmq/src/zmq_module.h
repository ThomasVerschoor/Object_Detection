#ifndef DUST_ZMQ_MODULE_H
#define DUST_ZMQ_MODULE_H


#include <dust/module/module.h>
#include "zmq_factory.h"

class ZMQModule : public dust::Module {
private:
    ZMQFactory zmqFactory;

public:
    ZMQModule();

    void setup(dust::ModuleRegistry *moduleRegistry) override;

    void cleanup(dust::ModuleRegistry *moduleRegistry) override;
};

EXPORT_MODULE(ZMQModule)

#endif //DUST_ZMQ_MODULE_H
