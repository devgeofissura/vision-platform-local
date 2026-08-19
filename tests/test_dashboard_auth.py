from tests.conftest import TestSession
from src.auth.password import hash_password
from src.storage.models import User


def _create_admin():
    db = TestSession()
    existing = db.query(User).filter(User.username == "admin").first()
    if not existing:
        db.add(User(username="admin", password_hash=hash_password("admin"), role="admin"))
        db.commit()
    db.close()


def test_login_page_renders(client):
    resp = client.get("/login")
    assert resp.status_code == 200
    assert "GeoFissura" in resp.text


def test_login_with_valid_credentials(client):
    _create_admin()
    resp = client.post("/login", data={"username": "admin", "password": "admin"}, follow_redirects=False)
    assert resp.status_code == 302
    assert resp.headers["location"] == "/dashboard"
    assert "token" in resp.cookies


def test_login_with_wrong_password(client):
    _create_admin()
    resp = client.post("/login", data={"username": "admin", "password": "wrong"})
    assert resp.status_code == 200
    assert "invalidas" in resp.text.lower() or "inválidas" in resp.text.lower()


def test_login_with_nonexistent_user(client):
    _create_admin()
    resp = client.post("/login", data={"username": "nobody", "password": "pass"})
    assert resp.status_code == 200
    assert "invalidas" in resp.text.lower() or "inválidas" in resp.text.lower()


def test_dashboard_redirect_without_auth(client):
    resp = client.get("/dashboard", follow_redirects=False)
    assert resp.status_code == 302
    assert resp.headers["location"] == "/login"


def test_dashboard_with_auth(client):
    _create_admin()
    login = client.post("/login", data={"username": "admin", "password": "admin"})
    resp = client.get("/dashboard")
    assert resp.status_code == 200
    assert "Dashboard" in resp.text


def test_logout_clears_cookie(client):
    resp = client.get("/logout", follow_redirects=False)
    assert resp.status_code == 302
    assert resp.headers["location"] == "/login"


def test_dashboard_pages_require_auth(client):
    for path in ["/dashboard", "/dashboard/cameras", "/dashboard/observations", "/dashboard/queue", "/dashboard/settings"]:
        resp = client.get(path, follow_redirects=False)
        assert resp.status_code == 302
        assert resp.headers["location"] == "/login"


def test_dashboard_pages_with_auth(client):
    _create_admin()
    client.post("/login", data={"username": "admin", "password": "admin"})
    for path in ["/dashboard", "/dashboard/cameras", "/dashboard/observations", "/dashboard/queue", "/dashboard/settings"]:
        resp = client.get(path)
        assert resp.status_code == 200


def test_login_already_logged_in_redirects(client):
    _create_admin()
    client.post("/login", data={"username": "admin", "password": "admin"})
    resp = client.get("/login", follow_redirects=False)
    assert resp.status_code == 302
    assert resp.headers["location"] == "/dashboard"
