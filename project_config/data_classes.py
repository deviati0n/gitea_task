from dataclasses import dataclass


@dataclass
class GiteaOptions:
    local_root_url: str

    @property
    def root_url(self) -> str:
        return self.local_root_url


@dataclass
class TestOptions:
    chrome_path: str
    repo_name: str
    file_name: str
    file_msg: str

    @property
    def get_chrome_path(self) -> str:
        return self.chrome_path

    @property
    def get_repo_name(self) -> str:
        return self.repo_name

    @property
    def get_file_name(self) -> str:
        return self.file_name

    @property
    def get_file_msg(self) -> str:
        return self.file_msg
