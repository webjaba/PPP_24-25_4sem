"""."""
import socket
import sys
from serialization.serializer import Serializer
from serialization.deserializer import Deserializer
from net.proto_abc import AbstractProtocolHandler
from net.proto import ProtocolHandler

# asd
class ClientServer:
    """."""

    def __init__(self, ip, port) -> None:
        """."""
        self.ip = ip
        self.port = port
        self.serializer = Serializer()
        self.deserializer = Deserializer()
        self.protocol: AbstractProtocolHandler = ProtocolHandler()

    def handle_query(self, conn, query: str) -> None:
        """."""
        serialized_query = self.serializer.serialize_str(query)
        self.protocol.send(conn, serialized_query)
        print('msg was sended')

    def recv_response(self, conn):
        """."""
        print('recieving data')
        data = self.protocol.recv(conn=conn)
        print(f'data was recieved: {len(data)}')
        d = self.deserializer.deserialize(data)
        print(d)
        return d

    def run(self) -> None:
        """."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.ip, self.port))
            self.handle_input(s)

    def handle_input(self, conn):
        """."""
        while True:
            msg = input('type "commands" for more information: ')
            match msg:
                case 'commands':
                    print(
                        'i - information',
                        's - enter to sql mode',
                        'q - exit from sql mode or exit from programm',
                        sep='\n'
                    )
                case 'i':
                    print(
                        'your sql query should looks like this:',
                        'SELECT <column1>, <column2>, <column3> FROM <table> WHERE <column1> > 0.5',
                        'SELECT <column1>, <column2>, <column3> FROM <table>',
                        'example:',
                        'SELECT * FROM table1',
                        'SELECT name, age FROM testtable WHERE (age > 0.5) AND (len(name) < 5)',
                        'SELECT * FROM metatable',
                        sep='\n'
                    )
                case 's':
                    msg = input('enter sql query here ("q" = exit): ')
                    if msg == 'q':
                        continue
                    else:
                        self.handle_query(conn, msg)
                        try:
                            self.recv_response(conn)
                        except ValueError:
                            print('empty data')
                case 'q':
                    print('program has closed')
                    sys.exit(1)
