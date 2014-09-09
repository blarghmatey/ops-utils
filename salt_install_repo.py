import os
import sys
import shutil
import yaml


def merge_top_files(source_path, target_path):
    top_dict = {}
    try:
        with open(target_path, 'r') as target:
            top_dict.update(yaml.load(target))
    except FileNotFoundError:
        sys.stderr.write("File at {0} not found".format(target_path))
    try:
        with open(source_path, 'r') as source:
            top_dict.update(yaml.load(source))
    except FileNotFoundError:
        sys.stderr.write("File at {0} not found".format(source_path))
    with open(target_path, 'w') as dest:
        yaml.dump(dest)


def copy_files(source_root_path, dest_root_path):
    for path in ['pillar', 'salt']:
        source = '{0}/{1}/top.sls'.format(source_root_path, path)
        dest = '{0}/{1}/top.sls'.format(dest_root_path, path)
        merge_top_files(source, dest)
        shutil.move(source, '{0}.backup'.format(source))
    for fname in os.listdir(source_root_path):
        shutil.copy('{0}/{1}'.format(source_root_path, fname),
                    '{0}/{1}'.format(dest_root_path, fname))


if __name__ == '__main__':
    source_root_path = sys.argv[1]
    dest_root_path = sys.argv[2]
    copy_files(source_root_path, dest_root_path)
