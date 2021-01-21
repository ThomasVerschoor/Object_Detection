#include <iostream>
#include "zmq_transport.h"

#if _WIN32
#include <Windows.h>
#endif

ZMQTransport::ZMQTransport(bool publisher, bool hostServer, std::string address, std::string topic, int timeout) : Transport("zeromq"), publisher(publisher),
                                                                                                                   hostServer(hostServer), address(std::move(address)),
                                                                                                                   topic(std::move(topic)), timeout(timeout) {}

ZMQTransport::~ZMQTransport() {
    disconnect();
}

void ZMQTransport::connect() {
    const std::lock_guard<std::mutex> guard(lock);
    if (!connected) {
        if (context == nullptr) {
            context = std::make_unique<zmq::context_t>(1);
        }

        if (publisher) {
            this->initializeSocket();
        } else {
            thread_signal.store(true);
#if _MSC_VER
            threadId = CreateThread(NULL, 0, reinterpret_cast<LPTHREAD_START_ROUTINE>(&ZMQTransport::subscribe_run), this, 0, NULL);
#else
            pthread_attr_t attr;
            pthread_attr_init(&attr);

            pthread_create(&threadId, &attr, &ZMQTransport::subscribe_run, this);
#endif
            working = true;
        }
    }
}

void ZMQTransport::disconnect() {
    const std::lock_guard<std::mutex> guard(lock);
    if (connected) {
        //kill worker
        if (working) {
            thread_signal.store(false);
#if _WIN32
            WaitForSingleObject(threadId, 1000);
            CloseHandle(threadId);
#else
            pthread_join(threadId, nullptr);
#endif

            working = false;
        } else {
            this->destroySocket();
        }

        //remove objects
        if (context) {
            context->close();
            context.reset();
        }

        if (socket) {
            socket.reset();
        }

        connected = false;
    }
}

void ZMQTransport::sendData(const std::vector<uint8_t> &payload) {
    const std::lock_guard<std::mutex> guard(lock);
    if (connected) {
        if (socket->send(zmq::message_t(topic), zmq::send_flags::sndmore)) {
            socket->send(zmq::message_t(payload.data(), payload.size()), zmq::send_flags::none);
        }
    }
}

void *ZMQTransport::subscribe_run(void *ptr) {
    auto zmq = static_cast<ZMQTransport *>(ptr);
    zmq->initializeSocket();

    zmq->socket->setsockopt(ZMQ_SUBSCRIBE, zmq->topic.c_str(), zmq->topic.size());
    zmq->socket->setsockopt(ZMQ_RCVTIMEO, zmq->timeout);
    zmq->socket->setsockopt(ZMQ_SNDHWM, 1);

    while (zmq->thread_signal.load()) {
		try {
			zmq::message_t topicMsg;
			zmq->socket->recv(topicMsg);
			std::string recvTopic = std::string(static_cast<char*>(topicMsg.data()), topicMsg.size());

			if (!recvTopic.empty()) {
				zmq::message_t dataMsg;
				zmq->socket->recv(dataMsg);
				std::vector<uint8_t> data(dataMsg.size());
				std::memcpy(data.data(), dataMsg.data(), dataMsg.size());

				zmq->getReceiveCallback()(data);
			}
		}
		catch (zmq::error_t & exception) {
			fprintf(stderr, "%s\n", exception.what());
		}
    }
    zmq->destroySocket();
    return nullptr;
}

void ZMQTransport::initializeSocket() {
    int type;
    if (publisher) {
        type = ZMQ_PUB;
    } else {
        type = ZMQ_SUB;
    }

    socket = std::make_unique<zmq::socket_t>(*context, type);
    if (hostServer) {
        socket->bind(address);
    } else {
        socket->connect(address);
    }

    connected = true;
}

void ZMQTransport::destroySocket() {
    if (hostServer) {
        const size_t buf_size = 32;
        char buf[buf_size];
        socket->getsockopt(ZMQ_LAST_ENDPOINT, buf, (size_t *) &buf_size);
		try {
			socket->unbind(buf);
		} catch (zmq::error_t &exception) {
			fprintf(stderr, "%s\n", exception.what());
		}
    } else {
		try {
			socket->disconnect(address);
		} catch (zmq::error_t &exception) {
			fprintf(stderr, "%s\n", exception.what());
		}
    }
    socket->close();
}

void ZMQTransport::flush() {

}
