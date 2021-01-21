#include "mqtt_module.h"

MQTTModule::MQTTModule() : Module({}, {"mqtt"}) {}

void MQTTModule::setup(dust::ModuleRegistry *moduleRegistry) {
    moduleRegistry->registerTransportFactory("mqtt", &factory);
}

void MQTTModule::cleanup(dust::ModuleRegistry *moduleRegistry) {
    moduleRegistry->unregisterTransportFactory("mqtt");
}
