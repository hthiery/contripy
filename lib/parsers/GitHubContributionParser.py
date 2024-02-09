from .ContributionParser import ContributionParser

from datetime import datetime
from python_graphql_client import GraphqlClient
import requests

class GitHubContributionParser(ContributionParser):
    def __init__(self, project, args, token):
        super().__init__(project, args)
        self.client = GraphqlClient(endpoint="https://api.github.com/graphql")
        self.token = token

    def _get_authored_contributions(self, author, start, end):
        commits = list()
        has_next_page = True
        after_cursor = None
        emails_string = str(author.emails).replace('\'', '\"')

        query = f"""
        query {{
            repository(
                name: "{ self.project.repo['name'] }"
                owner: "{ self.project.repo['owner'] }"
            ) {{
                defaultBranchRef {{
                target {{
                    ... on Commit {{
                    history(
                        author: {{ emails: { emails_string } }}
                        after: { after_cursor if after_cursor else "null" }
                        since: "{ start.isoformat() }"
                        until: "{ end.isoformat() }"
                    ) {{
                        totalCount
                        pageInfo {{
                            hasNextPage
                            endCursor
                        }}
                        nodes {{
                        ... on Commit {{
                            oid
                            messageHeadline
                            committedDate
                            author {{
                                email
                            }}
                        }}
                        }}
                    }}
                    }}
                }}
                }}
            }}
        }}
        """

        while has_next_page:
            data = self.client.execute(
                query=query,
                headers={"Authorization": "Bearer {}".format(self.token)},
            )

            history = data["data"]["repository"]["defaultBranchRef"]["target"]["history"]

            for contribution in history["nodes"]:
                commit = {
                    "id": contribution["oid"],
                    "subject": contribution["messageHeadline"],
                    "date": contribution["committedDate"],
                    "author": author.name,
                    "email": contribution["author"]["email"]
                }
                commits.append(commit)

            has_next_page = history["pageInfo"]["hasNextPage"]
            after_cursor = history["pageInfo"]["endCursor"]

        for commit in commits:
            self.create_commit_link(commit)

        return commits

    def get_authored_contributions(self, author):
        try_count = 1
        try_count_max = 10
        commits = list()

        start = datetime.strptime(self.args.period_start, '%Y-%m-%d')
        end = datetime.strptime(self.args.period_end, '%Y-%m-%d')

        #
        # For large projects like the Linux kernel repository, GitHub returns
        # server errors (502) when trying to fetch many commits. Implement
        # a workaround to retry with smaller time periods and accumulate the
        # commits from each API call.
        #
        while try_count <= try_count_max:
            try:
                split_period = (end - start) / try_count
                temp = list()
                for i in range(0, try_count):
                    next_start = start + split_period * i
                    next_end = start + split_period * (i + 1)
                    temp += (self._get_authored_contributions(author, next_start, next_end))
                commits += temp
                break
            except requests.exceptions.HTTPError as err:
                if err.response.status_code == 502:
                    # retry with smaller time period
                    try_count += 1
                else:
                    raise(err)

        if try_count > try_count_max:
            print('Failed to retrieve contributions from GitHub API')
            return None

        return commits

    def update_project(self):
        query = f"""
        query {{
            repository(
                name: "{ self.project.repo['name'] }"
                owner: "{ self.project.repo['owner'] }"
            ) {{
                description
            }}
        }}
        """

        data = self.client.execute(
            query=query,
            headers={"Authorization": "Bearer {}".format(self.token)},
        )

        project = data["data"]["repository"]

        if not self.project.description:
            self.project.description = project['description']