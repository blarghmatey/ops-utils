import re
import os
import sys
import argparse

parser = argparse.ArgumentParser(
    description="Generate a salt formula skeleton")
parser.add_argument('--state', dest='is_state', type=bool, default=False)
parser.add_argument('formula_name', nargs='+', type=str)

args = parser.parse_args()
formula_name = ('-').join(args.formula_name)
format_args = [formula_name]

if not args.is_state:
    dir_name = '{0}-formula'.format(formula_name)
    format_args.insert(0, dir_name)

if len(formula_name) == 0:
    print("Please provide a formula name")
    sys.exit(1)

if args.is_state:
    path_names = ['{0}/files'.format(*format_args)]
else:
    path_names = ['{0}/{1}'.format(*format_args), '{0}/{1}/files'.format(
        *format_args)]

for path in path_names:
    os.makedirs(path, mode=0o755, exist_ok=True)

if args.is_state:
    file_names = ['{0}/init.sls', '{0}/map.jinja']
else:
    file_names = ['{0}/pillar.example', '{0}/README.rst', '{0}/VERSION',
                  '{0}/{1}/init.sls', '{0}/{1}/map.jinja']

for fname in file_names:
    os.mknod(fname.format(*format_args), mode=0o644)

if not args.is_state:
    with open('{0}/VERSION'.format(*format_args), 'w') as version:
        version.write('0.0.1\n')

print(file_names)
with open(file_names[-1].format(*format_args), 'w') as pkg:
    pkg.write(
'''{{% set {0} = salt['grains.filter_by']({{
    'Debian': {{
        'pkgs': [
        ]
    }},
    'RedHat': {{
        'pkgs': [
        ]
    }},
    'Arch': {{
        'pkgs': [
        ]
    }}
}}, merge=salt['pillar.get']('{0}:lookup')) %}}
'''.format(re.sub('-', '_', formula_name)))

with open(file_names[-2].format(*format_args), 'w') as init:
    init.write(
'''{{% from "{0}/map.jinja" import {1} with context %}}
'''.format(formula_name, re.sub('-', '_', formula_name)))
