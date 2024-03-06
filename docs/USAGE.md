# Usage

## Installation of the tool

```sh
$ pip install -e .[test]
```

## Setup

```sh
export JIRA_CONFIG=${HOME}/Workspaces/MyCompany/Files/.jira
```

## Create pages and tree of pages in Confluence

```sh
export SPACE_KEY="~87241583"
export PARENT_PAGE_TITLE="SCRUM Tests"
$ jira page get "$SPACE_KEY" "$PARENT_PAGE_TITLE" | jq '.results[0]|.id'
"990807720"
$ jira page create "$SPACE_KEY" "X SRE Scrum Reports - 2020-02" "990807720"
...
$ jira page create "$SPACE_KEY" "X SRE Scrum Reports - 2020-02-03" "990807720"
...
$ jira page get "$SPACE_KEY" "X SRE Scrum Reports - 2020-02" | jq '.results[0]|.id'
"1933839849"
$ jira page get "$SPACE_KEY" "X SRE Scrum Reports - 2020-02-03" | jq '.results[0]|.id'
"1936556127"
$ jira page move "$SPACE_KEY" "X SRE Scrum Reports - 2020-02-03" "1933839849"
$ jira page move "$SPACE_KEY" "X SRE Scrum Reports - 2020-02-03" "990807720"
```

## Move pages in Confluence

Move one month:

```sh
$ SPACE_KEY=SRE
# Create monthly page
$ MONTH_PAGE_ID=$(jira page create "$SPACE_KEY" "SRE Scrum Reports - 2023-03" "$TOP_PAGE_ID" | jq -r '.id')
# Move daily pages under monthly page
$ export END=31
$ for i in $(seq 1 $END); do jira page move "ES" "SRE Scrum report - 2023-03-"`printf "%2.0d\n" $i |sed "s/ /0/"` "$MONTH_PAGE_ID" | jq '.id'; done
...
```

Move one year:

```sh
$ TOP_PAGE_ID=782699699
$ SPACE_KEY=SRE
$ YEARLY_PAGE_ID=$(jira page create "$SPACE_KEY" "SRE Scrum Reports - 2023" "$TOP_PAGE_ID" | jq -r '.id')
# Move monthly pages under yearly page
$ export END=12
$ for i in $(seq 1 $END); do jira page move "$SPACE_KEY" "SRE Scrum Reports - 2023-"`printf "%2.0d\n" $i |sed "s/ /0/"` "$YEARLY_PAGE_ID" | jq -r '.id'; done
...
```
