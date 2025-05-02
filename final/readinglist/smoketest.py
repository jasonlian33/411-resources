import requests

def run_smoketest():
    base_url = "http://localhost:5001/api"
    username = "test_user"
    password = "test_pass"

    book_orwell = {
        "author": "George Orwell",
        "title": "1984",
        "year": 1949,
        "genre": "Dystopian",
        "length": 328
    }

    book_huxley = {
        "author": "Aldous Huxley",
        "title": "Brave New World",
        "year": 1932,
        "genre": "Science Fiction",
        "length": 311
    }

    # Health check
    health_response = requests.get(f"{base_url}/health")
    assert health_response.status_code == 200
    assert health_response.json()["status"] == "success"
    print("Health check passed")

    # Reset users and books
    assert requests.delete(f"{base_url}/reset-users").json()["status"] == "success"
    print("Reset users successful")
    assert requests.delete(f"{base_url}/reset-books").json()["status"] == "success"
    print("Reset books successful")

    # Create user
    create_user_response = requests.put(f"{base_url}/create-user", json={
        "username": username,
        "password": password
    })
    assert create_user_response.status_code == 201
    print("User creation successful")

    session = requests.Session()

    # Login
    login_resp = session.post(f"{base_url}/login", json={
        "username": username,
        "password": password
    })
    assert login_resp.status_code == 200
    print("Login successful")

    # Create first book
    create_book_resp = session.post(f"{base_url}/create-book", json=book_orwell)
    assert create_book_resp.status_code == 201
    print("Book creation successful")

    # Change password
    change_pass_resp = session.post(f"{base_url}/change-password", json={
        "new_password": "new_test_pass"
    })
    assert change_pass_resp.status_code == 200
    print("Password change successful")

    # Login with new password
    login_resp = session.post(f"{base_url}/login", json={
        "username": username,
        "password": "new_test_pass"
    })
    assert login_resp.status_code == 200
    print("Login with new password successful")

    # Create second book
    create_book_resp = session.post(f"{base_url}/create-book", json=book_huxley)
    assert create_book_resp.status_code == 201
    print("Second book creation successful")

    # Logout
    logout_resp = session.post(f"{base_url}/logout")
    assert logout_resp.status_code == 200
    print("Logout successful")

    # Try creating a book while logged out (should fail)
    unauthorized_resp = session.post(f"{base_url}/create-book", json=book_huxley)
    assert unauthorized_resp.status_code == 401
    print("Unauthorized book creation failed as expected")


if __name__ == "__main__":
    run_smoketest()
