Redis.script
============

A simple command line tool to manage your Redis scripts easily using aliases

How to use
----------

    $ redis-script put script 'return "Hello World!"' hello

    $ redis-script put file 'counter_lua.lua' counter

    $ redis-script exec alias hello

    $ redis-script exec alias counter -k ... -a ...