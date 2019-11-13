import unittest
import student.student as Student
import core.core as Core
from remote.remote import Remote

class StudentTesting(unittest.TestCase):
    def test_create(self):
        students = [("testing01", "bachler-testing-student"), ("testing02", "bachler-testing-student")]
        Student.add_student_repos(students, False)

        active_students = Core.active_students()
        for i in range(len(students)):
            self.assertEqual(active_students[i][0], students[i][0])
            self.assertEqual(active_students[i][1], students[i][1])

    def test_delete(self):
        return
        students = [("testing01", "bachler-testing-student"), ("testing02", "bachler-testing-student")]
        for student in students:
            Student.delete_repo(student[0])

        active_students = Core.active_students()
        for active_student in active_students:
            self.assertNotIn(active_student, students)

        remote = Remote()
        for student in students:
            self.assertIsNone(remote.get_user_repo(student[0]))


if __name__ == '__main__':
    unittest.main()
