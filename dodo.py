import json
from pathlib import Path


FILE_TEXT_PLAN = [("alfa.txt", "you are alfa"),
                  ("beta.txt", "you are BETA")]


class TaskContext(object):
    """Class providing context parameters and handy methods related
    reporting parameters of source files by means of creating
    JSON files in report directory.
    """
    def __init__(self, root, source_name, target_name, priority):
        """
        root (pathlib.Path): root directory where are all files located
        source_name (str): base name of file to use as input
        target_name (str): name of root subdir to write targest to
        priority (int): number to consider
        """
        self.root = root
        self.source_name = source_name
        self.target_name = target_name
        self.priority = priority

    @property
    def source_path(self):
        """pathlib.Path to source file"""
        return self.root / self.source_name

    @property
    def target_dir(self):
        """pathlib.Path target dir.

        If the directory does not exists, it attempts to create it.
        """
        path = self.root / self.target_name
        path.mkdir(parents=True, exist_ok=True)
        return path

    @property
    def target_size_path(self):
        """pathlib.Path json with size information"""
        return self.target_dir / "size.json"

    @property
    def target_mtime_path(self):
        """pathlib.Path json with mtime information"""
        return self.target_dir / "mtime.json"

    @property
    def target_alldata_path(self):
        """pathlib.Path to json with alldata information"""
        return self.target_dir / "alldata.json"

    def write_size(self):
        """write to {target}/size.json information about source size"""
        source_path = self.source_path
        data = {"name": str(source_path),
                "size": source_path.stat().st_size}
        with self.target_size_path.open("w") as f:
            json.dump(data, f)
        return True

    def write_mtime(self):
        """write to {target}/mtime.json information about source mtime"""
        source_path = self.source_path
        data = {"name": str(source_path),
                "mtime": source_path.stat().st_mtime}
        with self.target_mtime_path.open("w") as f:
            json.dump(data, f)
        return True

    def write_alldata(self):
        """write to {target}/alldata.json all information about source"""
        source_path = self.source_path
        source_path_st = source_path.stat()
        data = {"name": str(source_path),
                "size": source_path_st.st_size,
                "mtime": source_path_st.st_mtime,
                "priority": self.priority}
        with self.target_alldata_path.open("w") as f:
            json.dump(data, f)
        return True


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
    root = Path()  # this is current directory
    for file_name, _ in FILE_TEXT_PLAN:
        source = Path(file_name)
        report_dir = "report_file_size-" + source.name
        priority = 123
        context = TaskContext(root, file_name, report_dir, priority)
        yield {
            "name": source.name,
            "file_dep": [source],
            "actions": [(context.write_size)],
            "targets": [context.target_size_path],
            "clean": True,
        }


def task_report_file_mtime():
    """Report file mtime by JSON file in report directory.
    """
    root = Path()  # this is current directory
    for file_name, _ in FILE_TEXT_PLAN:
        source = Path(file_name)
        report_dir = "report_file_mtime-" + source.name
        priority = 123
        context = TaskContext(root, file_name, report_dir, priority)
        yield {
            "name": source.name,
            "file_dep": [source],
            "actions": [(context.write_mtime)],
            "targets": [context.target_mtime_path],
            "clean": True,
        }


def task_report_file_complete():
    """Report multiple file parameters into set of JSON files in report dir.
    """
    root = Path()  # this is current directory
    for file_name, _ in FILE_TEXT_PLAN:
        source = Path(file_name)
        report_dir = "report_file__complete-" + source.name
        priority = 123
        context = TaskContext(root, file_name, report_dir, priority)
        yield {
            "name": source.name,
            "file_dep": [source],
            "actions": [(context.write_size),
                        (context.write_mtime),
                        (context.write_alldata),
                        ],
            "targets": [context.target_size_path,
                        context.target_mtime_path,
                        context.target_alldata_path,
                        ],
            "clean": True,
        }
