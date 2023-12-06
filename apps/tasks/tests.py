from datetime import timedelta
from io import BytesIO

from django.contrib.admin.sites import AdminSite
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.test import TestCase
from django.test.client import RequestFactory
from django.urls import resolve, reverse
from django.utils import timezone

from apps.contests.models import Contest
from apps.submissions.forms import SubmissionForm
from apps.submissions.models import Submission, SubmissionStatus
from apps.tasks.admin import TaskAdmin, TaskModelForm
from apps.tasks.models import Task
from apps.tasks.views import DetailView, handle_submission
from apps.users.models import User


class TaskTestCase(TestCase):
    def test_task_to_string(self) -> None:
        task = Task(title="Test Task")
        self.assertEqual(str(task), "Test Task")

    def test_running_contest_is_accessible(self) -> None:
        now = timezone.now()

        start_time = now - timedelta(hours=1)
        end_time = now + timedelta(hours=1)

        contest = Contest(start_time=start_time, end_time=end_time)
        task = Task(contest=contest)

        self.assertTrue(task.is_accessible)

    def test_past_contest_is_accessible(self) -> None:
        now = timezone.now()

        start_time = now - timedelta(hours=2)
        end_time = now - timedelta(hours=1)

        contest = Contest(start_time=start_time, end_time=end_time)
        task = Task(contest=contest)

        self.assertTrue(task.is_accessible)

    def test_future_contest_is_not_accessible(self) -> None:
        now = timezone.now()

        start_time = now + timedelta(hours=1)
        end_time = now + timedelta(hours=2)

        contest = Contest(start_time=start_time, end_time=end_time)
        task = Task(contest=contest)

        self.assertFalse(task.is_accessible)

    def test_cancelled_contest_is_not_accessible(self) -> None:
        now = timezone.now()

        start_time = now - timedelta(hours=1)
        end_time = now + timedelta(hours=1)

        contest = Contest(
            start_time=start_time,
            end_time=end_time,
            cancelled=True,
        )
        task = Task(contest=contest)

        self.assertFalse(task.is_accessible)


