#ifndef QUEUE
#define QUEUE

#include <string.h>
#include <omnetpp.h>

using namespace omnetpp;

class Queue: public cSimpleModule {
private:
    cQueue buffer;
    cMessage *endServiceEvent;
    simtime_t serviceTime;
    cOutVector bufferSizeVector;
    cOutVector packetDropVector;
    bool fdStatus;
public:
    Queue();
    virtual ~Queue();
protected:
    virtual void initialize();
    virtual void finish();
    virtual void handleMessage(cMessage *msg);
};

Define_Module(Queue);

Queue::Queue() {
    endServiceEvent = NULL;
}

Queue::~Queue() {
    cancelAndDelete(endServiceEvent);
}

void Queue::initialize() {
    buffer.setName("Buffer");
    bufferSizeVector.setName("BufferSizeVector");
    packetDropVector.setName("PacketDropVector");
    packetDropVector.record(0);
    endServiceEvent = new cMessage("endService");
    fdStatus = false;
}

void Queue::finish() {
}

void Queue::handleMessage(cMessage *msg) {

    if (msg == endServiceEvent) {
          // si el paquete esta en el buffer
          if (!buffer.isEmpty()) {
              // saca el paquete de la queue
              cPacket *pkt = (cPacket*) buffer.pop();
              // manda el paquete
              send(pkt, "out");
              // comienza un nuevo servicio
              serviceTime = pkt->getDuration();
              scheduleAt(simTime() + serviceTime, endServiceEvent);
          }
    } else { //si el mensaje es data
        if (!(buffer.getLength() >= par("bufferSize").intValue())) {
            int umbralMax = 0.75 * par("bufferSize").intValue();
            int umbralMin = 0.45 * par("bufferSize").intValue();

            if(buffer.getLength() >= umbralMax && !fdStatus){
                cPacket *fdPacket = new cPacket("feedback");
                fdPacket->setByteLength(20);
                fdPacket->setKind(2);
                buffer.insertBefore(buffer.front(), fdPacket);
                fdStatus = true; // queremos que solo checkee el if que sigue despues de esto

            } else if(buffer.getLength() < umbralMin && fdStatus){
                    cPacket *fdPacket = new cPacket("feedback");
                    fdPacket->setByteLength(20);
                    fdPacket->setKind(3);
                    buffer.insertBefore(buffer.front(), fdPacket);
                    fdStatus = false; // queremos que solo checkee el if de arriba despues de esto
             }

            buffer.insert(msg);
            bufferSizeVector.record(buffer.getLength());
            // si el server esta estatico
            if (!endServiceEvent->isScheduled()) {
                // inicia el servicio
                scheduleAt(simTime() + 0, endServiceEvent);
            }

        }
        else {
            // dropeamos el paquete
            delete(msg);
            this->bubble("packet-dropped");
            packetDropVector.record(1);
        }
    }
}




#endif /* QUEUE */
