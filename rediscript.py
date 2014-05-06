import redis
import argparse
from os.path import expanduser
import os

GLOBAL_CONFIG_FILE = os.path.join(expanduser("~"), '.redis-script')
REDIS_SCRIPT_PREFIX = 'redis:scripts:storage:'
DEFAULT_CONFIG = {'host':'localhost', 'db':0, 'port':6379}

def __safe_len(arg):
    try:
        return len(arg)
    except TypeError:
        return 0

def __safe_list(lst):
    if lst:
        return lst
    else:
        return []

def write_config(host, db, port):
    config = read_config()
    if host:
        config['host'] = host
    if db:
        config['db'] = db
    if port:
        config['port'] = port
    try:
        f.open('w', GLOBAL_CONFIG_FILE).write(json.dump(config))
    except:
        pass

def read_config():
    try:
        config = json.loads(f.open('r', GLOBAL_CONFIG_FILE).read())
        return config
    except:
        return DEFAULT_CONFIG

def get_key(name):
    return REDIS_SCRIPT_PREFIX + name

def put_script(r, script, name):
    scriptobj = r.register_script(script)
    r.set(get_key(name), scriptobj.sha)

def put_script_file(r, file_path, name):
    script = file(file_path).read()
    put_script(r, script, name)

def list_scripts(r):
    keys = r.keys(pattern=REDIS_SCRIPT_PREFIX + '*')
    id_start = __safe_len(REDIS_SCRIPT_PREFIX)
    labels = []
    for key in keys:
        labels.append(key[id_start:])
    return labels

def flush_scripts(r):
    r.script_flush()
    keys = r.keys(pattern=REDIS_SCRIPT_PREFIX + '*')
    for key in keys:
        r.delete(key)

def exec_script(r, script, keys=[], args=[]):
    return r.eval(script, __safe_len(keys), *(__safe_list(keys) + __safe_list(args)))

def exec_script_from_file(r, file_path, keys=[], args=[]):
    script = file(file_path).read()
    return exec_script(r, script, keys, args)

def exec_script_from_name(r, name, keys=[], args=[]):
    sha = r.get(get_key(name))
    return r.evalsha(sha, __safe_len(keys), *(__safe_list(keys) + __safe_list(args)))

def parse_commands():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='sub-command help', dest='command')

    parser_config = subparsers.add_parser('config', help='config help')
    parser_config.add_argument('-host', type=str, help='host help')
    parser_config.add_argument('-db', type=str, help='db help')
    parser_config.add_argument('-port', type=str, help='port help')

    parser_put = subparsers.add_parser('put', help='put help')
    parser_put_subparser = parser_put.add_subparsers(help='sub-command help', dest='put_command')

    parser_put_file = parser_put_subparser.add_parser('file', help='file help')
    parser_put_file.add_argument('file', type=str, help='file path')
    parser_put_file.add_argument('name', type=str, help='script name')

    parser_put_script = parser_put_subparser.add_parser('script', help='script help')
    parser_put_script.add_argument('script', type=str, help='script def')
    parser_put_script.add_argument('name', type=str, help='script name')

    parser_list = subparsers.add_parser('list', help='list help')

    parser_flush = subparsers.add_parser('flush', help='flush help')

    parser_exec = subparsers.add_parser('exec', help='exec help')
    parser_exec_subparser = parser_exec.add_subparsers(help='sub-command exec', dest='exec_command')

    parser_exec_file = parser_exec_subparser.add_parser('file', help='x help')
    parser_exec_file.add_argument('file', type=str, help='file path')
    parser_exec_file.add_argument('-k', nargs='+', type=str, help='keys')
    parser_exec_file.add_argument('-a', nargs='+', type=str, help='arguments')

    parser_exec_script = parser_exec_subparser.add_parser('script', help='x help')
    parser_exec_script.add_argument('script', type=str, help='script def')
    parser_exec_script.add_argument('-k', nargs='+', type=str, help='keys')
    parser_exec_script.add_argument('-a', nargs='+', type=str, help='arguments')

    parser_exec_name = parser_exec_subparser.add_parser('alias', help='x help')
    parser_exec_name.add_argument('name', type=str, help='name def')
    parser_exec_name.add_argument('-k', nargs='+', type=str, help='keys')
    parser_exec_name.add_argument('-a', nargs='+', type=str, help='arguments')

    return parser.parse_args()

def main():
    config = read_config()
    r = redis.StrictRedis(**(config))
    args = parse_commands()
    if args.command == 'config':
        write_config(args.host, args.db, args.port)
    if args.command == 'put':
        if args.put_command == 'file':
            put_script_file(r, args.file, args.name)
        elif args.put_command == 'script':
            put_script(r, args.script, args.name)
    elif args.command == 'list':
        for label in list_scripts(r):
            print label
    elif args.command == 'flush':
        flush_scripts(r)
    elif args.command == 'exec':
        if args.exec_command == 'file':
            print exec_script_from_file(r, args.file, args.k, args.a)
        elif args.exec_command == 'script':
            print exec_script_from_name(r, args.script, args.k, args.a)
        elif args.exec_command == 'alias':
            print exec_script_from_name(r, args.name, args.k, args.a)

if __name__ == "__main__":
    main()