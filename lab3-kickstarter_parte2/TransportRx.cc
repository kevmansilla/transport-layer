#ifndef TRANSPORTRX
#define TRANSPORTRX

#include <string.h>
#include <omnetpp.h>

#include "Feedback_m.h"

using namespace omnetpp;

class TransportRx : public cSimpleModule {
private:
    cQueue buffer;
    cMessage *endServiceEvent;
    simtime_t serviceTime;
    cOutVector bufferSizeVector;
    cOutVector packetDropVector;

    bool congestion;

public:
    TransportRx();
    virtual ~TransportRx();
protected:
    virtual void initialize();
    virtual void finish();
    virtual void handleMessage(cMessage *msg);
};

Define_Module(TransportRx);

TransportRx::TransportRx() {
    endServiceEvent = NULL;
}

TransportRx::~TransportRx() {
    cancelAndDelete(endServiceEvent);
}

void TransportRx::initialize() {
    buffer.setName("RxBuffer");
    endServiceEvent = new cMessage("endServiceEvent");
    congestion = false;
}

void TransportRx::finish() {
}

void TransportRx::handleMessage(cMessage *msg) {
    // Si se recibe un mensaje tipo 2 quiere decir que hay congestion en la red
    // VER PQ SE RECIBE UN FEEDBACK
    if(msg->getKind() == 2) {
        Feedback* pkt = (Feedback *)msg;
        congestion = pkt->getCongestion();
    } else {
        // En caso contrario es un mensaje de data o es un endServiceEvent
        // si msg está señalando un endServiceEvent
        if (msg == endServiceEvent) {
            // Si el paquete está en el búfer, envíe el siguiente
            if (!buffer.isEmpty()) {
                // dequeue paquete
                cPacket *pkt = (cPacket *)buffer.pop();
                // envia packet
                send(pkt, "toApp");
                // iniciar nuevo servicio
                serviceTime = pkt->getDuration();
                scheduleAt(simTime() + serviceTime, endServiceEvent);
            }
        } else { // if msg is a data packet
            // chequeo del limite del buffer
            if (buffer.getLength() >= par("bufferSize").intValue()) { 
                // Si el buufer esta lleno
                // drop packet
                delete msg;
                this->bubble("packet dropped");
                packetDropVector.record(1);
            } else {
                // enqueue packet
                buffer.insert(msg);
                bufferSizeVector.record(buffer.getLength());
                // si el servidor está inactivo
                if (!endServiceEvent->isScheduled()) {
                    // iniciar nuevo servicio ahora
                    scheduleAt(simTime() + 0, endServiceEvent);
                }
            }
        }
        // se envia el paquete de feedback
        Feedback * f = new Feedback();
        f->setKind(2);
        f->setByteLength(20);
        f->setRemainingBuffer(par("bufferSize").intValue() - buffer.getLength());
        f->setCongestion(congestion);
        send(f,"toOut$o");
    }
}

#endif
