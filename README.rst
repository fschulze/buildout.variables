buildout.variables
==================

Provides dynamic variables in buildouts.

An example use are unique DB names and conflict free parallel continuous integration runs on one machine.

Example buildout section::

    [variables]
    recipe = buildout.variables
    index-file = ${env:HOME}/jenkins-buildout-index.json
    index-start = 0
    index-key = ${env:JOB_NAME}
    portbase = indexed 12{index}00
    port = int ${portbase} 0:100
    port-instance = new port
    jobname = str "${env:JOB_NAME}" [^a-zA-Z0-9] _

    [env]
    recipe = gocept.recipe.env

There are several things going on here.

The first are the ``index-`` options. They provide you with the possiblity to get unique indices based on a key and stored in a shared file. That way each buildout gets the same index for each key used. In the example above the key is the JOB_NAME environment variable (set by Jenkins for example) and the index starts at 0. If a buildout with a different JOB_NAME is run, then it will get the next free index.

The ``portbase`` option evaluates "12{index}00".format(index=index). Thus the
first job will get 12000 and the second job 12100 and so on.

The ``port`` option declares a range of integers which can be used to get unique ports for whatever you need them for. The ``port-instance`` option uses that to declare a port which can be used with ${variables:port-instance} throughout the buildout and would be 12000 in this example. If you declare more, then up to 12099 will be possible before you get an error. Which variable
gets which port is determined by lexical order of the variable name.

The ``jobname`` option takes ${env:JOB_NAME} and runs re.sub on it. In this example everything besides letters and numbers is replaced by an underscore.

Besides integer ranges you can't use other dynamic variables from the same section.

Credits
=======

Thanks to Legacy Parts Corporation and http://enquos.com for which this package was initially created.