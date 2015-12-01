#!/usr/bin/env python
'''
Usage: keytool.py set <slot> <algo> <algoparam>
       keytool.py get

WARNING: THIS DESTROYS THE KEY IN THE SPECIFIED SLOT!

Slot can be one of:
  - sig/s/1: Signature key
  - enc/e/2: Encryption key
  - auth/a/3: Authentication key

Algorithm can be one of:
  - rsa/1
  - ecdh/18
  - ecdsa/19
  - eddsa/22

Algoparam for RSA must be "rsa<bits>"
Algoparam for ECDH/ECDSA/EDDS must be a curve name.

Possible curve names: cv25519, ed25519, nistp256, nistp384, nistp512,
    brainpoolP256r1, brainpoolP384r1, brainpoolP512r1, secp256k1

'''
import six
import subprocess
from docopt import docopt
from getpass import getpass

ALGOS = {
    'rsa': 1,
    'ecdh': 18,
    'ecdsa': 19,
    'eddsa': 22,
}

SLOTS = {
    'sig': 1,
    's': 1,
    'enc': 2,
    'e': 2,
    'auth': 3,
    'a': 3,
}


class AgentError(Exception):
    pass


class Agent(object):
    def __init__(self):
        self._proc = None

    def __del__(self):
        if self._proc:
            self._proc.kill()

    def _read(self, inquire_cb=None):
        lines = []
        while True:
            resp = self._proc.stdout.readline().rstrip()
            lines.append(resp.decode())
            if resp.startswith(b'INQUIRE'):
                data = None
                if inquire_cb:
                    _, key, msg = resp.split(b' ', 2)
                    data = inquire_cb(key, msg)
                if data is not None:
                    to_write = [b'D ']
                    for c in six.iterbytes(data):
                        to_write.append('%{:02x}'.format(c).encode())
                    self._write(b''.join(to_write))
                    self._write(b'END')
                else:
                    self._write(b'CAN')
            elif resp.startswith(b'OK'):
                break
            elif resp.startswith(b'ERR'):
                raise AgentError(resp.decode())
        return lines

    def _spawn(self):
        self._proc = subprocess.Popen(['/usr/libexec/scdaemon', '--multi-server'],
                                      stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        self._read()

    def _write(self, line):
        if not self._proc:
            self._spawn()
        self._proc.stdin.write(line + b'\r\n')
        self._proc.stdin.flush()

    def command(self, line, inquire_cb=None):
        self._write(line.encode())
        return self._read(inquire_cb=inquire_cb)


_admin_pin = None


def _admin_pin_cb(key, msg):
    global _admin_pin
    if key == b'NEEDPIN':
        if _admin_pin is None:
            _admin_pin = getpass('Admin PIN: ').encode() + b'\x00'
        return _admin_pin
    return None


def main():
    args = docopt(__doc__)
    if args['set']:
        try:
            slot = SLOTS[args['<slot>']]
        except KeyError:
            slot = int(args['<slot>'])
        try:
            algo = ALGOS[args['<algo>']]
        except KeyError:
            algo = int(args['<algo>'])
        agent = Agent()
        result = agent.command('SETATTR KEY-ATTR --force  {:d} {:d} {}'.format(
            slot, algo, args['<algoparam>']), inquire_cb=_admin_pin_cb)
        print(result[-1])
    elif args['get']:
        agent = Agent()
        for line in agent.command('GETATTR KEY-ATTR'):
            print(line)

if __name__ == '__main__':
    main()
