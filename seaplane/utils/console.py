from subprocess import check_output
from typing import List


def check_output_str(command: List[str], **kwargs) -> str:
    return check_output(command, **kwargs).decode('utf-8')
