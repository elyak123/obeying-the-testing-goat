from fabric.contrib.files import append, exists, sed
from fabric.api           import env, local, run, sudo
import random

REPO_URL = 'https://github.com/elyak123/obeying-the-testing-goat.git'

def _create_directory_structure_if_necessary(site_folder):
    for subfolder in ('database', 'static', 'virtualenv', 'source'):
        run(f'mkdir -p {site_folder}/{subfolder}')

def _get_lastest_source(source_folder):
    if exists(source_folder + '/.git'):
        run(f'cd {source_folder} && git fetch')
    else:
        run(f'git clone {REPO_URL} {source_folder}')
    current_commit = local('git log -n 1 --format=%H', capture=True)
    run(f'cd {source_folder} && git reset --hard {current_commit}')

def _update_settings(source_folder, site_name):
    settings_path = source_folder + '/superlists/settings.py'
    sed(settings_path, 'DEBUG = True', 'DEBUG = False')
    sed(settings_path, 
        'ALLOWED_HOSTS = .+$', 
        f'ALLOWED_HOSTS = ["{site_name}"]'
    )
    secret_key_file = source_folder + '/superlists/secret_key.py'
    if not exists(secret_key_file):
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
        append(settings_path, f'SECRET_KEY = {key}')
    append(settings_path, '\nfrom .secret_key import SECRET_KEY')

def _update_virtualenv(source_folder):
    virtualenv_folder = source_folder + '/../virtualenv'
    if not exists(virtualenv_folder + '/bin/pip'):
        run(f'python3.6 -m venv {virtualenv_folder}')
    run(f'{virtualenv_folder}/bin/pip install -r {source_folder}/requirements.txt')

def _update_static_files(source_folder):
    run(
        f'cd {source_folder}'  
        ' && ../virtualenv/bin/python manage.py collectstatic --noinput'  
    )


def _update_database(source_folder):
    run(
        f'cd {source_folder}'
        '&& ../virtualenv/bin/python manage.py migrate --noinput'
    )

def _provisioning():
    sudo('apt update && apt upgrade')
    try:
        nginx = run('which nginx')
    except:
        sudo('apt install nginx && systemctl start nginx')
    try:
        python36 = run('which python3.6')
    except:
        sudo('add-apt-repository ppa:fkrull/deadsnakes')
        sudo('apt update')
        sudo('apt install python3.6 python3.6-venv')


def _webserver_configuration(site_name, source_folder):
    if exists('/etc/nginx/sites-enabled/default'):
        sudo('rm -r /etc/nginx/sites-enabled/default')
    if not exists(f'/etc/nginx/sites-available/{site_name}'):
        run(f'sed "s/SITENAME/{site_name}/g" '
            f'{source_folder}/deploy_tools/nginx.template.conf'
            f'| sudo tee /etc/nginx/sites-available/{site_name}',
            warn_only=True
        )
        sudo(f'ln -s /etc/nginx/sites-available/{site_name} /etc/nginx/sites-enabled/{site_name}')

    if not exists(f'/etc/systemd/system/gunicorn-{site_name}.service'):
        run(f'sed -e "s/SITENAME/{site_name}/g" -e s/SERVERUSER/ubuntu/g -e s/MYAPP/superlists/g ' 
            f'{source_folder}/deploy_tools/gunicorn-systemd.template.service '
            f'| sudo tee /etc/systemd/system/gunicorn-{site_name}.service',
            warn_only=True
        )

def _restart_webserver(site_name):
    sudo('systemctl daemon-reload')
    try:
        sudo('systemctl reload nginx')
    except:
        sudo('systemctl start nginx')
    sudo(f'systemctl enable gunicorn-{site_name}')
    sudo(f'sudo systemctl start gunicorn-{site_name}')

def deploy():
    site_folder = f'/home/{env.user}/sites/{env.host}'
    source_folder = site_folder + '/source'
    _provisioning()
    _create_directory_structure_if_necessary(site_folder)
    _get_lastest_source(source_folder)
    _update_virtualenv(source_folder)
    _update_static_files(source_folder)
    _update_database(source_folder)
    _webserver_configuration(env.host, source_folder)
    _restart_webserver(env.host)
