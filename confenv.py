#!/usr/bin/env python
from django.core.management import utils
import secrets
import sys


def main(interactive):
    default_env_dict = {
        'MONGO_INITDB_ROOT_USERNAME': 'mongoadmin',
        'MONGO_INITDB_ROOT_PASSWORD': secrets.token_urlsafe(24),
        'DJANGO_SECRET_KEY': utils.get_random_secret_key(),
        'DJANGO_DEBUG': 'True',
        'DB_HOST': 'localhost',
        'DB_PORT': '27017',
        'DB_NAME': 'db-bulker'
    }
    env_dict = {}

    with open('.env') as f:
        for line in f.readlines():
            try:
                key, value = line.split('=')
                env_dict[key] = value.rstrip()
            except ValueError as e:
                print(e)
                pass
            
    for required_key in default_env_dict.keys():
        if env_dict.get(required_key) == None:
            if interactive:
                print(f'The key {required_key} is undefined. Please input a value (or leave empty for default: {default_env_dict[required_key]!r}):')
                new_value = input() or default_env_dict[required_key]
            else:
                print(f'The key {required_key} is undefined. Writing default value...')
                new_value = default_env_dict[required_key]
            env_dict[required_key] = new_value

    with open('.env', 'w') as f:
        for key, value in env_dict.items():
            f.write(f'{key}={value}\n')
            
if __name__ == '__main__':
    if len(sys.argv) < 2:
        interactive = True
    main(interactive)