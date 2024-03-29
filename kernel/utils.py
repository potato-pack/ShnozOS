from hashlib import sha256
from json import load as l, dump as d
from tools.parser import Parse
from centrl.cmds import *
from tools.error import ERROR, INVALID_CMD, QUOTE
from subprocess import Popen, PIPE


def call_cmd(cmd):
    try:
        process = Popen(cmd, stdout=PIPE, stderr=PIPE)
        stdout, stderr = process.communicate()
        return stdout, stderr
    except FileNotFoundError:
        print(cmd)
        print(ERROR, INVALID_CMD, QUOTE+cmd+QUOTE)




class Shell:
    def __init__(self, fsf: str, data_j: str, data_c:str) -> None:
        self.cd = 'root'
        self.data_j = data_j
        self.data_c = data_c
        self.json = self._load(self.data_j)
        self.call = self._load(self.data_c)
        try:
            if not self.json['user']['username']:
                self._create_user()
        except:
            self._create_user()
        self._username = self.json['user']['username']
        self._passw = self.json['user']['password']
        self.inp_start = f'{self._username}@{self.cd}$ '
        self._jp = data_j.encode('utf-8')
        self._fsf = fsf

            



    
    def _create_user(self):
        print('Please fill this form to create a user')
    

        _username = input('Username: ')
        _passw = input('Password (it will be hashed): ')
        data_to_dump = {
            'user': {
                'username': _username,
                'password': sha256(_passw.encode('utf-8')).hexdigest()
            }
        }
        self._dump(data_to_dump, 'centrl/data.json')
        self.json = self._load('centrl/data.json')


    def execute(self, inp=None):
        if not inp:
            inp = input(self.inp_start)
        self._handle(inp)


    def _handle(self, inp):
        cmd_set_seq = Parse().parse(inp)
        if cmd_set_seq[0] == 'cd':
            # Use the cd func from centrl
            c_d = cd(cmd_set_seq, self)
            self.reload(c_d)

        if cmd_set_seq[0] == 'rsetu':
            rsetu(cmd_set_seq, self)

        if cmd_set_seq[0] == 'udateu':
            udateu(cmd_set_seq, self)

        if cmd_set_seq[0] == 'quit':
            quit()

        if cmd_set_seq[0] == 'ver':
            ver(cmd_set_seq, self)

        if cmd_set_seq[0] == 'github':
            github(cmd_set_seq, self)

        if cmd_set_seq[0] == 'help':
            help(cmd_set_seq, self)

        if cmd_set_seq[0] == 'setenv':
            setenv(cmd_set_seq, self)

        if cmd_set_seq[0] == 'mkenv':
            mkenv(cmd_set_seq, self)

        if cmd_set_seq[0] == 'dlenv':
            dlenv(cmd_set_seq, self)

        if cmd_set_seq[0] == 'new':
            new(cmd_set_seq, self)

        if cmd_set_seq[0] == 'dlete':
            dlete(cmd_set_seq, self)

        if cmd_set_seq[0] == 'lidir':
            lidir(cmd_set_seq, self)

        if cmd_set_seq[0] == 'edit':
            edit(cmd_set_seq, self)

        if cmd_set_seq[0] == 'arth':
            arth(cmd_set_seq, self)

        if not cmd_set_seq[0] in cmds:
            # Cmd not listed so create error
            cmd = self._query_call(cmd_set_seq)
            if cmd:
                call_cmd(cmd[1])
            print(ERROR, INVALID_CMD, QUOTE+cmd_set_seq[0]+QUOTE)
        else:
            print(ERROR, INVALID_CMD, QUOTE+cmd_set_seq[0]+QUOTE)

        self.reload(self.cd)


    def _load(self, path):
        with open(path, 'r') as tempf:
            data = l(tempf)
            tempf.close()

        return data

    
    def _dump(self, data: dict, path):
        with open(path, 'w') as tempf:
            d(data, tempf)
            tempf.close()


    def reload(self, cd):
        self.cd = cd
        self.json = self._load(self.data_j)
        try:
            if not self.json['user']['username']:
                self._create_user()
        except KeyError:
            self._create_user()
        self._username = self.json['user']['username']
        self._passw = self.json['user']['password']
        self.inp_start = f'{self._username}@{self.cd}$ '

    def _query_call(self, cmd_set_seq):
        for cmd in self.call['cmds'][0]:
            if cmd_set_seq == cmd:
                return [cmd[0], cmd[1]]
        return None

    def __delattr__(self, __name: str) -> None:
        self.reload(self.cd)