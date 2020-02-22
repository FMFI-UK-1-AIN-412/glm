import os
from typing import List, Optional, Any, Dict

from remote.context import Context


def get_pull_requests(context: Context, filters: Optional[Dict[str, Any]] = None) -> List["PullRequest"]:
    from student.student import Student
    from core.config_loader import directory_path

    pulls = []
    for student_pulls_dir in os.listdir(directory_path("pulls/")):
        student = Student(student_pulls_dir)
        for student_pull_file in os.listdir(student.pulls_directory()):
            pr = context.get_pull_request(context, student_pull_file, student)
            if pr.passes_filters(filters):
                pulls.append(pr)

    return pulls
