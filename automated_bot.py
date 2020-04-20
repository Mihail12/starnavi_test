import configparser
import random

import requests
import factory

config = configparser.RawConfigParser()
config.read('.config.automated_bot')
config_kwargs = dict(config.items('BOT SECTION'))


number_of_users = int(config_kwargs.get('number_of_users', 0))
max_posts_per_user = int(config_kwargs.get('max_posts_per_user', 0))
max_likes_per_user = int(config_kwargs.get('max_likes_per_user', 0))

users_tokens = []
server_api = {
    'base': 'http://localhost:8000/',
    'login': 'api/auth/login/',
    'users': 'api/users/',
    'posts': 'api/posts/',
    'likes': 'api/likes/',
}


def get_headers(token):
    return {
        'Authorization': f'JWT {token}'
    }


def create_user_and_posts():
    user_data = {
        "email": factory.Faker('email').generate(),
        "first_name": factory.Faker('first_name').generate(),
        "last_name": factory.Faker('last_name').generate(),
        "password": factory.Faker('password').generate(),
        "username": factory.Faker('word').generate()
    }
    requests.post(f"{server_api['base']}{server_api['users']}", user_data)

    auth_login_data = {'password': user_data['password'], 'username': user_data['username']}
    token = requests.post(f"{server_api['base']}{server_api['login']}", data=auth_login_data).json()['token']
    users_tokens.append(token)

    for _ in range(random.randint(0, max_posts_per_user)):
        post_data = {
            'text': factory.Faker('text').generate()
        }
        requests.post(f"{server_api['base']}{server_api['posts']}", post_data, headers=get_headers(token))


def like_random_posts():
    for token in users_tokens:
        posts_response = requests.get(f"{server_api['base']}{server_api['posts']}", headers=get_headers(token))
        posts = [post['guid'] for post in posts_response.json()]
        for post in random.choices(posts, k=random.randint(0, max_likes_per_user)):
            like_data = {
                'post': post
            }
            requests.post(f"{server_api['base']}{server_api['likes']}", like_data, headers=get_headers(token))


if __name__ == '__main__':
    print(f'Creating {number_of_users} users and up to {max_posts_per_user} posts per users started.')
    for _ in range(number_of_users):
        create_user_and_posts()

    print(f'Liking posts... Up to {max_likes_per_user} likes per user')
    like_random_posts()
    print('Successfully ended.')
