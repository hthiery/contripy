import argparse
import json
import os
import sys
import yaml

from datetime import datetime
from dotenv import load_dotenv
from envyaml import EnvYAML

from .lib.parsers import *
from .lib.models import Author, Project

def dump_json(outfile, authors, projects, cfg, args):
    a = {
        author.name: {
            k: v
            for k, v in author.__dict__.items()
        } for author in authors
    }

    p = {
        project.name: {
            k: v
            for k, v in project.__dict__.items()
        } for project in projects
    }

    final = {
        'period': {
            'start': args.period_start,
            'end': args.period_end
        },
        'authors': a,
        'projects': p,
        'document': cfg['document']
    }

    # create folder
    out_path = os.path.dirname(outfile)
    if out_path and not os.path.exists(out_path):
        os.makedirs(out_path)

    with open(outfile, 'w') as f:
        json.dump(final, f, indent=2, separators=(',', ': '))
        f.write('\n')


def parse_args():
    start = datetime.now().replace(year=datetime.now().year-1)

    parser = argparse.ArgumentParser(description='Contribution reporter.')
    parser.add_argument('--from', dest='period_start', help='Period start',
                        default=start.strftime('%Y-%m-%d'))
    parser.add_argument('--to', dest='period_end', help='Period end',
                        default=datetime.now().strftime('%Y-%m-%d'))
    parser.add_argument('-p', '--project', dest='project', nargs='*',
                        help='project(s)')
    parser.add_argument('-c', '--config', dest='cfgfile', metavar='CFG',
                        type=str, help='config file', required=True)
    parser.add_argument('-o', '--out', dest='outfile', metavar='OUT',
                        type=str, help='output file', required=True)
    args = parser.parse_args()

    return args


def run():
    load_dotenv()
    authors = list()
    projects = list()

    args = parse_args()

    try:
        cfg = EnvYAML(args.cfgfile)
    except yaml.YAMLError as exc:
        print(exc)
        print('ERROR: parsing config')
        sys.exit(1)

    for name in cfg['authors']:
        authors.append(Author(name, cfg['authors'][name]))

    for name in cfg['projects']:
        projects.append(Project(name, cfg['projects'][name]))

    for project in projects:
        if args.project and project.name not in args.project:
            continue
        print('Checking project {}'.format(project.name))

        if project.parser == "git":
            parser = GitContributionParser(project, args)
        elif project.parser == "github":
            try:
                token = cfg['parser']['github']['token']
            except KeyError:
                print("Specifying parser.github.token in config is required for GitHub parser!")
                sys.exit(1)
            try:
                parser = GitHubContributionParser(project, args, token)
            except NameError:
                print("GitHub parser not available, skipping project {}".format(project.name))
                continue
        else:
            print(f"Invalid parser { project.parser }")
            sys.exit(1)

        parser.update_project()

        for author in authors:
            print(' Author: {} .. '.format(author.name), end='', flush=True)
            if project.only_users and not author.name in project.only_users:
                print('skip')
                continue
            if project.skip_users and author.name in project.skip_users:
                print('skip')
                continue
            commits = parser.get_authored_contributions(author)
            if commits:
                author.add_authored_contributions(project.name, commits)

            others = parser.get_other_contributions(author)
            if others:
                author.add_other_contributions(project.name, others)

            if not (commits is None or others is None):
                print('{}/{}'.format(len(commits), len(others) if others else 0))

    dump_json(args.outfile, authors, projects, cfg, args)