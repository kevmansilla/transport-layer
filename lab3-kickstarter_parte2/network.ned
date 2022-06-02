simple Generator
{
    parameters:
        volatile int packetByteSize;
        volatile double generationInterval; // sec
        @display("i=block/source");
    gates:
        output out;
}

simple Queue
{
    parameters:
        volatile int bufferSize;
        volatile int serviceTime; // sec
        @display("i=block/queue;q=buffer");
    gates:
        input in;
        output out;
}

simple TransportTx {
    parameters:
        int bufferSize;
        @display("i=block/queue;q=buffer");
    gates:
        input toApp;
        inout toOut;
}

simple TransportRx {
    parameters:
        int bufferSize;
        @display("i=block/queue;q=buffer");
    gates:
        output toApp;
        inout toOut;
}

simple Sink
{
    parameters:
        @display("i=block/sink");
    gates:
        input in;
}

module NodeTx
{
    parameters:
        @display("i=block/routing");
    gates:
        inout iout;
    submodules:
        gen: Generator {
            parameters:
                @display("p=75,55");
        }
        traTx: TransportTx {
            parameters:
                @display("p=75,190");
        }
    connections:
        gen.out --> traTx.toApp;
        traTx.toOut$o --> iout$o;
        iout$i --> traTx.toOut$i;
}

module NodeRx
{
    parameters:
        @display("i=block/routing");
    gates:
        inout iout;
    submodules:
        sink: Sink {
            parameters:
                @display("p=75,50");
        }

        traRx: TransportRx {
        	parameters:
        	    @display("p=75,190");
        }
    connections:
        iout$i --> traRx.toOut$i;
        //case study 1
       	//traRx.toApp --> { datarate = 0.5Mbps; } --> sink.in;
        //case study 2
        traRx.toApp --> { datarate = 1Mbps; } --> sink.in;
        traRx.toOut$o --> iout$o;
}

network Network
{
    @display("bgl=2");
    submodules:
        nodeTx: NodeTx {
            @display("p=30,30");
        }
        queue1: Queue {
            @display("p=130,30");
        }
        queue2: Queue {
            @display("p=130,100");
        }
        nodeRx: NodeRx {
            @display("p=230,30");
        }
    connections:
        nodeTx.iout$o --> { datarate = 1Mbps; delay = 100us; } --> queue1.in;
        //case study 1
        //queue1.out --> { datarate = 1Mbps; delay = 100us; } --> nodeRx.iout$i;
        //case study 2
        queue1.out --> { datarate = 0.5Mbps; delay = 100us; } --> nodeRx.iout$i;
        nodeRx.iout$o --> queue2.in;
        queue2.out --> nodeTx.iout$i;
}
