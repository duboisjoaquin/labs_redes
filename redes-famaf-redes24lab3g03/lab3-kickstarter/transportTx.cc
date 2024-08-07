#ifndef TRANSPORT_TX
#define TRANSPORT_TX

#include <omnetpp.h>
#include <string.h>

using namespace omnetpp;

class TransportTx : public cSimpleModule {
    private:
        cOutVector bufferSizeVector;
        cOutVector packetDropVector;
        cQueue buffer;
        cMessage *endServiceEvent;
        simtime_t serviceTime;
        float transferModifier;
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
    bufferSizeVector.setName("BufferSizeVector");
    packetDropVector.setName("PacketDropVector");
    packetDropVector.record(0);
    endServiceEvent = new cMessage("endService");
    transferModifier = 1.0;
}

void TransportTx::finish() {
}

void TransportTx::handleMessage(cMessage *msg) {
    // si el mensaje señala termino de servicio
    simtime_t new_data_transfer=0.0;
    if (msg == endServiceEvent) {
        // si hay un paquete en el buffer, manda el siguiente
        if (!buffer.isEmpty()) {
            // desencola el paquete
            cPacket *pkt = (cPacket*) buffer.pop();
            // manda el paquete
            send(pkt, "toOut$o"); // conexion entrada/salida
            // empieza un nuevo servicio
            serviceTime = pkt->getDuration();
            new_data_transfer=serviceTime*transferModifier;
            //calculamos el nuevo data transfer a usar como simulacion
            scheduleAt(simTime() + new_data_transfer, endServiceEvent);
        }
    } else { // si el mensaje son paquetes de datos
        if (buffer.getLength() >= par("bufferSize").intValue()) {
            // dropeamos el paquete
            delete(msg);
            this->bubble("packet-dropped");
            packetDropVector.record(1);
        } else {
            // encolamos el mensaje
            if (msg->getKind() == 2) {
                //se paso de nuestro umbral
                transferModifier = transferModifier*3;
            } else if (msg->getKind() == 3){
                //esta en un nivel aceptable para retomar la velocidad
                transferModifier = transferModifier/3;
            } else {
                // encola el paquete
                buffer.insert(msg);
                bufferSizeVector.record(buffer.getLength());
                // si el servidor esta estatico
                if (!endServiceEvent->isScheduled()) {
                    // empieza el servicio
                    scheduleAt(simTime() + 0, endServiceEvent);
                }
            }
        }
    }
}

#endif
