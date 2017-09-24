======================
Doit TaskContext study
======================

This is a study on how to provide task context data by means of TaskContext class.

This is just a study of possible solution and the name TaskContext is completely
arbitrary.

Challenge:

- have number of actions in single task, which shall share some common
  parameters.
- propose constructs allowing to share these parameters in a clean way.

Sample set of tasks:

- few files ("alfa.txt", "beta.txt") are created
- for each file, create various sets of reports (JSON files) reporting
  their size, mtime etc.
- The parameter "priority" is useded just to illustrate any other params
  can be maintained for the context.
- the task "report_file_complete" shows reuse of task context in multiple
  actions (within one task).
- other tasks (using task context) have single action only, but even in
  this case it shall be clear, that the TaskContext instance is able
  encapsulating relevant data and functionality in a clear way.

Installation and use
====================

Assuming you have python 3.6 and tox installed.

Note: If you have other python versions, simply modify `tox.ini` file.

To create the environment run::

    $ tox

After installation, cd to the directory with a `dodo.py` file.
Currently there are more variants.

This creates virtual env in `.tox/py36`. Activate it::

    $ source .tox/py36/bin/activate
    (py36)$

Use it as usually with doit. Start listing tasks::

    (py36)$ doit list
    create_file            Create file with given name and content.
    report_file_complete   Report multiple file parameters into set of JSON files in report dir.
    report_file_mtime      Report file mtime by JSON file in report directory.
    report_file_size       Report file size by JSON file in report directory.

and continue listing them really all::

    (py36)$ doit list --all
    create_file                     Create file with given name and content.
    create_file:alfa.txt            
    create_file:beta.txt            
    report_file_complete            Report multiple file parameters into set of JSON files in report dir.
    report_file_complete:alfa.txt   
    report_file_complete:beta.txt   
    report_file_mtime               Report file mtime by JSON file in report directory.
    report_file_mtime:alfa.txt      
    report_file_mtime:beta.txt      
    report_file_size                Report file size by JSON file in report directory.
    report_file_size:alfa.txt       
    report_file_size:beta.txt       

Run the tasks and play with it
==============================
Do it::

    (py36)$ doit
    .  create_file:alfa.txt
    .  create_file:beta.txt
    .  report_file_size:alfa.txt
    .  report_file_size:beta.txt
    .  report_file_mtime:alfa.txt
    .  report_file_mtime:beta.txt
    .  report_file_complete:alfa.txt
    .  report_file_complete:beta.txt

You can also call `clean` and `forget`.

Try deleting some of created files and rerun the `doit`.

Note, that the solution has small bug: the mtime is not updated in second run and further on as `doit`
is comparing input files disregarding modification time. There are solutions but this is not in
scope of this study.

Discussion about parametrization
================================

`TaskContext` class
-------------------

Put relevant task parameters into `__init__` constructor.

Calculate dependent parameters by means of class properties.

For actions to perform implement class method. Note, that it if you plan to use it as an action in
`doit`, there are rules for returned values which notify `doit` that all went well. This is the
reason some of the methods return `True`.

There is no need to implement all actions by class methods. There is also no need to use all of the
methods in `doit`. Just do what seems practical.

Big advantage of `TaskContext` type of classes is, that they are easy to test independently from
`doit` tasks.

Global variables
----------------
To keep common configuration data across multiple tasks, global variables are often neede.

Here it is the case for `FILE_TEXT_PLAN` variable.

KISS (especially planning the doit tasks)
-----------------------------------------
The best is keep most of the complexity out of `task_{taskname}` code.

The most important is to keep the returned (or yielded) result simple.
