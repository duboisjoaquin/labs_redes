#!/usr/bin/env python
# encoding: utf-8
# Revisión 2019 (a Python 3 y base64): Pablo Ventura
# Revisión 2014 Carlos Bederián
# Revisión 2011 Nicolás Wolovick
# Copyright 2008-2010 Natalia Bidart y Daniel Moisset
# $Id: server.py 656 2013-03-18 23:49:11Z bc $

import optparse
import socket
import connection
import sys
from constants import *
import threading


class Server(object):
    """
    El servidor, que crea y atiende el socket en la dirección y puerto
    especificados donde se reciben nuevas conexiones de clientes.
    """

    def __init__(self, addr=DEFAULT_ADDR, port=DEFAULT_PORT,
                 directory=DEFAULT_DIR):
        print("Serving %s on %s:%s." % (directory, addr, port))
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((addr, port))

        self.addr = addr
        self.port = port
        self.directory = directory
        # Creacion de un semaforo con tope para limitar la cantidad de hilos
        self.thread = threading.BoundedSemaphore(MAX_THREADS)
        self.thread_use = 0

    def serve(self):
        """
        Loop principal del servidor. Se acepta una conexión a la vez
        y se espera a que concluya antes de seguir.
        """
        self.server_socket.listen()

        while True:
            # FALTA: Aceptar una conexión al server, crear una
            # Connection para la conexión y atenderla hasta que termine.
            client_socket, client_adress = self.server_socket.accept()
            connec = connection.Connection(client_socket, self.directory)
            if self.thread_use < MAX_THREADS:
                self.thread_use += 1
                self.client_handler(connec)
            else:
                connec._send(connec._codes(SERVER_BUSSY))
                client_socket.close()

    def client_handler(self, connec: connection.Connection):
        """
        manejador de clientes, se encarga de crear un hilo para cada cliente
        """

        self.thread.acquire()
        t = threading.Thread(target=self.thread_using, args=(connec,))
        t.start()

    def thread_using(self, connec: connection.Connection):
        """
        usamos try finally para asegurarnos de que el semaforo se libere
        cuando el hilo termine y dar paso a otro hilo
        """
        try:
            connec.handle()
        finally:
            self.thread.release()
            self.thread_use -= 1


def main():
    """Parsea los argumentos y lanza el server"""

    parser = optparse.OptionParser()
    parser.add_option(
        "-p", "--port",
        help="Número de puerto TCP donde escuchar", default=DEFAULT_PORT)
    parser.add_option(
        "-a", "--address",
        help="Dirección donde escuchar", default=DEFAULT_ADDR)
    parser.add_option(
        "-d", "--datadir",
        help="Directorio compartido", default=DEFAULT_DIR)

    options, args = parser.parse_args()
    if len(args) > 0:
        parser.print_help()
        sys.exit(1)
    try:
        port = int(options.port)
    except ValueError:
        sys.stderr.write(
            "Numero de puerto invalido: %s\n" % repr(options.port))
        parser.print_help()
        sys.exit(1)

    server = Server(options.address, port, options.datadir)
    server.serve()


if __name__ == '__main__':
    main()
