import pytest

from contrib.tests import url


def test_basic_route(api):
    @api.route("/")
    def home(req, resp):
        resp.body = "Welcome Home."


def test_route_overlap_throws_exception(api):
    @api.route("/")
    def home(req, resp):
        resp.body = "Welcome Home."

    with pytest.raises(AssertionError):
        @api.route("/")
        def home2(req, resp):
            resp.body = "Welcome Home2."


def test_parameterized_route(api, client):
    @api.route("/{name}")
    def hello(req, resp, name):
        resp.body = f"hey {name}"

    assert client.get(url("/matthew")).text == "hey matthew"


def test_alcazar_test_client_can_send_requests(api, client):
    RESPONSE_TEXT = "THIS IS COOL"

    @api.route("/cool")
    def cool(req, resp):
        resp.body = RESPONSE_TEXT

    assert client.get(url("/cool")).text == RESPONSE_TEXT


def test_status_code_is_returned(api, client):
    @api.route("/cool")
    def cool(req, resp):
        resp.body = "cool thing"
        resp.status_code = 215

    assert client.get(url("/cool")).status_code == 215


def test_default_404_response(client):
    response = client.get(url("/doesnotexist"))

    assert response.status_code == 404
    assert response.text == "Not found."


def test_class_based_handler_route_registration(api):
    @api.route("/book")
    class BookResource:
        def get(self, req, resp):
            resp.body = "yolo"


def test_class_based_handler_get(api, client):
    response_text = "this is a get request"

    @api.route("/book")
    class BookResource:
        def get(self, req, resp):
            resp.body = response_text

    client.get(url("/book"))

    assert client.get(url("/book")).text == response_text


def test_class_based_handler_post(api, client):
    response_text = "this is a post request"

    @api.route("/book")
    class BookResource:
        def post(self, req, resp):
            resp.body = response_text

    assert client.post(url("/book")).text == response_text


def test_class_based_handler_not_allowed_method(api, client):
    @api.route("/book")
    class BookResource:
        def post(self, req, resp):
            resp.body = "yolo"

    with pytest.raises(AttributeError):
        client.get(url("/book"))


# todo: test for Response helper functions: json, html, text, body, status_codes and content types
