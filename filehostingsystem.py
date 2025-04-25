from datetime import datetime
import copy


class File:
    def __init__(self, name: str, size: int, timestamp: datetime, ttl: datetime):
        self.name = name
        self.size = size
        self.timestamp = timestamp
        self.ttl = ttl


class Directory:
    def __init__(self, name: str):
        self.name = name
        self.children = {}  # key: name, value: File or Directory

    def add(self, item):
        if item.name in self.children:
            raise RuntimeError(f"{item.name} already exists.")
        self.children[item.name] = item

    def get(self, name):
        if name not in self.children:
            raise Exception("Name does not exist.")
        return self.children[name]

    def delete(self, name):
        if name not in self.children:
            raise Exception("Name does not exist.")
        del self.children[name]


class Server:
    def __init__(self, name: str):
        self.name = name
        self.root = Directory(name)
        self.state_history = {}  # key: timestamp, value: self.root

    def _parse_path(self, path: str):
        return path.split("/")

    def _get_parent_dir(self, path_parts):
        current = self.root
        for part in path_parts[:-1]:
            current = current.get(part)
            if not isinstance(current, Directory):
                raise RuntimeError("Invalid path.")
        return current

    def _recursive_dfs(self, current_dir: Directory, prefix: str):
        """returns all files that include prefix"""
        all_files = []
        for key, value in current_dir.children.items():
            if isinstance(value, File) and value.name.startswith(prefix):
                all_files.append(value)
            if isinstance(value, Directory):
                all_files.extend(self._recursive_dfs(value, prefix))
        return all_files

    def _save_state(self, timestamp: datetime):
        self.state_history[timestamp] = copy.deepcopy(self.root)

    def FILE_UPLOAD_AT(
        self, timestamp: datetime, file_path: str, size: int, ttl: datetime | None
    ):
        path_parts = self._parse_path(file_path)
        file_name = path_parts[-1]
        parent = self._get_parent_dir(path_parts)
        if file_name in parent.children:
            raise RuntimeError("File already exists.")
        parent.add(File(file_name, size, timestamp, ttl))
        self._save_state(timestamp)

    def FILE_GET_AT(self, timestamp: datetime, file_path: str):
        path_parts = self._parse_path(file_path)
        file_name = path_parts[-1]
        parent = self._get_parent_dir(path_parts)
        file = parent.get(file_name)
        file.timestamp = timestamp
        self._save_state(timestamp)
        return file.size if isinstance(file, File) else None

    def FILE_COPY_AT(self, timestamp: datetime, source: str, dest: str):
        path_parts_source = self._parse_path(source)
        path_parts_dest = self._parse_path(dest)
        source_dir = self._get_parent_dir(path_parts_source)
        dest_dir = self._get_parent_dir(path_parts_dest)
        source_file = source_dir.get(path_parts_source[-1])
        dest_file = File(
            path_parts_dest[-1], source_file.size, timestamp, source_file.ttl
        )  # copy file with src ttl
        if dest_file.name in dest_dir.children:
            dest_dir.delete(dest_file.name)
        dest_dir.add(dest_file)
        source_file.timestamp = timestamp
        self._save_state(timestamp)

    def FILE_SEARCH_AT(self, timestamp: datetime, prefix: str):
        prefix_list = self._recursive_dfs(self.root, prefix)
        not_dead = [f for f in prefix_list if not f.ttl or f.ttl > timestamp]
        for f in not_dead:
            f.timestamp = timestamp
        not_dead.sort(key=lambda f: (-f.size, f.name))
        self._save_state(timestamp)
        return [(f.name, f.size) for f in not_dead[:10]]

    def ROLLBACK(self, timestamp: datetime):
        valid_timestamps = [t for t in self.state_history if t <= timestamp]
        if not valid_times:
            raise RuntimeError("No rollback state found.")
        closest = max(valid_times)
        self.root = copy.deepcopy(self.state_history[closest])
