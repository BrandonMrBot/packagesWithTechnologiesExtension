List of packages with QR - Showing technologies
==============

Getting Started
---------------

- Activate the ClimMob environment.
```
$ . ./path/to/ClimMob/bin/activate
```

- Change directory into your newly created plugin.
```
$ cd packagesWithTechnologiesExtension
```

- Build the plugin
```
$ python setup.py develop
```

- Add the plugin to the ClimMob list of plugins by editing the following line in development.ini or production.ini
```
    #climmob.plugins = examplePlugin
    climmob.plugins = packagesWithTechnologiesExtension
```

- Run ClimMob again
