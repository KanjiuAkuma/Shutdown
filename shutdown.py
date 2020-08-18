"""
Created by Joscha Vack on 8/18/2020.
"""

import argparse
import json
import os
import re
import sys

desc = """\
Basic usage:
> shutdown.py [time]
    Shuts windows down after time

Time Format:
    Simple:
        (d+(d|m|h|s))+
        - Order does not matter.
        - Every identifier should only be used once

    Advanced:
        (?<d>\\d+)?(^|,)(?<h>\\d+)?(^|$|:)(?<m>\\d+)?($|\\.)(?<s>\\d+)?
        If only one number is given its assumed to be hours.

Named configs:
To create a named config issue a shutdown command as stated in basic usage and add the [-a | -add] [name] parameter to it 
Instead of executing the shutdown command it will be saved and accessible via name instead of a time pattern
eg:
    > shutdown.py 1h -add default
    > shutdown.py default
        -> will shut down the pc after one hour
        
To edit a config user [-a | -add] [name] with the --o flag
eg:
    > shutdown.py 1h 30m -a default --o

To remove a named config use the [-r | -rem] [name] parameter
eg:
    > shutdown -rem default
"""

_config_path = 'cfg.json'

# check if cfg exists
if not os.path.exists(_config_path):
    with open(_config_path, 'w+') as f:
        f.write('{}')

# load cfg
with open(_config_path, 'r') as f:
    cfg = json.load(f)


def parseTimeString(time: str) -> int:
    """
    Simple Format:
        (d+(d|m|h|s))+
        - Order does not matter.
        - Every identifier should only be used once

    Advanced Format:
        (?<d>\\d+)?(^|,)(?<h>\\d+)?(^|$|:)(?<m>\\d+)?($|\\.)(?<s>\\d+)?
        If only one number is given its assumed to be hours.

    :param time: Time as string in described format
    :return: time in seconds
    :rtype: int
    """

    # try parse with identifiers first
    m = re.match(r'((?P<d>\d+)d)?((?P<h>\d+)h)?((?P<m>\d+)m)?((?P<s>\d+)s)?', time)
    # try parse with advanced pattern if first failed
    if not m.group(0):
        m = re.match(r'(?P<d>\d+)?(^|,)(?P<h>\d+)?(^|$|:)(?P<m>\d+)?($|\.)(?P<s>\d+)?', time)

    if not m:
        return -1

    val = 0
    if m['d']:
        val += int(m['d']) * 24 * 60 * 60
    if m['h']:
        val += int(m['h']) * 60 * 60
    if m['m']:
        val += int(m['m']) * 60
    if m['s']:
        val += int(m['s'])
    return val


def accept(argv: list):
    parser = argparse.ArgumentParser(
        prog='Shutdown',
        description='Shutdown utility with named configurations',
        epilog=desc,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('cmd',
                        nargs='*',
                        help='Time after which to shut down or name of named config. For information on time format use -h')
    parser.add_argument('-l',
                        dest='list',
                        action='store_true',
                        help='Prints a list of all named configurations')
    parser.add_argument('-a', '-add',
                        metavar='name',
                        dest='add',
                        help='Add named configuration')
    parser.add_argument('-r', '-rem',
                        metavar='name',
                        dest='rem',
                        help='Delete named configuration')
    parser.add_argument('--a', '--abort',
                        dest='abort',
                        action='store_true',
                        help='Abort shutdown')
    parser.add_argument('--o',
                        dest='overwrite',
                        action='store_true',
                        help='Overwrite existing config')

    args = parser.parse_args(argv)
    if args.abort:
        # abort shutdown
        print('Aborting shutdown')
        os.system('shutdown /a')
        return
    if args.list:
        # print list of all configs
        print('Named configurations:')
        for k, v in cfg.items:
            print('\t%s: %s' % (k, v))
        return
    if args.add:
        cmd_args = [arg for arg in argv if arg not in ['-a', '-add', args.add]]
        if args.add not in cfg or args.overwrite or input('Config %s already exists: %s.\nOverwrite? (y|n) ' % (args.add, cfg[args.add])).lower() == 'y':
            name = args.add.lower()
            cfg[name] = cmd_args
            with open(_config_path, 'w') as f:
                json.dump(cfg, f)
            print('Saved config %s: %s' % (name, ' '.join(cmd_args)))
        return
    if args.rem:
        name = args.rem.lower()
        if cfg.pop(name, False):
            with open(_config_path, 'w') as f:
                json.dump(cfg, f)
            print('Removed config %s' % name)
        else:
            print('Config %s not found' % name)
        return
    cmd_str = ' '.join(args.cmd)
    if cmd_str in cfg:
        # is named config
        accept(cfg[cmd_str])
    else:
        time_s = parseTimeString(cmd_str)
        if time_s != -1:
            # is valid time
            print('Shutting down in %ds' % time_s)
            os.system('shutdown /s /t %d' % time_s)
        else:
            print("Command '%s' is neither a named config nor a valid time." % cmd_str)


if __name__ == '__main__':
    accept(sys.argv[1:])
    accept('2:10 -a default'.split(' '))
    accept('2:30 -a default --o'.split(' '))
    accept('default'.split(' '))
    accept('--a'.split(' '))
    accept('-r default'.split(' '))
    accept('default'.split(' '))
    accept('1,1:1.1'.split(' '))
    accept('--abort'.split(' '))
    accept('1h 2m 30s'.split(' '))
    accept('--abort'.split(' '))
    accept('2:10 -a default'.split(' '))
