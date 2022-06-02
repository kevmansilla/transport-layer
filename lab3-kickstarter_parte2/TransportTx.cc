#ifndef TRANSPORTTX
#define TRANSPORTTX

#include <string.h>
#include <omnetpp.h>

#include "Feedback_m.h"

using namespace omnetpp;

class TransportTx: public cSimpleModule {
private:
    cQueue buffer;
    cMessage *endServiceEvent;
    simtime_t serviceTime;
    cOutVector bufferSizeVector;
    cOutVector packetDropVector;

    bool congestion;
    int RemainingBuffer;
    bool currentGeneration;

public:
    TransportTx();
    virtual ~TransportTx();
protected:
    virtual void initialize();
    virtual void finish();
    virtual void handleMessage(cMessage *msg);
};

Define_Module(TransportTx);

TransportTx::TransportTx() {
    endServiceEvent = NULL;
}

TransportTx::~TransportTx() {
    cancelAndDelete(endServiceEvent);
}

void TransportTx::initialize() {
    buffer.setName("buffer");
    endServiceEvent = new cMessage("endService");
    congestion = false;
    RemainingBuffer = 1;
    currentGeneration = false;
}

void TransportTx::finish() {
}

void TransportTx::handleMessage(cMessage *msg) {
    // Si el paquete es un feedback, tomamos los valores para luego actuar:
    if (msg->getKind() == 2) {
        Feedback* f = (Feedback *)msg;
        congestion = f->getCongestion();
        RemainingBuffer = f->getRemainingBuffer();
        delete(msg);
    }
    // Si el paquete es un endServiceEvent, estamos autorizados a mandar un nuevo paquete:
    else if (msg == endServiceEvent) {
        // Chequeamos que el buffer del receptor tenga espacio y no haya congestion:
        if(RemainingBuffer > 0 && !congestion){
            // Si hay un paquete en la queue para ser enviado, lo enviamos:
            if (!buffer.isEmpty()) {
                // Tomamos el paquete y lo dequeue:
                cPacket *pkt = (cPacket*) buffer.pop();
                // Mandamos el packete:
                send(pkt, "toOut$o");
                
                // Como el mensaje se envio, enviamos endServiceEvent para continuar enviando paquetes:
                serviceTime = pkt->getDuration();
                scheduleAt(simTime() + serviceTime, endServiceEvent);

                // Decrementamos el tamano de la ventana en uno:
                RemainingBuffer--;
            }
        }
        // Si hay congestion o el buffer receptor esta lleno, retrasamos el envio:
        else {
            scheduleAt(simTime() + 0.1, endServiceEvent);
        }
    }
    // Si el paquete es un paquete de datos:
    else {
        // Si el buffer esta lleno, el paquete se pierde (VER QUE HACER):
        if (buffer.getLength() >= par("bufferSize").intValue()) {
            delete msg;
            this->bubble("packet dropped");
            packetDropVector.record(1);
        }
        // Si hay lugar en la queue, guardamos el mensaje:
        else {
            buffer.insert(msg);
            bufferSizeVector.record(buffer.getLength());
            // Si no hay un endServiceEvent programado, enviamos la confirmacion:
            if (!endServiceEvent->isScheduled()) {
                scheduleAt(simTime() + 0, endServiceEvent);
            }
        }
    }
    // Si el buffer actual esta casi lleno, bajamos la generacion de paquetes:
    if(buffer.getLength() >= par("bufferSize").intValue()){
        cSimulation * sim = sim->getActiveSimulation();
        cModule * gen = sim->getModuleByPath("Network.nodeTx.gen");
        gen->par("generationInterval").setDoubleValue(gen->par("generationInterval").doubleValue() * 1.3);
        currentGeneration = true;
    }

    // Si el buffer no supera el 85% de su capacidad, aumentamos la generacion de paquetes:
    if (currentGeneration && (buffer.getLength() <= par("bufferSize").intValue() * 0.85)) {
        currentGeneration = false;
        cSimulation * sim = sim->getActiveSimulation();
        cModule * gen = sim->getModuleByPath("Network.nodeTx.gen");
        gen->par("generationInterval").setDoubleValue(gen->par("generationInterval").doubleValue() / 1.3);
    }

}

#endif /* TransportTx */
