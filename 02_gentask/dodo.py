import json
from pathlib import Path
from doit.task import clean_targets


FILE_TEXT_PLAN = [("alfa.txt", "you are alfa"),
                  ("beta.txt", "you are BETA")]


class TaskContext(object):
    """Class providing context parameters and handy methods related to
    reporting parameters of source files by means of creating
    JSON files in report directory.
    """
    def __init__(self, source_name, root, report_dir_prefix, priority):
        """
        root (pathlib.Path): root directory where are all source files located
        source_name (str): base name of file to use as input
        report_dir_prefix (str): prefix for directory to write reports to
        priority (int): number to consider
        """
        self.root = root
        self.priority = priority

        self.source = self.root / source_name
        """path to source file (derived from root + source_name)"""

        self.target_dir = self.root / (report_dir_prefix + source_name)
        """target directory"""

        self.target_size_path = self.target_dir / "size.json"
        """path to json file with size information"""

        self.target_mtime_path = self.target_dir / "mtime.json"
        """path to json file with mtime information"""

        self.target_alldata_path = self.target_dir / "alldata.json"
        """path to json file with alldata information"""

    def ensure_target_dir(self):
        self.target_dir.mkdir(parents=True, exist_ok=True)
        return True

    def remove_target_dir(self):
        if self.target_dir.exists():
            self.target_dir.rmdir()
        return True

    def write_size(self):
        """write to {target}/size.json information about source size"""
        data = {"name": str(self.source),
                "size": self.source.stat().st_size}
        with self.target_size_path.open("w") as f:
            json.dump(data, f)
        return True

    def write_mtime(self):
        """write to {target}/mtime.json information about source mtime"""
        data = {"name": str(self.source),
                "mtime": self.source.stat().st_mtime}
        with self.target_mtime_path.open("w") as f:
            json.dump(data, f)
        return True

    def write_alldata(self):
        """write to {target}/alldata.json all information about source"""
        source_stat = self.source.stat()
        data = {"name": str(self.source),
                "size": source_stat.st_size,
                "mtime": source_stat.st_mtime,
                "priority": self.priority}
        with self.target_alldata_path.open("w") as f:
            json.dump(data, f)
        return True

    def task_report(self, topics, clean=True):
        topic_action_target = {
            "size": (self.write_size, self.target_size_path),
            "mtime": (self.write_mtime, self.target_mtime_path),
            "alldata": (self.write_alldata, self.target_alldata_path),
        }
        return {
            "name": self.source.name,
            "file_dep": [self.source],
            "actions": [self.ensure_target_dir] +
                       [topic_action_target[topic][0] for topic in topics],
            "targets": [topic_action_target[topic][1] for topic in topics],
            "clean": [clean_targets, self.remove_target_dir],
        }


def write_file(path, text):
    """Write `text` value into py.path.local file path.
    """
    path.write_text(text, "utf-8")
    return True


def task_create_file():
    """Create file with given name and content.
    """
    for target_name, text in FILE_TEXT_PLAN:
        target = Path(target_name)
        yield {
            "name": target_name,
            "actions": [(write_file, [target, text])],
            "targets": [target],
            "clean": True,
        }


def task_report_file_size():
    """Report file size by JSON file in report directory."""
    for file_name, _ in FILE_TEXT_PLAN:
        context = TaskContext(file_name,
                              root=Path(),
                              report_dir_prefix="report_file_size_",
                              priority=123)
        yield context.task_report(topics=["size"])


def task_report_file_mtime():
    """Report file mtime by JSON file in report directory.
    """
    for file_name, _ in FILE_TEXT_PLAN:
        context = TaskContext(file_name,
                              root=Path(),
                              report_dir_prefix="report_file_mtime_",
                              priority=123)
        yield context.task_report(topics=["mtime"])


def task_report_file_complete():
    """Report multiple file parameters into set of JSON files in report dir.
    """
    for file_name, _ in FILE_TEXT_PLAN:
        context = TaskContext(file_name,
                              root=Path(),
                              report_dir_prefix="report_file_complete_",
                              priority=123)
        yield context.task_report(topics=["size", "mtime", "alldata"])
