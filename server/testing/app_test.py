import flask

from app import app
from models import Article, User

app.secret_key = b'a\xdb\xd2\x13\x93\xc1\xe9\x97\xef2\xe3\x004U\xd1Z'

class TestApp:
    '''Flask API in app.py'''

    def test_can_access_member_only_index_while_logged_in(self):
        '''Allows logged in users to access member-only article index at /members_only_articles.'''
        with app.test_client() as client:
            
            client.get('/clear')

            # Log in the user
            user = User.query.first()
            client.post('/login', json={
                'username': user.username
            })

            # Check if the member-only index is accessible
            response = client.get('/members_only_articles')
            assert response.status_code == 200

            # Log out the user
            client.delete('/logout')

            # Check if the member-only index is not accessible after logout
            response = client.get('/members_only_articles')
            assert response.status_code == 401

    def test_member_only_articles_show_only_member_only_articles(self):
        '''Only shows member-only articles at /members_only_articles.'''
        with app.test_client() as client:
            
            client.get('/clear')

            # Log in the user
            user = User.query.first()
            client.post('/login', json={
                'username': user.username
            })

            # Check if the member-only articles are marked as such
            response_json = client.get('/members_only_articles').get_json()
            for article in response_json:
                assert article['is_member_only'] is True

    def test_can_access_member_only_article_while_logged_in(self):
        '''Allows logged in users to access full member-only articles at /members_only_articles/<int:id>.'''
        with app.test_client() as client:
            
            client.get('/clear')

            # Log in the user
            user = User.query.first()
            client.post('/login', json={
                'username': user.username
            })

            # Get an existing member-only article ID
            article_id = Article.query.with_entities(Article.id).filter_by(is_member_only=True).first()[0]

            # Check if the member-only article is accessible
            response = client.get(f'/members_only_articles/{article_id}')
            assert response.status_code == 200

            # Log out the user
            client.delete('/logout')

            # Check if the member-only article is not accessible after logout
            response = client.get(f'/members_only_articles/{article_id}')
            assert response.status_code == 401
