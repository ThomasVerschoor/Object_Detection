# MQTT module

The MQTT module allows DUST blocks to communicate using MQTT.

## Dependencies

This module depends on Eclipse Mosquitto.

Note: when using vcpkg, Mosquitto installs the `pthreads` (for Windows) library. This currently breaks the compilation of projects that use other `pthread` implementations, like the implementation in `mingw64`.
If you encounter problems in projects that use `pthread` or `<thread>`, you should remove the header files installed by `pthreads`.

## Configuration

```json
{
    "type": "mqtt",
    "host": "test.mosquitto.org",
    "port": 1883,
    "topic": "testing-grounds",
    "username": "",
    "password": "",
    "publish": false,
    "qos": 0
}
```

| Field | Required | Values |
| --- | --- | --- |
| host | yes | The IP or hostname of the broker |
| port | yes | The port of the broker |
| topic | yes | The topic to publish or subscribe to |
| username | no (default empty) | The username used to connect to the broker |
| password | no (default empty) | The password used to connect to the broker |
| publish | no (default false) | True if the block is publishing, false if it is listening |
| qos | no (default 0) | Quality of Service of the connection |