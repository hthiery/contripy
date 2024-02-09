class ContributionParser:
    def __init__(self, project, args):
        self.project = project
        self.args = args

    def get_other_contributions(self, author):
        return []

    def get_authored_contributions(self, author):
        return []

    def update_project(self):
        pass

    def create_commit_link(self, commit):
        commit['link'] = self.project.gitweburl.replace('%COMMIT-ID%', commit['id'])