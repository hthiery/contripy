# Collecting Contributions

This is a set of python scripts that collect contributions by author and
generates a report with asciidoctor.

## Requirements

For contripy script:

* envyaml (Python)
* python-dotenv (Python)

Additionally when using the Git parser:

* git

Additionally when using the GitHub parser:

* python-graphql-client (Python)
* requests (Python)

Additionally when using the report script:

* asciidoctor
* ruby-asciidoctor-pdf
* python3-dateutil (Python)

## Config Format

The config is in YAML format.

The config contains a list of projects and a list of authors.

```
projects:
  <PROJECT-NAME#0>:
    url: <PROJECT-URL>
    giturl: <PROJECT-GIT-URL>
    gitweburl: <PROJECT-GIT-WEB-URL>
  :
  :
  <PROJECT-NAME#n>:
    url: <PROJECT-URL>
    giturl: <PROJECT-GIT-URL>
    gitweburl: <PROJECT-GIT-WEB-URL>

authors:
  <AUTHOR-NAME#0>:
    emails:
	  - <EMAIL#0>
	  :
	  - <EMAIL#n>
  :
  <AUTHOR-NAME#n>:
    emails:
	  - <EMAIL#0>
	  :
	  - <EMAIL#n>

```

## Parsers

The following contribution parsers are available.

### Git Parser

The Git parser is the default and uses the local `git` CLI to clone the
repository and extract all the contributions by running `git log`. It can
be explicitly selected by using `parser: git` in the project config.

### GitHub Parser

The GitHub parser uses the GitHub GraphQL API to collect contributions for a
project without the need to do a full clone. Please note that it can only fetch
"authored" contributions and not "other" contributions.

Further the GitHub parser can be used to update the project description from
the description that is used in the GitHub project. This happens automatically
if the config doesn't specify a value for `description`.

The parser requires a GitHub API token in the config. Instead of adding the
token to the config it can be passed via environment variable or `.env` file.

#### config.yml

```yaml
parser:
  github:
    token: ${GITHUB_APITOKEN}
```

#### .env

```
GITHUB_APITOKEN=<token>
```

