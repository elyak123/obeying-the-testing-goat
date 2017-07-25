from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run
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
	current_commit = local('git log -n l --format =%H', capture=True)
	run(f'cd {source_folder} && git reset --hard {current_commit}')

def deploy():
	site_folder = f'/home/{env.user}/sites/{env.host}'
	source_folder = site_folder + '/source'
	_create_directory_structure_if_necessary(site_folder)
	_get_lastest_source(source_folder)
	_update_virtualenv(source_folder)
	_update_static_files(source_folder)
	_update_database(source_folder)