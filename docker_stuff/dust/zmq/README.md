# ZeroMQ module

The zmq module allows applications to send and receive data using ZeroMQ PUB/SUB.

## Requirements

* DUST 2
* [`libzmq`](https://github.com/zeromq/libzmq) 4.3 or higher
* [`cppzmq`](https://github.com/zeromq/cppzmq) version compatible with `libzmq` version

```bash
git clone https://github.com/zeromq/libzmq.git && \
    cd libzmq && \
    git checkout v4.3.2 && \
    mkdir build && cd build && \
    cmake .. && make -j4 install && \
    cd ../.. && rm -rfd libzmq
git clone https://github.com/zeromq/cppzmq.git && \
    cd cppzmq && \
    git checkout v4.4.1 && \
    mkdir build && cd build && \
    cmake .. && make -j4 install && \
    cd ../.. && rm -rfd cppzmq
```

## Building

```bash
mkdir -p build
cd build

cmake -DCMAKE_BUILD_TYPE=Release ..
make -j4
```

## Usage

### Configuration

```json
{
    "type": "zeromq",
    "topic": "testing-grounds",            
    "host_server": true,
    "host": "tcp://*:5000",
    "publish": true
}
```

| Field | Required | Values |
| --- | --- | --- |
| host | yes | The connection string passed to ZeroMQ |
| publish | yes | Set the current block as publisher |
| topic | yes | The topic used by ZeroMQ to differentiate this channel |
| host_server | no (default false) | Set to true to host the TCP server |
| timeout | no (default 2500) | Sets the `ZMQ_RCVTIMEO` value of ZeroMQ |

