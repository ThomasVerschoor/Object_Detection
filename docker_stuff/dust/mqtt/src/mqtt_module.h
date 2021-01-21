#ifndef DUST_MQTT_MODULE_H
#define DUST_MQTT_MODULE_H


#include <dust/module/module.h>
#include "mqtt_factory.h"

class MQTTModule : public dust::Module {
private:
    MQTTFactory factory;

public:
    MQTTModule();

    void setup(dust::ModuleRegistry *moduleRegistry) override;

    void cleanup(dust::ModuleRegistry *moduleRegistry) override;
};

EXPORT_MODULE(MQTTModule)


#endif //DUST_MQTT_MODULE_H