class TaskAdminTestCase(TestCase):
    def setUp(self) -> None:
        now = timezone.now()

        self.site = AdminSite()
        self.admin = TaskAdmin(Task, self.site)

        self.contest = Contest._default_manager.create(
            title="Test Contest 1",
            description="This is a test contest",
            start_time=now,
            end_time=now + timedelta(hours=1),
            cancelled=False,
        )

    def test_list_display(self) -> None:
        list_display = self.admin.list_display
        expected = ("title", "contest", "memory_limit", "time_limit")

        self.assertEqual(list_display, expected)

    def test_list_filter(self) -> None:
        list_filter = self.admin.list_filter
        expected = ("contest", "score")

        self.assertEqual(list_filter, expected)

    def test_fieldsets(self) -> None:
        fieldsets = self.admin.fieldsets

        expected = [
            (("General"), {"fields": ("title", "description", "constraints")}),
            (("Meta"), {"fields": ("contest", "score")}),
            (("Limits"), {"fields": ("memory_limit", "time_limit")}),
            ("Test case", {"fields": ("input_file", "output_file")}),
        ]

        self.assertEqual(fieldsets, expected)

    def test_save_model(self) -> None:
        title = "Example task"
        description = "Some example task"
        constraints = (["A sad task constraint"],)
        memory_limit = 256
        time_limit = 1

        input_text = "Hello, World!"
        output_text = "Hello, World!"

        input_file = InMemoryUploadedFile(
            file=BytesIO(input_text.encode("utf-8")),
            field_name="input_file",
            name="input.txt",
            content_type="text/plain",
            size=13,
            charset="utf-8",
        )
        output_file = InMemoryUploadedFile(
            file=BytesIO(output_text.encode("utf-8")),
            field_name="output_file",
            name="output.txt",
            content_type="text/plain",
            size=13,
            charset="utf-8",
        )

        # We're gonna use RequestFactory to mock a request. This is
        # necessary because the save_model method requires a request
        # object with the FILES attribute.
        mock = RequestFactory()
        request = mock.post("/admin/tasks/task/add/")

        request.FILES["input_file"] = input_file
        request.FILES["output_file"] = output_file

        task = Task(
            title=title,
            description=description,
            constraints=constraints,
            memory_limit=memory_limit,
            time_limit=time_limit,
            contest=self.contest,
        )

        self.admin.save_model(
            request=request, obj=task, form=TaskModelForm(), change=False
        )

        self.assertEqual(task.title, title)
        self.assertEqual(task.description, description)
        self.assertEqual(task.constraints, constraints)
        self.assertEqual(task.memory_limit, memory_limit)
        self.assertEqual(task.time_limit, time_limit)
        self.assertEqual(task.input_file, input_text)
        self.assertEqual(task.output_file, output_text)

    def test_save_model_without_files(self) -> None:
        title = "Example task"
        description = "Some example task"
        constraints = (["A sad task constraint"],)
        memory_limit = 256
        time_limit = 1

        task = Task(
            title=title,
            description=description,
            constraints=constraints,
            memory_limit=memory_limit,
            time_limit=time_limit,
            contest=self.contest,
        )

        # We're gonna use RequestFactory to mock a request. This is
        # necessary because the save_model method requires a request
        # object with the FILES attribute.
        mock = RequestFactory()
        request = mock.post("/admin/tasks/task/add/")

        self.admin.save_model(
            request=request, obj=task, form=TaskModelForm(), change=False
        )

        self.assertEqual(task.title, title)
        self.assertEqual(task.description, description)
        self.assertEqual(task.constraints, constraints)
        self.assertEqual(task.memory_limit, memory_limit)
        self.assertEqual(task.time_limit, time_limit)
        self.assertEqual(task.input_file, "")
        self.assertEqual(task.output_file, "")

    def test_save_model_with_change(self) -> None:
        title = "Example task"
        description = "Some example task"
        constraints = (["A sad task constraint"],)
        memory_limit = 256
        time_limit = 1

        input_text = "Hello, World!"
        output_text = "Hello, World!"

        input_file = InMemoryUploadedFile(
            file=BytesIO(input_text.encode("utf-8")),
            field_name="input_file",
            name="input.txt",
            content_type="text/plain",
            size=13,
            charset="utf-8",
        )
        output_file = InMemoryUploadedFile(
            file=BytesIO(output_text.encode("utf-8")),
            field_name="output_file",
            name="output.txt",
            content_type="text/plain",
            size=13,
            charset="utf-8",
        )

        # We're gonna use RequestFactory to mock a request. This is
        # necessary because the save_model method requires a request
        # object with the FILES attribute.
        mock = RequestFactory()
        request = mock.post("/admin/tasks/task/add/")

        request.FILES["input_file"] = input_file
        request.FILES["output_file"] = output_file

        task = Task(
            title=title,
            description=description,
            constraints=constraints,
            memory_limit=memory_limit,
            time_limit=time_limit,
            contest=self.contest,
        )

        self.admin.save_model(
            request=request, obj=task, form=TaskModelForm(), change=True
        )

        self.assertEqual(task.title, title)
        self.assertEqual(task.description, description)
        self.assertEqual(task.constraints, constraints)
        self.assertEqual(task.memory_limit, memory_limit)
        self.assertEqual(task.time_limit, time_limit)
        self.assertEqual(task.input_file, input_text)
        self.assertEqual(task.output_file, output_text)

    def test_save_model_with_change_without_files(self) -> None:
        title = "Example task"
        description = "Some example task"
        constraints = (["A sad task constraint"],)
        memory_limit = 256
        time_limit = 1

        task = Task(
            title=title,
            description=description,
            constraints=constraints,
            memory_limit=memory_limit,
            time_limit=time_limit,
            contest=self.contest,
        )

        # We're gonna use RequestFactory to mock a request. This is
        # necessary because the save_model method requires a request
        # object with the FILES attribute.
        mock = RequestFactory()
        request = mock.post("/admin/tasks/task/add/")

        self.admin.save_model(
            request=request, obj=task, form=TaskModelForm(), change=True
        )

        self.assertEqual(task.title, title)
        self.assertEqual(task.description, description)
        self.assertEqual(task.constraints, constraints)
        self.assertEqual(task.memory_limit, memory_limit)
        self.assertEqual(task.time_limit, time_limit)
        self.assertEqual(task.input_file, "")
        self.assertEqual(task.output_file, "")


class TaskURLTestCase(TestCase):
    def test_detail_url_to_view_name(self) -> None:
        url = reverse("tasks:detail", args=[1])

        view_name = resolve(url).view_name
        expected = "tasks:detail"

        self.assertEqual(view_name, expected)

    def test_detail_url_reverse(self) -> None:
        url = reverse("tasks:detail", args=[1])
        expected = "/tasks/1/"

        self.assertEqual(url, expected)


