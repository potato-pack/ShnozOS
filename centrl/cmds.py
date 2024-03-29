from tools.error import *
from tools.parser import Parse
from hashlib import sha256
from .version import *
from shutil import rmtree
from os import mkdir, remove, path, walk

cmds = [
    'cd', 'rsetu', 'quit', 'udateu', 'github', 'ver', 'setenv', 'mkenv',
    'dlenv', 'help', 'arth', 'new', 'dlete', 'edit', 'lidir', 'newcmd'
]

def cd(cmd_set_seq, instance):
    """`instance` must be of type Shell"""
    if instance.cd:
        try:
            p = 'centrl\\'+instance.cd+'\\'+cmd_set_seq[1]
            if cmd_set_seq[1] == '../':
                back_p = Parse().parse(instance.cd, sep='\\')[0]
                cd_into_back_p = 'centrl\\'+back_p
                if not back_p:
                    return instance.cd
                    
                if path.isdir(cd_into_back_p):
                    return f'{back_p}'
                else:
                    print(ERROR, DIR_NOT_FOUND, back_p+'.', 
                    'Cannot cd into dir')
                    return instance.cd
            
            if path.isdir(p):
                return f'{instance.cd}\\{cmd_set_seq[1]}'
            else:
                print(ERROR, DIR_NOT_FOUND, instance.cd+'\\'+cmd_set_seq[1]+'.', 
                'Cannot cd into dir')
                return instance.cd
        except IndexError:
            pass
    else:
        raise ShellInstanceError(FATAL_ERR, instance, IS_NOT, OF_TYPE, SHELL)


def rsetu(cmd_set_seq, instance):
    """`instance` must be of type Shell"""
    if instance.json:
        d = instance.json
        del d['user']['username']
        del d['user']['password']
        instance.dump(d, 'centrl/data.json')
    else:
        raise ShellInstanceError(FATAL_ERR, instance, IS_NOT, OF_TYPE, SHELL)


def udateu(cmd_set_seq, instance):
    """`instance` must be of type Shell"""
    # TODO fix if user did not make any paramerters
    if instance.json:
        d = instance.json
        try:
            d['user']['username'] = cmd_set_seq[1]
            d['user']['password'] = sha256(cmd_set_seq[2].encode('utf-8')).hexdigest()
        except IndexError:
            d['user']['username'] = input('Username: ')
            d['user']['password'] = sha256(input('Password (it will be hashed): ').encode('utf-8')).hexdigest()
        instance.dump(d, 'centrl/data.json')
    else:
        raise ShellInstanceError(FATAL_ERR, instance, IS_NOT, OF_TYPE, SHELL)


def ver(cmd_set_seq, instance):
    print(version)


def github(cmd_set_seq, instance):
    print(github_link)


def setenv(cmd_set_seq, instance):
    if instance.json:
        try:
            env_var_name = cmd_set_seq[1]
            val = cmd_set_seq[2]
            d = instance.json
            try:
                if instance.json['env'][env_var_name]:
                    d['env'][env_var_name] = val
                    instance.dump(d, 'centrl/data.json')
            except KeyError:
                print(ERROR, INVALID_ENV_VAR, QUOTE+env_var_name+QUOTE)
        except IndexError:
            print(ERROR, 'No environment variable name and value not defined')
    else:
        raise ShellInstanceError(FATAL_ERR, instance, IS_NOT, OF_TYPE, SHELL)


def mkenv(cmd_set_seq, instance):
    if instance.json:
        try:
            try:
                env_var_name = cmd_set_seq[1]
                val = cmd_set_seq[2]
                d = instance.json
                d['env'][env_var_name] = val
            except KeyError:
                d['env'] = {}
                env_var_name = cmd_set_seq[1]
                val = cmd_set_seq[2]
                d = instance.json
                d['env'][env_var_name] = val
            instance.dump(d, 'centrl/data.json')
        except IndexError:
            print(ERROR, 'No environment variable name and value not defined')
    else:
        raise ShellInstanceError(FATAL_ERR, instance, IS_NOT, OF_TYPE, SHELL)


def dlenv(cmd_set_seq, instance):
    if instance.json:
        d = instance.json
        ensure_password_is_right(instance)
        try:
            try:
                env_var_name = cmd_set_seq[1]
                del d['env'][env_var_name]
            except KeyError:
                d['env'] = {}
                env_var_name = cmd_set_seq[1]
                del d['env'][env_var_name]
            instance.dump(d, 'centrl/data.json')
        except IndexError:
            print(ERROR, 'No environment variable name and value not defined')
    else:
        raise ShellInstanceError(FATAL_ERR, instance, IS_NOT, OF_TYPE, SHELL)


