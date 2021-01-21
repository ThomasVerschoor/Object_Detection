#include "zmq_module.h"

ZMQModule::ZMQModule() : Module({}, {"zeromq"}) {}

void ZMQModule::setup(dust::ModuleRegistry *moduleRegistry) {
    moduleRegistry->registerTransportFactory("zeromq", &zmqFactory);
}

void ZMQModule::cleanup(dust::ModuleRegistry *moduleRegistry) {
    moduleRegistry->unregisterTransportFactory("zeromq");
}
