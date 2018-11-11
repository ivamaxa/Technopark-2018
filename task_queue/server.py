import argparse
import socket
import time
import uuid
import pickle
from datetime import datetime, timedelta
from collections import deque
import os


class TaskQueueServer:

    def __init__(self, ip, port, path, timeout):
        self.path = path
        self.timeout = timeout
        self.ip = ip
        self.port = port
        self.queue_dict = {}
        self.queue_get = {}

    def run(self):
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        connection.bind((self.ip, self.port))
        connection.listen(1)

        while True:
            current_connection, address = connection.accept()
            data = current_connection.recv(1000000)
            if not data:
                break

            data_list = data.decode('utf8').split()
            answer = None
            if data_list[0] == 'ADD':
                answer = self.add(data_list)

            elif data_list[0] == 'IN':
                answer = self.in_queue(data_list[1], data_list[2])

            elif data_list[0] == 'GET':
                answer = self.get(data_list[1])

            elif data_list[0] == 'ACK':
                answer = self.ack(data_list[1], data_list[2])

            elif data_list[0] == 'SAVE':
                if self.save():
                    current_connection.send(b'OK')
                    break
            else:
                current_connection.send(b'ERROR')
                break

            if type(answer) is bool:
                if answer:
                    current_connection.send(b'YES')
                else:
                    current_connection.send(b'NO')
            else:
                current_connection.send(answer.encode('ascii'))

            current_connection.close()

    def add(self, data_list):
        str_id = str(uuid.uuid4())
        dict_queue = {
            'queue': data_list[1],
            'length': data_list[2],
            'data': data_list[3],
            'id': str_id,
            'time': None

        }
        if not self.check(dict_queue['queue']):
            self.queue_dict[dict_queue['queue']] = deque()
            self.queue_get[dict_queue['queue']] = {}
        self.queue_dict[dict_queue['queue']].append(dict_queue)
        return str_id

    def get(self, queue):
        if not self.check(queue):
            conn.send(b'NONE')
        task = self.queue_dict[queue].popleft()
        task['time'] = datetime.now()
        self.queue_get[queue][task['id']] = task
        result_str = "{} {} {}".format(task['id'], task['length'], task['data'])
        return result_str

    def ack(self, queue, str_id):
        ack_queue = False
        if str_id in self.queue_get[queue].keys():
            if datetime.now() - self.queue_get[queue][str_id]['time'] <= timedelta(seconds=server.timeout):
                del self.queue_get[queue][str_id]
                ack_queue = True

        return ack_queue

    def in_queue(self, queue, str_id):
        if not self.check(queue):
            return False

        queue_in = False
        if str_id in self.queue_get[queue].keys():
            queue_in = True
        else:
            for i in self.queue_dict[queue]:
                if str_id == i['id']:
                    queue_in = True
        return queue_in

    def save(self):
        with open(os.path.join(self.path, 'queue'), 'wb') as f:
            pickle.dump(self.queue_dict, f)
        return True

    def check(self, queue):
        if queue not in self.queue_dict:
            return False
        return True




def parse_args():
    parser = argparse.ArgumentParser(description='This is a simple task queue server with custom protocol')
    parser.add_argument(
        '-p',
        action="store",
        dest="port",
        type=int,
        default=5555,
        help='Server port')
    parser.add_argument(
        '-i',
        action="store",
        dest="ip",
        type=str,
        default='0.0.0.0',
        help='Server ip adress')
    parser.add_argument(
        '-c',
        action="store",
        dest="path",
        type=str,
        default='./',
        help='Server checkpoints dir')
    parser.add_argument(
        '-t',
        action="store",
        dest="timeout",
        type=int,
        default=300,
        help='Task maximum GET timeout in seconds')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    server = TaskQueueServer(**args.__dict__)
    server.run()
