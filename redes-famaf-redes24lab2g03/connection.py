# encoding: utf-8
# Revisión 2019 (a Python 3 y base64): Pablo Ventura
# Copyright 2014 Carlos Bederián
# $Id: connection.py 455 2011-05-01 00:32:09Z carlos $

from constants import *
from base64 import b64encode
import os


class Connection(object):
    """
    Conexión punto a punto entre el servidor y un cliente.
    Se encarga de satisfacer los pedidos del cliente hasta
    que termina la conexión.
    """

    def __init__(self, socket, directory):
        # FALTA: Inicializar atributos de Connection
        self.socket = socket
        self.directory = directory
        self.connec = True
        self.buffer = ""


    def quit(self):
        # Cierra la conexion con el cliente
        res = self._codes(CODE_OK)
        self.connec = False
        self._send(res)

    def get_file_listing(self):
        res = self._codes(CODE_OK) + EOL

        try:
            # recorre archivos en self.directory
            for file in os.listdir(self.directory):
                aux = file + EOL
                res += aux

            self._send(res)
        except FileNotFoundError:
            res = self._codes(BAD_REQUEST)
            self._send(res)

    def get_metadata(self, filename):
        res = self._codes(CODE_OK) + EOL
        try:
            # Chequeamos validez del nombre del archivo
            if not self._is_valid(filename):
                res = self._codes(INVALID_ARGUMENTS)
            # chequeamos si el archivo existe
            elif filename in os.listdir(self.directory):
                file_path = os.path.join(self.directory, filename)
                data = os.path.getsize(file_path)
                res += str(data)
            else:
                res = self._codes(FILE_NOT_FOUND)
        except FileNotFoundError:  # De no existir el directorio, devolvemos BAD_REQUEST
            res = self._codes(BAD_REQUEST)

        self._send(res)

    def get_slice(self, filename, offset, size):
        try:
            # Chequeamos validez del nombre del archivo
            if not self._is_valid(filename):
                res = self._codes(INVALID_ARGUMENTS)
                self._send(res)
            # chequeamos si el archivo existe
            elif filename in os.listdir(self.directory):
                file_path = os.path.join(self.directory, filename)
                file_size = os.path.getsize(file_path)

                # Chequeamos si el offset excede el tamaño del archivo
                if (file_size < offset + size) or (offset < 0):
                    res = self._codes(BAD_OFFSET)
                else:
                    res = self._codes(CODE_OK)  # 0 ok code
                    self._send(res)
                    # Abrimos el archivo y leemos el slice
                    with open(file_path, "rb") as file:  # r de read, b de binary
                        # Seek nos permite movernos a una posicion especifica del archivo
                        file.seek(offset)

                        b_remaining = size
                        while b_remaining > 0:
                            b_read = file.read(b_remaining)
                            b_remaining -= len(b_read)
                            self._sendb64(b_read)

                    eol = ''
                    # Agregamos el /r/n al final de lo enviado en base 64
                    self._send(eol)
            else:
                res = self._codes(FILE_NOT_FOUND)

        except FileNotFoundError:  # De no existir el directorio, devolvemos BAD_REQUEST
            res = self._codes(BAD_REQUEST)
            self._send(res)

    def handle(self):
        """
        Atiende eventos de la conexión hasta que termina.
        """
        while self.connec:
            command = self._parser()
            if '\n' in command:  # Si el comando tiene un \n, es un bad eol
                res = self._codes(BAD_EOL)
                self._send(res)
            else:
                if len(command) > 0:
                    try:
                        self._fun_analizer(command)
                    except RuntimeError:  # caso raro que falle el send
                        res = self._codes(INTERNAL_ERROR)
                        self._send(res)

        self.socket.close()

    def _fun_analizer(self, command):
        # Analiza la funcion que se quiere ejecutar
        if len(command) == 0:
            self._send(self._codes(CODE_OK))
        else:
            command = command.split()  # separa por espacios en un array
            # el nombre de la funcion se guarda en el primer lugar del arreglo
            function = command[0]

            if function == "quit":
                if len(command) > 1:  # Si el comando tiene mas de un argumento, es invalido
                    res = self._codes(INVALID_ARGUMENTS)
                    self._send(res)
                else:
                    self.quit()
            # lista los archivos dentro del directorio del objeto (self.directory)
            elif function == "get_file_listing":
                if len(command) > 1:  # Si el comando tiene mas de un argumento, es invalido
                    res = self._codes(INVALID_ARGUMENTS)
                    self._send(res)
                else:
                    self.get_file_listing()
            # toma el nombre de la funcion y el nombre de un archivo y llama a la funcion metadata (devuelve el size del archivo)
            elif function == "get_metadata":
                if len(command) != 2:  # Malformacion del comando
                    res = self._codes(INVALID_ARGUMENTS)
                    self._send(res)
                else:
                    filename = command[1]
                    if type(filename) != str:
                        res = self._codes(INVALID_ARGUMENTS)
                        self._send(res)
                    else:
                        self.get_metadata(filename)
            elif function == "get_slice":  # divide desde un offset hasta un size de un archivo
                if(len(command) != 4):  # Malformacion del comando
                    res = self._codes(INVALID_ARGUMENTS)
                    self._send(res)
                else:
                    try:  # chequea excepciones de tipo de datos
                        filename = command[1]
                        offset = int(command[2])
                        size = int(command[3])
                        if type(filename) != str:
                            res = self._codes(INVALID_ARGUMENTS)
                            self._send(res)
                        else:
                            self.get_slice(filename, offset, size)
                    except ValueError:
                        res = self._codes(INVALID_ARGUMENTS)
                        self._send(res)
            else:
                res = self._codes(INVALID_COMMAND)
                self._send(res)

    def _parser(self):
        # recibe de a 4096 bytes de info hasta que se encuentre con EOL o no reciba nada del cliente
        while self.connec and EOL not in self.buffer:
            data = self.socket.recv(4096).decode("ascii")
            self.buffer += data
            if len(data) == 0:
                self.connec = False

        # vemos si el while termino poque no recibio nada o si fue porque recibio el final de linea
        if EOL in self.buffer:
            # En req guardo el comando y en buffer lo que sigue despues del EOL
            req, self.buffer = self.buffer.split(EOL, 1)
            return req.strip()  # Saco los espacios en blanco
        else:
            self.connec = False
            return ""

    def _send(self, msg):
        # Envia un mensaje al servidor
        msg = msg + EOL
        msg = msg.encode("ascii")  # Codificamos el mensaje

        while len(msg) > 0:
            b_sent = self.socket.send(msg)
            if b_sent == 0:
                raise RuntimeError("socket connection broken")
            msg = msg[b_sent:]

    def _sendb64(self, msg):
        # Envia un mensaje codificado en base64 al servidor
        msg = b64encode(msg)
        while len(msg) > 0:
            # print(msg)
            b_sent = self.socket.send(msg)
            if b_sent == 0:
                raise RuntimeError("socket connection broken")
            msg = msg[b_sent:]

    def _is_valid(self, filename: str):
        # Verificamos si el nombre de un archivo es valido
        # Restamos el conjunto de caracteres validos al conjunto de caracteres del nombre
        chars = set(filename) - VALID_CHARS
        # Usamos sets para que no haya caracteres repetidos
        # Si chars es vacio, entonces el nombre es valido
        return (len(chars) == 0)


    def _codes(self, code):
        # Devuelve el mensaje correspondiente al codigo
        assert valid_status(code)
        if fatal_status(code):
            self.connec = False
        return f"{code} {error_messages[code]}"