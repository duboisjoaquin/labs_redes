#ifndef TRANSPORT_RX
#define TRANSPORT_RX

#include <omnetpp.h>
#include <string.h>

using namespace omnetpp;

class TransportRx: public cSimpleModule {
    private:
        cOutVector bufferSizeVector;
        cOutVector packetDropVector;
        cQueue buffer;
        cQueue fdBuffer;
        cMessage *endServiceEvent;
        cMessage *endFeedbackEvent;
        simtime_t serviceTime;
        bool fdStatus;

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
    endFeedbackEvent = NULL;
}

TransportRx::~TransportRx() {
    cancelAndDelete(endServiceEvent);
    cancelAndDelete(endFeedbackEvent);
}

void TransportRx::initialize() {
    buffer.setName("buffer");
    bufferSizeVector.setName("BufferSizeVector");
    packetDropVector.setName("PacketDropVector");
    fdBuffer.setName("bufferFd");
    packetDropVector.record(0);
    endServiceEvent = new cMessage("endService");
    endFeedbackEvent = new cMessage("endFeedback");
    fdStatus = false;
}

void TransportRx::finish() {
}


void TransportRx::handleMessage(cMessage *msg) {

    if (msg == endServiceEvent) {
          // si el paquete esta en el buffer
          if (!buffer.isEmpty()) {
              // saca el paquete de la queue
              cPacket *pkt = (cPacket*) buffer.pop();
              // manda el paquete
              send(pkt, "toApp");
              // comienza un nuevo servicio
              serviceTime = pkt->getDuration();
              scheduleAt(simTime() + serviceTime, endServiceEvent);
          }
    } else  if(msg == endFeedbackEvent){
        // el mensaje es un feedback debe salir por el out con queue2
        if (!fdBuffer.isEmpty()) {
            // si el buffer de feedback no esta vacio manda el siguiente
            cPacket *fdPacket = (cPacket*) fdBuffer.pop();
                send(fdPacket, "toOut$o");
                scheduleAt(simTime() + fdPacket->getDuration(), endFeedbackEvent);
        }
    } else { // si el msg es data
        if (buffer.getLength() >= par("bufferSize").intValue()) {
            // dropea el paquete
            delete(msg);
            this->bubble("packet-dropped");
            packetDropVector.record(1);
        } else {
            // mete el mensaje a la cola
            if (msg->getKind() == 2 || msg->getKind() == 3){
                fdBuffer.insert(msg);

                if (!endFeedbackEvent->isScheduled()) {
                    //si no hay mensajes scheluded lo manda
                    scheduleAt(simTime() + 0, endFeedbackEvent);
                }
            } else {
                //el mensaje es de tipo 1 y hay que ver como deja el buffer
                float umbralMax = 0.75 * par("bufferSize").intValue();
                float umbralMin = 0.45 * par("bufferSize").intValue();

                if (buffer.getLength() >= umbralMax && !fdStatus){
                    //Caso umbralMax es alcanzado y debemos regular el mandando de paquertes
                    cPacket *fdPacket = new cPacket("packet");
                    fdPacket->setByteLength(20);
                    fdPacket->setKind(2);
                    send(fdPacket, "toOut$o");  //conexion de entrada/salida conectada con queue2
                    fdStatus = true; // queremos que solo checkee el if que sigue despues de esto
                }else if (buffer.getLength() < umbralMin && fdStatus){
                    //Caso umbralMax es alcanzado y debemos regular el mandando de paquertes
                    cPacket *fdPacket = new cPacket("packet");
                    fdPacket->setByteLength(20);
                    fdPacket->setKind(3);
                    send(fdPacket, "toOut$o"); //conexion de entrada/salida conectada con queue2
                    fdStatus = false; // queremos que solo checkee el if de arriba despues de esto
                }
                // encolo el mensaje
                buffer.insert(msg);
                bufferSizeVector.record(buffer.getLength());
                // el server esta estatico
                if (!endServiceEvent->isScheduled()) {
                    // empieza el servicio
                    scheduleAt(simTime() + 0, endServiceEvent);
                }
            }
        }
    }
}

#endif
