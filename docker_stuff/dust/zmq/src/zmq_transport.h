#ifndef DUST_ZMQ_TRANSPORT_H
#define DUST_ZMQ_TRANSPORT_H


#include <dust/module/transport.h>
#include <zmq.hpp>
#include <atomic>
#include <mutex>

#ifdef _WIN32
#include <Windows.h>
#endif

class ZMQTransport : public dust::Transport {
private:
    bool publisher;
    bool hostServer;
    std::string address;
    std::string topic;
    int timeout;

    bool connected = false;
    bool working = false;

#ifdef _WIN32
    HANDLE threadId;
#else
    pthread_t threadId = 0;
#endif
    std::mutex lock;
    std::unique_ptr<zmq::context_t> context;
    std::unique_ptr<zmq::socket_t> socket;
    std::atomic_bool thread_signal{};

    void initializeSocket();

    void destroySocket();

    static void *subscribe_run(void *ptr);

public:
    ZMQTransport(bool publisher, bool hostServer, std::string address, std::string topic, int timeout);

    ~ZMQTransport() override;

    void connect() override;

    void sendData(const std::vector<uint8_t> &payload) override;

    void disconnect() override;

    void flush() override;
};


#endif //DUST_ZMQ_TRANSPORT_H