class TasksViewTestCase(TestCase):
    def setUp(self) -> None:
        now = timezone.now()
        start_time = now - timedelta(hours=1)
        end_time = now + timedelta(hours=1)

        self.code = "print('Hello, World!')"

        self.contest = Contest._default_manager.create(
            title="Test Contest 1",
            description="This is a test contest",
            start_time=start_time,
            end_time=end_time,
        )
        self.task = Task._default_manager.create(
            title="Example task",
            description="Some example task",
            score=200,
            constraints=["A sad task constraint"],
            contest=self.contest,
            output_file="Hello, World!\n",
        )

        self.user = User._default_manager.create(
            email="user@email.com",
            username="user",
            password="password",
        )

        self.submission = Submission._default_manager.create(
            author=self.user,
            task=self.task,
            code="print('Hello, World!')",
            status=SubmissionStatus.WAITING_JUDGE,
        )

        self.url = reverse("tasks:detail", args=[self.task.id])
        self.view = DetailView()
        self.view.object = self.task

    def test_send_submission_successfully(self) -> None:
        self.client.force_login(self.user)

        self.client.post(self.url, data={"code": self.code})
        self.assertEqual(Submission._default_manager.count(), 2)

    def test_send_submission_with_short_code(self) -> None:
        self.client.force_login(self.user)

        self.client.post(self.url, data={"code": "c"})
        self.assertEqual(Submission._default_manager.count(), 1)

    def test_detail_view_model_is_task(self) -> None:
        self.assertEqual(DetailView.model, Task)

    def test_detail_view_template_name_is_correct(self) -> None:
        self.assertEqual(DetailView.template_name, "tasks/detail.html")

    def test_detail_view_form_class_is_submission_form(self) -> None:
        self.assertEqual(DetailView.form_class, SubmissionForm)

    def test_send_submission_without_authentication(self) -> None:
        response = self.client.post(self.url, data={"code": self.code})
        expected_target = reverse("login")

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            expected_target,
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )

    def test_access_task_that_is_accessible(self) -> None:
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_access_task_that_is_not_accessible(self) -> None:
        self.task.contest.cancelled = True
        self.task.contest.save()

        response = self.client.get(self.url)
        expected_target = reverse("home")

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            expected_target,
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )

    def test_handle_submission_with_exception(self) -> None:
        self.client.force_login(self.user)

        code = "raise Exception('Test exception')"
        response = self.client.post(self.url, data={"code": code})
        url = reverse("submissions:list")

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            url,
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )

    def test_handle_submission_with_correct_output(self) -> None:
        self.client.force_login(self.user)

        self.task.output_file = "Hello, World!\n"
        self.task.save()

        response = self.client.post(self.url, data={"code": self.code})
        url = reverse("submissions:list")

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            url,
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )

    def test_handle_submission_with_wrong_output(self) -> None:
        self.client.force_login(self.user)

        self.task.output_file = "Hello, World!"
        self.task.save()

        url = reverse("submissions:list")
        response = self.client.post(self.url, data={"code": self.code})

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            url,
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )

    def test_submission_has_accepted_status_increases_user_score(self) -> None:
        handle_submission.apply(
            args=(self.submission.code, self.task.id, self.submission.id)
        )

        self.submission.refresh_from_db()
        self.user.refresh_from_db()

        self.assertEqual(self.submission.status, SubmissionStatus.ACCEPTED)
        self.assertEqual(self.user.score, self.task.score)

    def test_submission_without_accepted_status_does_not_increase_user_score(
        self,
    ) -> None:
        self.submission.code = 'print("Hello, Word")'

        handle_submission.apply(
            args=(self.submission.code, self.task.id, self.submission.id)
        )

        self.user.refresh_from_db()
        self.assertEqual(self.user.score, 0)

    def test_repeated_accepted_submission_cant_sum_to_user_score(self) -> None:
        handle_submission.apply(
            args=(self.submission.code, self.task.id, self.submission.id)
        )

        second_submission = Submission._default_manager.create(
            author=self.user,
            task=self.task,
            code="print('Hello, World!')",
            status=SubmissionStatus.WAITING_JUDGE,
        )

        handle_submission.apply(
            args=(second_submission.code, self.task.id, second_submission.id)
        )

        self.user.refresh_from_db()
        self.assertEqual(self.user.score, self.task.score)

    def test_form_success_url(self) -> None:
        url = reverse("submissions:list")
        self.assertEqual(self.view.get_success_url(), url)

    def test_invalid_form_submission(self) -> None:
        self.client.force_login(self.user)

        response = self.client.post(self.url, data={"code": ""})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/detail.html")
        self.assertFalse(response.context["form"].is_valid())


class BackgroundJobTaskTest(TestCase):
    def setUp(self) -> None:
        now = timezone.now()
        start_time = now - timedelta(hours=1)
        end_time = now + timedelta(hours=1)

        self.code = "print('Hello, World!')"

        self.contest = Contest._default_manager.create(
            title="Test Contest 1",
            description="This is a test contest",
            start_time=start_time,
            end_time=end_time,
        )
        self.task = Task._default_manager.create(
            title="Example task",
            description="Some example task",
            contest=self.contest,
        )
        self.user = User._default_manager.create(
            email="user@email.com",
            username="user",
            password="password",
        )
        self.submission = Submission._default_manager.create(
            author=self.user,
            task=self.task,
            code=self.code,
            status=SubmissionStatus.ACCEPTED,
        )

    def test_handle_submission_with_correct_output(self) -> None:
        self.task.output_file = "Hello, World!\n"
        self.task.save()

        handle_submission.apply(
            args=(self.code, self.task.id, self.submission.id)
        )

        self.submission.refresh_from_db()
        expected = SubmissionStatus.ACCEPTED

        self.assertEqual(self.submission.status, expected)

    def test_handle_submission_with_wrong_output(self) -> None:
        self.task.output_file = "Hello, World!"
        self.task.save()

        handle_submission.apply(
            args=(self.code, self.task.id, self.submission.id)
        )

        self.submission.refresh_from_db()
        expected = SubmissionStatus.WRONG_ANSWER

        self.assertEqual(self.submission.status, expected)

    def test_handle_submission_with_exception(self) -> None:
        code = "raise Exception('Test exception')"
        handle_submission.apply(args=(code, self.task.id, self.submission.id))

        self.submission.refresh_from_db()
        expected = SubmissionStatus.RUNTIME_ERROR

        self.assertEqual(self.submission.status, expected)
