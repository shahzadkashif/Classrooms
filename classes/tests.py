from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from classes.models import Classroom, Student


class ModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="admin",
            password='adminadmin',
            )
        self.user.set_password(self.user.password)
        self.user.save()

    def test_create(self):
        classroom = Classroom.objects.create(
            teacher= self.user,
            subject="Science",
            grade=5,
            year="2018",
            )
        student = Student.objects.create(
            name="Laila",
            dob="1995-01-02",
            exam_grade=100,
            classroom=classroom,
            )


class SigninTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(
            username="admin",
            password='1234567890-=',
            )

    def test_url(self):
        url = reverse("signin")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_valid_signin(self):
        url = reverse("signin")
        data = {"username":"admin", "password":"1234567890-="}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)

    def test_invalid_signin(self):
        url = reverse("signin")
        data = {"username":"admin", "password":"1234567890-"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "admin")

    def test_base(self):
        url = reverse("signin")
        response = self.client.get(url)
        self.assertTemplateUsed(response, "base.html")
        self.assertTemplateUsed(response, "navbar.html")
        self.assertContains(response, reverse("signin"))
        self.assertContains(response, reverse("signup"))
        self.assertNotContains(response, reverse("signout"))


class SignupTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(
            username="admin",
            password='1234567890-=',
            )

    def test_url(self):
        url = reverse("signup")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_valid_signup(self):
        url = reverse("signup")
        data = {"username":"admin2", "password":"1234567890-="}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)

    def test_invalid_signup(self):
        url = reverse("signup")
        data = {"username":"admin", "password":"1234567890-="}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "admin")

    def test_base(self):
        url = reverse("signup")
        response = self.client.get(url)
        self.assertTemplateUsed(response, "base.html")
        self.assertTemplateUsed(response, "navbar.html")
        self.assertContains(response, reverse("signin"))
        self.assertContains(response, reverse("signup"))
        self.assertNotContains(response, reverse("signout"))


class SignoutTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(
            username="admin",
            password='1234567890-=',
            )

    def test_url(self):
        self.client.login(username="admin", password="1234567890-=")
        url = reverse("signout")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)


class CreateClassroomTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="admin",
            password='1234567890-=',
            )

    def test_url(self):
        self.client.login(username="admin", password="1234567890-=")
        url = reverse("classroom-create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_url_redirect(self):
        url = reverse("classroom-create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("signin"))

    def test_valid_create(self):
        self.client.login(username="admin", password="1234567890-=")
        data = {
            "subject":"Science",
            "grade":5,
            "year":"2018"
        }
        url = reverse("classroom-create")
        response = self.client.post(url, data)
        classrooms = Classroom.objects.all()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(classrooms.count(), 1)
        self.assertEqual(classrooms.first().teacher, self.user)
        self.assertEqual(classrooms.first().subject, data["subject"])
        self.assertEqual(classrooms.first().grade, data["grade"])
        self.assertEqual(classrooms.first().year, data["year"])

    def test_invalid_create(self):
        self.client.login(username="admin", password="1234567890-=")
        data = {
            "subject":"Science",
            "grade":5,
            "year":""
        }
        url = reverse("classroom-create")
        response = self.client.post(url, data)
        classrooms = Classroom.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(classrooms.count(), 0)
        self.assertContains(response, data["subject"])
        self.assertContains(response, data["grade"])


class ClassroomDetailTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="admin",
            password='1234567890-=',
            )
        cls.user2 = User.objects.create_user(
            username="admin2",
            password='1234567890-=',
            )
        cls.classroom = Classroom.objects.create(
            teacher= cls.user,
            subject="Science",
            grade=5,
            year="2018",
            )
        cls.students = []
        for i in range(0,5):
            cls.students.append(
                Student.objects.create(
                    name=f"Laila-{i}",
                    dob="1995-01-02",
                    exam_grade=100,
                    classroom=cls.classroom,
                    gender="F"
                )
            )

    def test_url(self):
        url = reverse("classroom-detail", kwargs={"classroom_id": 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code ,200)

    def test_displayed_info(self):
        url = reverse("classroom-detail", kwargs={"classroom_id": 1})
        response = self.client.get(url)

        self.assertContains(response, self.classroom.subject)
        self.assertContains(response, self.classroom.grade)
        self.assertContains(response, self.classroom.year)

        for student in self.students:
            self.assertContains(response, student.name)
            self.assertContains(response, student.exam_grade)

    def test_shown_buttons(self):
        url = reverse("classroom-detail", kwargs={"classroom_id": 1})
        response = self.client.get(url)
        self.assertNotContains(response, reverse("student-create", kwargs={"classroom_id": 1}))
        self.assertNotContains(response, reverse("student-update", kwargs={"classroom_id": 1, "student_id": 1}))
        self.assertNotContains(response, reverse("student-delete", kwargs={"classroom_id": 1, "student_id": 1}))

        self.client.login(username="admin", password="1234567890-=")
        url = reverse("classroom-detail", kwargs={"classroom_id": 1})
        response = self.client.get(url)
        self.assertContains(response, reverse("student-create", kwargs={"classroom_id": 1}))
        for student in self.students:
            self.assertContains(response, reverse("student-update", kwargs={"classroom_id": 1, "student_id": student.id}))
            self.assertContains(response, reverse("student-delete", kwargs={"classroom_id": 1, "student_id": student.id}))

    def test_base(self):
        url = reverse("classroom-detail", kwargs={"classroom_id": 1})
        response = self.client.get(url)
        self.assertTemplateUsed(response, "base.html")
        self.assertTemplateUsed(response, "navbar.html")
        self.assertContains(response, reverse("signin"))
        self.assertContains(response, reverse("signup"))
        self.assertNotContains(response, reverse("signout"))


class StudentCreateTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="admin",
            password='1234567890-=',
            )
        cls.user2 = User.objects.create_user(
            username="admin2",
            password='1234567890-=',
            )
        cls.classroom = Classroom.objects.create(
            teacher= cls.user,
            subject="Science",
            grade=5,
            year="2018",
            )

    def test_create(self):
        self.client.login(username="admin", password="1234567890-=")
        url = reverse("student-create", kwargs={"classroom_id": 1})
        data = {
            "name":"Laila",
            "dob":"1995-01-02",
            "exam_grade":100,
            "gender":"F"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code ,302)
        students = Student.objects.filter(classroom_id=1)
        self.assertEqual(students.count(), 1)
        self.assertEqual(students[0].name, data["name"])
        self.assertEqual(students[0].exam_grade, data["exam_grade"])


class StudentUpdateTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="admin",
            password='1234567890-=',
            )
        cls.user2 = User.objects.create_user(
            username="admin2",
            password='1234567890-=',
            )
        cls.classroom = Classroom.objects.create(
            teacher= cls.user,
            subject="Science",
            grade=5,
            year="2018",
            )
        cls.students = []
        for i in range(0,5):
            cls.students.append(
                Student.objects.create(
                    name=f"Laila-{i}",
                    dob="1995-01-02",
                    exam_grade=100,
                    classroom=cls.classroom,
                    gender="F"
                )
            )

    def test_url(self):
        self.client.login(username="admin", password="1234567890-=")
        student = self.students[0]
        url = reverse("student-update", kwargs={"classroom_id": 1, "student_id": student.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update(self):
        self.client.login(username="admin", password="1234567890-=")
        student = self.students[0]
        url = reverse("student-update", kwargs={"classroom_id": 1, "student_id": student.id})
        data = {
            "name":"Laila",
            "dob":"1995-01-02",
            "exam_grade":10,
            "gender":"F"
        }
        response = self.client.post(url, data)
        student = Student.objects.get(id=self.students[0].id)
        self.assertEqual(student.exam_grade, data["exam_grade"])


class StudentDeleteTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="admin",
            password='1234567890-=',
            )
        cls.user2 = User.objects.create_user(
            username="admin2",
            password='1234567890-=',
            )
        cls.classroom = Classroom.objects.create(
            teacher= cls.user,
            subject="Science",
            grade=5,
            year="2018",
            )
        cls.students = []
        for i in range(0,5):
            cls.students.append(
                Student.objects.create(
                    name=f"Laila-{i}",
                    dob="1995-01-02",
                    exam_grade=100,
                    classroom=cls.classroom,
                    gender="F"
                )
            )

    def test_delete(self):
        self.client.login(username="admin", password="1234567890-=")
        student = self.students[0]
        url = reverse("student-delete", kwargs={"classroom_id": 1, "student_id": student.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

