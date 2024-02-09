from .ContributionParser import ContributionParser

import os
import subprocess

REPOS_DIR = 'repos'

class GitContributionParser(ContributionParser):
    def __init__(self, project, args):
        super().__init__(project, args)
        self._get_repo(REPOS_DIR)

    def get_other_contributions(self, author):
        commits = list()

        cmd = [
            'git',
            'log',
            '--date=short',
            '--after={}'.format(self.args.period_start),
            '--until={}'.format(self.args.period_end),
            '--pretty=format:id=%H##date=%ad##author=%an##email=%ae##subject=%s',
            '--regexp-ignore-case',
        ]

        # The contribution type. Don't care about lower/upper case.
        # case is ignored (-i/--regexp-ignore-case option)
        contributions = [
            "signed-off-by",
            "reported-by",
            "tested-by",
            "suggested-by",
            "reviewed-by",
            "co-developed-by",
            "acked-by"
        ]
        for c in contributions:
            for email in author.emails:
                cmd.append('--grep')
                cmd.append('{}:.*{}'.format(c, email))

        output = subprocess.check_output(cmd, cwd=self.repodir)
        for line in output.splitlines():
            try:
                commit = self._get_commit_from_line(line)

                # skip if author of commit is same as user (author)
                if commit['email'] in author.emails:
                    continue

                commits.append(commit)

            except ValueError:
                print('ignore', line)

        for commit in commits:
            self.create_commit_link(commit)

        return commits

    def get_authored_contributions(self, author):
        commits = list()

        cmd = [
            'git',
            'log',
            '--date=short',
            '--pretty=format:id=%H##date=%ad##author=%an##email=%ae##subject=%s',
            '--after={}'.format(self.args.period_start),
            '--until={}'.format(self.args.period_end),
            '--author={}'.format(author.name),
            ]
        output = subprocess.check_output(cmd, cwd=self.repodir)
        for line in output.splitlines():
            try:
                commit = self._get_commit_from_line(line)
                if commit['email'].lower() not in [a.lower() for a in author.emails]:
                    continue
                commits.append(commit)
            except ValueError:
                print('ignore', line)

        for commit in commits:
            self.create_commit_link(commit)

        return commits

    def _create_repos_dir(self):
        if not os.path.exists(REPOS_DIR):
            os.makedirs(REPOS_DIR)

    def _get_repo(self, repos_dir):
        self._create_repos_dir()
        self.repodir = os.path.join(REPOS_DIR, self.project.name)
        print(self.repodir)

        try:
            cmd = [
                'git',
                'clone',
                self.project.giturl,
                self.project.name
                ]
            o = subprocess.check_output(cmd, cwd=REPOS_DIR)
        except subprocess.CalledProcessError:
            # assume we already cloned and now we can fetch/pull
            cmd = [
                'git',
                'pull'
                ]
            o = subprocess.check_output(cmd, cwd=self.repodir)

    #    try:
    #        cmd = [
    #             'git',
    #             'checkout',
    #             '{}'.format(project.branch)
    #             ]
    #        o = subprocess.check_output(cmd, cwd=project_repo_dir)
    #    except subprocess.CalledProcessError:
    #        print('cannot switch to branch "{}"'.format(project.branch))
    #        sys.exit(1)

    def _get_commit_from_line(self, line):
        commit = {}
        values = line.decode().split('##')
        for value in values:
            s = value.split('=')
            commit[s[0]] = s[1]
        return commit