# -*- coding: utf-8 -*-
"""koalixcrm#444 -- admin link helpers must HTML-escape user-controlled text."""
import pytest

from koalixcrm.reporting.tests.factories.project_factory import StandardProjectFactory
from koalixcrm.reporting.tests.factories.task_factory import StandardTaskFactory
from koalixcrm.reporting.tests.factories.work_factory import StandardWorkFactory

PAYLOAD = '<script>alert(1)</script>'  # 25 chars, survives limit_string_length(.., 30)
ESCAPED = '&lt;script&gt;alert(1)&lt;/script&gt;'


@pytest.mark.django_db
class TestTaskLinkEscaping:
    def test_title_is_escaped(self):
        task = StandardTaskFactory.create(title=PAYLOAD)
        html = str(task.link_to_task())
        assert '<script>' not in html
        assert ESCAPED in html

    def test_link_unchanged_for_plain_title(self):
        task = StandardTaskFactory.create(title='Plain title')
        assert str(task.link_to_task()) == (
            "<a href='/admin/reporting/task/%s' >Plain title</a>" % task.id
        )

    def test_unsaved_task_not_present(self):
        from koalixcrm.reporting.models.task import Task
        assert Task(title=PAYLOAD).link_to_task() == 'Not present'


@pytest.mark.django_db
class TestProjectLinkEscaping:
    def test_project_name_is_escaped(self):
        project = StandardProjectFactory.create(project_name=PAYLOAD)
        html = str(project.link_to_project())
        assert '<script>' not in html
        assert ESCAPED in html

    def test_link_unchanged_for_plain_name(self):
        project = StandardProjectFactory.create(project_name='Plain project')
        assert str(project.link_to_project()) == (
            "<a href='/admin/reporting/project/%s' >Plain project</a>" % project.id
        )


@pytest.mark.django_db
class TestWorkLink:
    def test_link_contains_id_only(self):
        work = StandardWorkFactory.create()
        assert str(work.link_to_work()) == (
            "<a href='/admin/reporting/work/%s' >%s</a>" % (work.id, work.id)
        )
