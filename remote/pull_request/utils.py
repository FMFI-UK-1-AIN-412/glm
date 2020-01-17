import os
from typing import List, Tuple, Optional, Any, Dict

from remote.context import Context


def get_pull_requests(context: Context, filters: Optional[Dict[str, Any]] = None):
    from student.student import Student
    from core.config_loader import directory_path
    from remote.pull_request.pull_request import PullRequest

    pulls = []
    for student_pulls_dir in os.listdir(directory_path("pulls/")):
        student = Student(student_pulls_dir)
        for student_pull_file in os.listdir(student.pulls_directory()):
            pr = PullRequest(context, student_pull_file, student)
            if pr.passes_filters(filters):
                pulls.append(pr)

    return pulls
