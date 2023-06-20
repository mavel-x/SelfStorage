import os

def main():
    os.system('python -m pip install -r requirements.txt')

    if not os.path.isfile('.env'):
        from django.core.management.utils import get_random_secret_key
        secret_key = get_random_secret_key()
        with open('.env', 'w') as file:
            file.write(f'DJANGO_SECRET_KEY={secret_key}')

    os.system('python manage.py migrate')

    if not os.path.isdir('media'):
        os.mkdir('media')

if __name__ == '__main__':
    main()