# Usage

## Installation of the tool

```sh
$ pip install -e .[test]
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
$ jira page get "ES" "SRE SCRUM Reports"
"782699699"
```

Move one month:

```sh
$ jira page create "ES" "SRE Scrum Reports - 2021-04" "782699699" | jq '.id'
"1936556287"
$ export END=31
$ for i in $(seq 1 $END); do jira page move "ES" "SRE Scrum report - 2021-04-"`printf "%2.0d\n" $i |sed "s/ /0/"` "1936556287" | jq '.id'; done
...
```