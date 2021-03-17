# coding: utf-8

import unittest
import httpretty
import json
from backlog.util import load_conf
from backlog.base import BacklogAPI

API_ENDPOINT = "https://{space}.backlog.jp/api/v2/{uri}"


class TestProject(unittest.TestCase):
    def setUp(self):
        self.conf = load_conf("./conf.default.yml")["backlog"]
        self.api = BacklogAPI(self.conf["space"], self.conf["api_key"])
        self.space = self.conf["space"]
        self.api_key = self.conf["api_key"]

    @httpretty.activate
    def test_list(self):
        _uri = "projects"
        _archived = False

        expects = [
            {
                "id": 1,
                "projectKey": "TEST",
                "name": "test",
                "chartEnabled": False,
                "subtaskingEnabled": False,
                "projectLeaderCanEditProjectLeader": False,
                "textFormattingRule": "markdown",
                "archived": _archived
            }
        ]

        httpretty.register_uri(
            httpretty.GET,
            API_ENDPOINT.format(space=self.space, uri=_uri),
            body=json.dumps(expects),
            match_querystring=True,
            status=200
        )

        resp = self.api.project.list(archived=False)

        self.assertEqual(expects, resp)

    def test_create(self):
        pass

    @httpretty.activate
    def test_get(self):
        # Set parameter and expects
        _project_id = 1
        _uri = "projects/{project_id_or_key}".format(project_id_or_key=_project_id)
        expects = {
            "id": 1,
            "projectKey": "TEST",
            "name": "test",
            "chartEnabled": False,
            "subtaskingEnabled": False,
            "projectLeaderCanEditProjectLeader": False,
            "textFormattingRule": "markdown",
            "archived": False
        }

        httpretty.register_uri(
            httpretty.GET,
            API_ENDPOINT.format(space=self.space, uri=_uri),
            body=json.dumps(expects),
            status=200
        )

        # test
        resp = self.api.project.get(projectIdOrKey=_project_id)

        self.assertEqual(resp["id"], _project_id)

    def test_update(self):
        pass

    def test_get_icon(self):
        pass

    def test_get_history(self):
        pass

    def test_add_user(self):
        pass

    @httpretty.activate
    def test_list_users(self):
        # Project id given
        _projectIdOrKey = str(1000)

        expects = [
            {
                "id": 1,
                "userId": "admin",
                "name": "admin",
                "roleType": 1,
                "lang": "ja",
                "mailAddress": "eguchi@nulab.example"
            },
        ]

        httpretty.register_uri(
            httpretty.GET,
            API_ENDPOINT.format(
                space=self.space,
                uri="projects/{projectIdOrKey}/users".format(projectIdOrKey=_projectIdOrKey)),
            body=json.dumps(expects)
        )

        resp = self.api.project.list_users(projectIdOrKey=_projectIdOrKey)

        self.assertEqual(expects, resp)

        # Project key given
        _projectIdOrKey = "sample"

        httpretty.register_uri(
            httpretty.GET,
            API_ENDPOINT.format(
                space=self.space,
                uri="projects/{projectIdOrKey}/users".format(projectIdOrKey=_projectIdOrKey)),
            body=json.dumps(expects)
        )

        resp = self.api.project.list_users(projectIdOrKey=_projectIdOrKey)

        self.assertEqual(expects, resp)

    def test_delete_user(self):
        pass

    @httpretty.activate
    def test_list_types(self):
        _project_id = 1
        _uri = "projects/{project_id_or_key}/issueTypes".format(
            project_id_or_key=_project_id
        )
        expects = [
            {
                "id": 1,
                "projectId": _project_id,
                "name": "バグ",
                "color": "#990000",
                "displayOrder": 0
            }
        ]

        httpretty.register_uri(
            httpretty.GET,
            API_ENDPOINT.format(space=self.space, uri=_uri),
            body=json.dumps(expects)
        )

        resp = self.api.project.list_issue_types(projectIdOrKey=_project_id)

        self.assertEqual(list, type(resp))
        self.assertEqual(expects[0]["name"], resp[0]["name"])

    @httpretty.activate
    def test_add_issue_type(self):
        _project_id = 1
        _name = "バグ"
        _color = "#990000"
        _uri = "projects/{project_id_or_key}/issueTypes".format(
            project_id_or_key=_project_id
        )
        expects = {
            "id": 1,
            "projectId": _project_id,
            "name": _name,
            "color": _color,
            "displayOrder": 0
        }

        httpretty.register_uri(
            httpretty.POST,
            API_ENDPOINT.format(space=self.space, uri=_uri),
            body=json.dumps(expects)
        )

        resp = self.api.project.add_issue_type(
            projectIdOrKey=_project_id,
            name=_name,
            color=_color
        )

        self.assertEqual(expects["projectId"], resp["projectId"])
        self.assertEqual(expects["name"], resp["name"])

    @httpretty.activate
    def test_update_issue_type(self):
        _project_id = 1
        _id = 1
        _name = "バグ"
        _color = "#990000"
        _uri = "projects/{project_id_or_key}/issueTypes/{id}".format(
            project_id_or_key=_project_id,
            id=_id
        )
        expects = {
            "id": _id,
            "projectId": _project_id,
            "name": _name,
            "color": _color,
            "displayOrder": 0
        }

        httpretty.register_uri(
            httpretty.PATCH,
            API_ENDPOINT.format(space=self.space, uri=_uri),
            body=json.dumps(expects)
        )

        resp = self.api.project.update_issue_type(
            projectIdOrKey=_project_id,
            id=_id,
            name=_name,
            color=_color
        )

        self.assertEqual(expects["projectId"], resp["projectId"])
        self.assertEqual(expects["name"], resp["name"])
        self.assertEqual(expects["color"], resp["color"])

    @httpretty.activate
    def test_delete_issue_type(self):
        _project_id = 1
        _id = 1
        _substituteIssueTypeId = 2
        _uri = "projects/{project_id_or_key}/issueTypes/{id}".format(
            project_id_or_key=_project_id,
            id=_id
        )
        expects = {
            "id": _id,
            "projectId": _project_id,
            "name": "バグ",
            "color": "#990000",
            "displayOrder": 0
        }

        httpretty.register_uri(
            httpretty.DELETE,
            API_ENDPOINT.format(space=self.space, uri=_uri),
            body=json.dumps(expects)
        )

        resp = self.api.project.delete_issue_type(
            projectIdOrKey=_project_id,
            id=_id,
            substituteIssueTypeId=_substituteIssueTypeId
        )

        self.assertEqual(expects["projectId"], resp["projectId"])
        self.assertEqual(expects["name"], resp["name"])

    @httpretty.activate
    def test_list_categories(self):
        _project_id = 1
        _uri = "projects/{project_id_or_key}/categories".format(
            project_id_or_key=_project_id
        )
        expects = [
            {
                "id": 12,
                "name": "開発",
                "displayOrder": 0
            }
        ]

        httpretty.register_uri(
            httpretty.GET,
            API_ENDPOINT.format(space=self.space, uri=_uri),
            body=json.dumps(expects)
        )

        resp = self.api.project.list_categories(
            projectIdOrKey=_project_id,
        )

        self.assertEqual(expects[0]["id"], resp[0]["id"])

    @httpretty.activate
    def test_add_category(self):
        _project_id = 1
        _name = "開発"
        _uri = "projects/{project_id_or_key}/categories".format(
            project_id_or_key=_project_id
        )
        expects = {
            "id": 1,
            "name": _name,
            "displayOrder": 0
        }

        httpretty.register_uri(
            httpretty.POST,
            API_ENDPOINT.format(space=self.space, uri=_uri),
            body=json.dumps(expects)
        )

        resp = self.api.project.add_category(
            projectIdOrKey=_project_id,
            name=_name
        )

        self.assertEqual(expects["name"], resp["name"])

    @httpretty.activate
    def test_update_category(self):
        _project_id = 1
        _id = 1
        _name = "開発"
        _uri = "projects/{project_id_or_key}/categories/{id}".format(
            project_id_or_key=_project_id,
            id=_id
        )
        expects = {
            "id": _id,
            "name": _name,
            "displayOrder": 0
        }

        httpretty.register_uri(
            httpretty.PATCH,
            API_ENDPOINT.format(space=self.space, uri=_uri),
            body=json.dumps(expects)
        )

        resp = self.api.project.update_category(
            projectIdOrKey=_project_id,
            id=_id,
            name=_name
        )

        self.assertEqual(expects["name"], resp["name"])

    @httpretty.activate
    def test_delete_category(self):
        _project_id = 1
        _id = 1
        _uri = "projects/{project_id_or_key}/categories/{id}".format(
            project_id_or_key=_project_id,
            id=_id
        )
        expects = {
            "id": _id,
            "name": "開発",
            "displayOrder": 0
        }

        httpretty.register_uri(
            httpretty.DELETE,
            API_ENDPOINT.format(space=self.space, uri=_uri),
            body=json.dumps(expects)
        )

        resp = self.api.project.delete_category(
            projectIdOrKey=_project_id,
            id=_id
        )

        self.assertEqual(expects["id"], resp["id"])


if __name__ == "__main__":
    unittest.main(warnings='ignore')
