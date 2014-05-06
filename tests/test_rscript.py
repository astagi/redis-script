import redis
import rediscript
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

import os
from os.path import expanduser

class TestRedisScript():

    def setUp(self):
        self.r = redis.StrictRedis(host='localhost', port=6379, db=0)
        rediscript.REDIS_SCRIPT_PREFIX = 'redis:test:scripts:storage:'
        rediscript.GLOBAL_CONFIG_FILE = os.path.join(expanduser("~"), '.redis-script-test')

    def tearDown(self):
        flush_scripts(self.r)

    def test_write_config(self):
        pass

    def test_read_config(self):
        pass

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
        pass

    def test_exec_script_from_file(self):
        pass

    def test_exec_script_from_name(self):
        pass