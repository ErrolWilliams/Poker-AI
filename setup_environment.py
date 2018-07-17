#!/usr/bin/python3.6
import subprocess

packages = [
	'lxml',
	'tensorflow',
	'websockets',
	'holdem'
]

def install(package_name):
	subprocess.call(['pip3.6', 'install', package_name])

if __name__ == '__main__':
	for package in packages:
		install(package)

