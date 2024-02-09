from .GitContributionParser import GitContributionParser

try:
    from python_graphql_client import GraphqlClient
except ImportError:
    print("Module python_graphql_client not installed, GitHub parser not available")
else:
    from .GitHubContributionParser import GitHubContributionParser