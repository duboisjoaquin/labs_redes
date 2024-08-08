#ifndef NET
#define NET

#include <string.h>
#include <omnetpp.h>
#include <packet_m.h>

using namespace omnetpp;

class Net: public cSimpleModule {
private:
    unsigned int nodeCount {0};
    bool countedFlag {false};

    void sendPacket(Packet *pkt);

public:
    Net();
    virtual ~Net();
protected:
    virtual void initialize();
    virtual void finish();
    virtual void handleMessage(cMessage *msg);
};

Define_Module(Net);

#endif /* NET */

Net::Net() {
}

Net::~Net() {
}

void Net::initialize() {
    // create a packet to check de size of the ring
    Packet *sizeCheckPacket = new Packet();

    // seting the kind to 2
    sizeCheckPacket->setKind(2);

    // seting the lenght of the packet to 2B
    sizeCheckPacket->setByteLength(2);

    // seting the count to 0
    sizeCheckPacket->setHopCount(0);

    // setting the source and the destination
    sizeCheckPacket->setSource(this->getParentModule()->getIndex());
    sizeCheckPacket->setDestination(this->getParentModule()->getIndex());

    send(sizeCheckPacket, "toLnk$o", 0);
}

void Net::finish() {
}

void Net::sendPacket(Packet *pkt) {
    // setting the destination and source
    int destination = pkt->getDestination();
    int source = this->getParentModule()->getIndex();

    // calculate the best way
    int clockDistance = (destination - source) % nodeCount;
    int antiClockDistance = nodeCount - clockDistance;

    int out;

    // Checking the shortest path
    if (clockDistance > antiClockDistance) {
        // setting the outgate to 0
        out = 0;
    }
    else{
        // setting the outgate to 1
        out = 1;
    }

    send(pkt, "toLnk$o", out);
}

void Net::handleMessage(cMessage *msg) {

    // All msg (events) on net are packets
    Packet *pkt = (Packet *) msg;


    if (pkt->getKind() == 2 && pkt->getDestination() == this->getParentModule()->getIndex()) {
           // This pkt is cheking the size of the ring
           nodeCount = pkt->getHopCount() + 1;
           countedFlag = true;
           delete (pkt);
    }
    // If this node is the final destination, send to App
    else if (pkt->getDestination() == this->getParentModule()->getIndex()) {
        send(msg, "toApp$o");
    }
    // If not, forward the packet to some else... to who?
    else if (pkt->arrivedOn("toLnk$i")){
        // We send to link interface #0, which is the
        // one connected to the clockwise side of the ring
        // Is this the best choice? are there others?

        pkt->setHopCount(pkt->getHopCount() + 1);

        if (pkt->arrivedOn("toLnk$i", 0)) { // if the pkt arrived on left, send it to right
            send(pkt, "toLnk$o", 1);
        }
        else {
            send(pkt, "toLnk$o", 0);
        }
    }
    else{ // packet sent by app
        sendPacket(pkt);
    }
}
