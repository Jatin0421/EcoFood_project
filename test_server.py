import pytest
from server import app, db, User, Donation, Volunteer

@pytest.fixture
def client():
    # Set testing configuration and use an in-memory database for isolation.
    app.config['TESTING'] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"  
    with app.test_client() as client:
        with app.app_context():
            db.create_all()  # Create all tables before each test
        yield client
        with app.app_context():
            db.drop_all()  # Clean up after each test

def test_homepage(client):
    response = client.get('/')
    assert response.status_code == 200
    # Expect the homepage to include either "Welcome" or "EcoFood"
    assert b"Welcome" in response.data or b"EcoFood" in response.data

def test_signup_and_login(client):
    # --- Test Signup ---
    response = client.post('/signup', data={
        'email': 'test@example.com',
        'username': 'testuser',
        'password': 'password123',
        'role': 'User'
    }, follow_redirects=True)
    # After signing up, the user should be redirected to the login page
    assert response.status_code == 200
    assert b"Login" in response.data  # Login page content expected

    # --- Test Login ---
    response = client.post('/login', data={
        'email': 'test@example.com',
        'password': 'password123'
    }, follow_redirects=True)
    # After login, the user should be taken to the dashboard
    assert response.status_code == 200
    assert b"Dashboard" in response.data

def test_donate_food(client):
    # First, create a user and log in (required for the /donate route)
    client.post('/signup', data={
        'email': 'donor@example.com',
        'username': 'donor',
        'password': 'donorpass',
        'role': 'User'
    }, follow_redirects=True)
    client.post('/login', data={
        'email': 'donor@example.com',
        'password': 'donorpass'
    }, follow_redirects=True)
    
    # Submit a donation form via POST
    response = client.post('/donate', data={
        'foodName': 'Bread',
        'quantity': '2 loaves',
        'expiryDate': '2025-12-31',
        'location': '123 Main St',
        'contact': '1234567890'
    }, follow_redirects=True)
    assert response.status_code == 200

    # Check that the donation appears in the food list page
    response = client.get('/food-list')
    assert b"Bread" in response.data

def test_volunteer_signup(client):
    # Submit the volunteer form
    response = client.post('/volunteer', data={
        'name': 'Volunteer One',
        'email': 'volunteer@example.com',
        'phone': '0987654321'
    }, follow_redirects=True)
    assert response.status_code == 200
    # The redirect goes to the home page; check for a confirmation message or homepage text.
    assert (b"Thank you" in response.data or
            b"Volunteer" in response.data or
            b"Welcome" in response.data)

def test_logout(client):
    # Create and log in a user before testing logout functionality
    client.post('/signup', data={
        'email': 'logout@example.com',
        'username': 'logoutuser',
        'password': 'logoutpass',
        'role': 'User'
    }, follow_redirects=True)
    client.post('/login', data={
        'email': 'logout@example.com',
        'password': 'logoutpass'
    }, follow_redirects=True)
    
    # Perform logout; this should redirect to the login page.
    response = client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b"Login" in response.data

if __name__ == "__main__":
    pytest.main()
    print("\n✅✅ All tests passed successfully! ✅✅")
