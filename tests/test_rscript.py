import redis
import rediscript
import os
import json
from os.path import expanduser

from rediscript import write_config
from rediscript import read_config
from rediscript import get_key
from rediscript import put_script
from rediscript import put_script_file
from rediscript import list_scripts
from rediscript import flush_scripts
from rediscript import exec_script
from rediscript import exec_script_from_file
from rediscript import exec_script_from_name

class TestRedisScript():

    def setUp(self):
        self.r = redis.StrictRedis(host='localhost', port=6379, db=0)
        rediscript.REDIS_SCRIPT_PREFIX = 'redis:test:scripts:storage:'
        rediscript.GLOBAL_CONFIG_FILE = os.path.join(expanduser("~"), '.redis-script-test')

    def tearDown(self):
        flush_scripts(self.r)
        try:
            os.remove(rediscript.GLOBAL_CONFIG_FILE)
        except OSError:
            pass

    def test_config(self):
        assert json.dumps(read_config()) == json.dumps(rediscript.DEFAULT_CONFIG)
        write_config('remotehost', 2000, 1)
        print rediscript.GLOBAL_CONFIG_FILE
        assert json.dumps(read_config()) == '{"host": "remotehost", "db": 1, "port": 2000}'

    def test_get_key(self):
        label = 'myscript'
        assert get_key(label) == rediscript.REDIS_SCRIPT_PREFIX + label

    def test_put_script(self):
        put_script(self.r, 'return "Hello World!"', 'hello')
        assert self.r.get(get_key('hello')) != None

    def test_put_script_file(self):
        put_script_file(self.r, 'tests/lua_scripts/counter_lua.lua', 'counter')
        assert self.r.get(get_key('counter')) != None

    def test_list_scripts(self):
        put_script_file(self.r, 'tests/lua_scripts/counter_lua.lua', 'counter')
        assert len(list_scripts(self.r)) == 1

    def test_flush_scripts(self):
        put_script_file(self.r, 'tests/lua_scripts/counter_lua.lua', 'counter')
        flush_scripts(self.r)
        assert len(list_scripts(self.r)) == 0

    def test_exec_script(self):
        assert 'Hello World!' == exec_script(self.r, 'return "Hello World!"')

    def test_exec_script_from_file(self):
        assert 'Hello World!' == exec_script_from_file(self.r, 'tests/lua_scripts/hello_world.lua')

    def test_exec_script_from_name(self):
        put_script(self.r, 'return "Hello World!"', 'hello')
        assert 'Hello World!' == exec_script_from_name(self.r, 'hello')