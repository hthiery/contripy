class Project(object):
    def __init__(self, name, cfg):
        self.name = name
        self.url = cfg['url']
        self.giturl = cfg['giturl']
        self.gitweburl = cfg['gitweburl']

        if 'description' in cfg:
            self.description = cfg['description']
        else:
            self.description = None

        if 'parser' in cfg:
            self.parser = cfg['parser']
        else:
            self.parser = 'git'

        if 'skip-users' in cfg:
            self.skip_users = cfg['skip-users']
        else:
            self.skip_users = None

        if 'only-users' in cfg:
            self.only_users = cfg['only-users']
        else:
            self.only_users = None

        if 'branch' in cfg:
            self.branch = cfg['branch']
        else:
            self.branch = 'master'

        if self.giturl.startswith("https://github.com/"):
            repo = self.giturl.split("/")[-1]
            owner = self.giturl[len("https://github.com/"):-(len(repo)+1)]
            self.repo = {
                "name": repo,
                "owner": owner
            }


class Author(object):
    def __init__(self, name, cfg):
        self.name = name
        self.emails = cfg['emails']
        self.projects = {}

    def _add_contributions(self, project, commits, contribution):
        commits = sorted(commits, key=lambda k: k['date'], reverse=True)
        if project not in self.projects:
            self.projects[project] = {}
        self.projects[project][contribution] = commits

    def add_authored_contributions(self, project, commits):
        """Add authored commits."""
        self._add_contributions(project, commits, 'authored')

    def add_other_contributions(self, project, commits):
        """Add other contributions."""
        self._add_contributions(project, commits, 'others')