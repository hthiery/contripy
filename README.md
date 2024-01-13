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