def new(cmd_set_seq, instance):
    if instance.cd:
        try:
            if path.splitext(cmd_set_seq[1])[1]:
                if cmd_set_seq[2]:
                    p = 'centrl\\'+cmd_set_seq[2]+'\\'+cmd_set_seq[1]
                    try:
                        if cmd_set_seq[2] == "root":
                            print(ERROR, INVALID_CMD+": Cannot create file in root dir")
                        else:
                            with open(p, 'x') as tempf:
                                pass
                    except FileExistsError:
                        print(ERROR, FILE_EXISTS, cmd_set_seq[2]+'\\'+cmd_set_seq[1]+'.', 
                        'Cannot create new file')
                else:
                    p = 'centrl\\'+instance.cd+'\\'+cmd_set_seq[1]
                    try:
                        if instance.cd == "root":
                            print(ERROR, INVALID_CMD+": Cannot create file in root dir")
                        else:
                            with open(p, 'x') as tempf:
                                pass
                    except FileExistsError:
                        print(ERROR, FILE_EXISTS, instance.cd+'\\'+cmd_set_seq[1]+'.', 
                        'Cannot create new file')
            else:
                p = 'centrl\\'+instance.cd+'\\'+cmd_set_seq[1]
                try:
                    mkdir(p)
                except FileExistsError:
                    print(ERROR, FILE_EXISTS, p+'.', 'Cannot create new file')
        except IndexError:
            print(ERROR, MISSING_ARG, '1.', 'Cannot run new')
    else:
        raise ShellInstanceError(FATAL_ERR, instance, IS_NOT, OF_TYPE, SHELL)


def dlete(cmd_set_seq, instance):
    if instance.cd:
        try:
            try:
                p = 'centrl\\'+instance.cd+'\\'+cmd_set_seq[1]
                if path.splitext(cmd_set_seq[1])[1]:
                    remove(p)
                else:
                    rmtree(p, ignore_errors=True)
            except FileNotFoundError:
                print(ERROR, FILE_NOT_FOUND, instance.cd+'\\'+cmd_set_seq[1], 
                'Cannot run dlete')
        except IndexError:
            print(ERROR, MISSING_ARG, '1.', 'Cannot run dlete')
    else:
        raise ShellInstanceError(FATAL_ERR, instance, IS_NOT, OF_TYPE, SHELL)

def edit(cmd_set_seq, instance):
    if instance.cd:
        try:
            p = 'centrl\\'+instance.cd+'\\'+cmd_set_seq[1]
            if path.splitext(cmd_set_seq[1])[1]:
                if cmd_set_seq[2] == 'true':
                    try:
                        with open(p, 'a') as tempf:
                            lines = []
                            print('-------- edit --------')
                            while True:
                                line = input()
                                if line == '*done*':
                                    break
                                else:
                                    lines.append(line+'\n')
                            tempf.writelines(lines)

                    except FileNotFoundError:
                        print(ERROR, FILE_NOT_FOUND, instance.cd+'\\'+cmd_set_seq[1]+'.', 
                        'Cannot edit file')
                else:
                    try:
                        with open(p, 'w') as tempf:
                            lines = []
                            print('-------- edit --------')
                            while True:
                                line = input()
                                if line == '*done*':
                                    break
                                else:
                                    lines.append(line+'\n')
                            tempf.writelines(lines)

                    except FileNotFoundError:
                        print(ERROR, FILE_NOT_FOUND, instance.cd+'\\'+cmd_set_seq[1]+'.', 
                        'Cannot edit file')
            else:
                print(ERROR, CANNOT_EDIT, p, 'is a directory. Cannot edit')
        except IndexError:
            print(ERROR, MISSING_ARG, '1.', 'Cannot run new')
    else:
        raise ShellInstanceError(FATAL_ERR, instance, IS_NOT, OF_TYPE, SHELL)

def help(cmd_set_seq, instance):
    try:
        if cmd_set_seq[1] in cmds:
            print('Find help here:', github_link+'/wiki/'+'Commands/')
    except:
        print(ERROR, MISSING_ARG)


def arth(cmd_set_seq, instance):
    try:
        if cmd_set_seq[2] == '+':
            print(int(cmd_set_seq[1])+float(cmd_set_seq[3]))
    except Exception as e:
        print(e)


def lidir(cmd_set_seq, instance):
    if instance.cd:
        try:
            p = 'centrl\\'+instance.cd+'\\'
            print(f'Inside {p}')
            if (instance.cd == "root"):
                for root, dirs, files in walk(p, topdown=False):
                    #for name in files:
                    #    print(f'{p}\\{name}')
                    for name in dirs:
                        print(f'{p}\\{name}')
                        for root, dirs, files in walk(f'{p}\\{name}', topdown=True):
                            for fname in files:
                                print(f'{p}\\{name}\\{fname}')
            else:
                for root, dirs, files in walk(p, topdown=False):
                    for name in dirs:
                        print(f'{p}\\{name}')
                        for root2, dirs2, files2 in walk(f'{p}\\{name}', topdown=True):

                            for fname2 in files2:
                                print(f'{p}\\{name}\\{fname}')
                    for name in files:
                        print(f'{p}\\{name}')

        except IndexError:
            print(ERROR, MISSING_ARG, '1.', 'Cannot run new')
    else:
        raise ShellInstanceError(FATAL_ERR, instance, IS_NOT, OF_TYPE, SHELL)


        

def ensure_password_is_right(instance):
    json = instance.json
    getting_password = True
    while getting_password:
        pss = input('Password: ')
        if not sha256(pss.encode()).hexdigest() == json['user']['password']:
            print('Wrong password')
            continue
        else:
            getting_password = False