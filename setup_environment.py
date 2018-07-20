#!/usr/bin/python3
import subprocess

packages = [
	'lxml',
	'tensorflow',
	'websockets',
	'roomai',
	'tflearn',
	'numpy',
	'h5py'
]

def install(package_name):
	subprocess.call(['pip3', 'install', package_name])

if __name__ == '__main__':
	for package in packages:
		install(package)

