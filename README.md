Shutdown
===

Shutdown utility with named configurations
by Kanjiu Akuma

Usage
===
```
positional arguments:
  
  cmd                 Time after which to shut down or name of named config. For information on time format use -h

optional arguments:
  -h, --help          show this help message and exit
  -l                  Prints a list of all named configurations
  -a name, -add name  Add named configuration
  -r name, -rem name  Delete named configuration
  --a, --abort        Abort shutdown
  --o                 Overwrite existing config
 ```

Basic usage:
---
```
> shutdown.py [time]
    Shuts windows down after time
```

Time Format:
---
```
    - Simple:
        (d+(d|m|h|s))+
        - Order does not matter.
        - Every identifier should only be used once    
    - Advanced:
        (?<d>\d+)?(^|,)(?<h>\d+)?(^|$|:)(?<m>\d+)?($|\.)(?<s>\d+)?
        If only one number is given its assumed to be hours.
```

Named configs
---
> To create a named config issue a shutdown command as stated in basic usage
> and add the [-a | -add] [name] parameter to it
> Instead of executing the shutdown command it will be saved and accessible 
> via name instead of a time pattern

    > shutdown.py 1h -add default
    > shutdown.py default
        -> will shut down the pc after one hour

> To edit a config user [-a | -add] [name] with the --o flag

    > shutdown.py 1h 30m -a default --o

> To remove a named config use the [-r | -rem] [name] parameter

    > shutdown -rem default

