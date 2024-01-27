def test_user_registration(client_activated_user):
    client, mock_user = client_activated_user
    with client.application.test_request_context():
        client.post('/accounts/sign-up',
            data={
                'email': mock_user.email,
                'username': mock_user.username,
                'password_hash': mock_user.password_hash,
                'activated': True
            }
        )
        client.post('/accounts/sign-in',
            data={
            'email': mock_user.email,
            'password_hash': mock_user.password_hash
            })
        response = client.get('/')
        assert response.status_code == 200

def test_user_sign_in(client_activated_user):
    client, mock_user = client_activated_user
    with client.application.test_request_context():
        login_data = {
            'email': mock_user.email,
            'password': 'testpassword' 
        }
        response = client.post('/accounts/sign-in', data=login_data)
        assert response.status_code == 302
        
def test_user_sign_out(client_activated_user):
    client, mock_user = client_activated_user
    with client.application.test_request_context():
        client.post('/accounts/sign-in', data={
            'email': mock_user.email,
            'password': 'plaintext_password'
        })
        response = client.get('/accounts/sign-out')
        assert response.status_code == 302
        assert '/accounts/sign-in' in response.location
        
def test_user_profile_access(client_activated_user):
    client, mock_user = client_activated_user
    with client.application.test_request_context():
        login_data = {
            'email': mock_user.email,
            'password': 'testpassword' 
        }
        response = client.post('/accounts/sign-in', data=login_data)
        response = client.get('/accounts/profile', follow_redirects=True)
        assert "Welcome back" in response.get_data(as_text=True)