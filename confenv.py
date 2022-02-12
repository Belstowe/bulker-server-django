#!/usr/bin/env python
from django.core.management import utils
import secrets
import sys
import json
from pathlib import Path
from textwrap import indent


def gen_mongo_js(filename, user, pwd, db):
    Path(filename).touch(exist_ok=True)
    with open(filename, 'w') as f:
        f.write('db.createUser(\n')
        f.write(
            indent(
                json.dumps(
                    {
                        'user': user,
                        'pwd': pwd,
                        'roles': [
                            {
                                'role': "readWrite",
                                'db': db
                            }
                        ]
                    },
                    indent=4
                ),
                '    '
            )
        )
        f.write('\n);')


class EnvParser:
    def __init__(self, filename, interactive, default_data):
        self.filename = filename
        self.data = {}

        Path(filename).touch(exist_ok=True)
        with open(filename) as f:
            for line in f.readlines():
                try:
                    key, value = line.split('=')
                    self.data[key] = value.rstrip()
                except ValueError as e:
                    print(e)
                    pass

        for required_key in default_data.keys():
            if self.data.get(required_key) is None:
                if interactive is True:
                    print(f'[{filename}]: The key {required_key} is undefined.')
                    print(f'Please input a value (or leave empty for default: {default_data[required_key]!r}):')
                    new_value = input().strip() or default_data[required_key]
                else:
                    print(f'[{filename}]: The key {required_key} is undefined. Writing default value...')
                    new_value = default_data[required_key]
                self.data[required_key] = new_value

    def write(self):
        with open(self.filename, 'w') as f:
            for key, value in self.data.items():
                f.write(f'{key}={value}\n')


def main(interactive):
    django_env = EnvParser(
        filename='django.env',
        interactive=interactive,
        default_data={
            'DJANGO_SECRET_KEY': utils.get_random_secret_key(),
            'DJANGO_DEBUG': 'True',
            'DB_HOST': 'localhost',
            'DB_PORT': '27017'
        }
    )
    mongo_env = EnvParser(
        filename='mongo.env',
        interactive=interactive,
        default_data={
            'MONGO_INITDB_ROOT_USERNAME': 'mongoadmin',
            'MONGO_INITDB_ROOT_PASSWORD': secrets.token_urlsafe(24)
        }
    )
    shared_env = EnvParser(
        filename='.env',
        interactive=interactive,
        default_data={
            'MONGO_INITDB_DATABASE': 'db-bulker',
            'DB_USERNAME': 'bulker-user',
            'DB_PASSWORD': secrets.token_urlsafe(12)
        }
    )
    gen_mongo_js(
        'mongo-init.js',
        user=shared_env.data.get('DB_USERNAME'),
        pwd=shared_env.data.get('DB_PASSWORD'),
        db=shared_env.data.get('MONGO_INITDB_DATABASE')
    )

    django_env.write()
    mongo_env.write()
    shared_env.write()


if __name__ == '__main__':
    interactive = True
    if len(sys.argv) >= 2:
        interactive = sys.argv[1]
    main(interactive)
