===============
gentask variant
===============

Plan of things to do is in global variable `FILE_TEXT_PLAN`.

TaskContext class allows:

- creating context for one source file processing
- ensure_target_dir and remove_target_dir

- PLUS: task_report method can generate task dictionary (actions, targets...)

Task dictionary is created by call to context method `task_report`.
