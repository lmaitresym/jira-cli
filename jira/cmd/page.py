# -*- coding: utf-8 -*-
import typer
from jira.api.page_client import PageClient
import json

app = typer.Typer(help="Manage pages")

@app.command(help="Get a page")
def get(
    page_title: str = typer.Argument(help="The page title"),
    space_key: str = typer.Argument(help="The space key")
    ):
    result = PageClient().getPage(space_key, page_title)
    #print("{} / {} / {} / {}".format(page_title, space_key, rc, self.options), file=sys.stderr)
    print(json.dumps(result, indent=2))
    return result

@app.command(help="Delete a page")
def delete(page_id: str = typer.Argument(help="The page id")):
    result = PageClient().deletePage(page_id)
    print(json.dumps(result, indent=2))
    return result

@app.command(help="Create a page")
def create(
    page_title: str = typer.Argument(help="The page title"),
    space_key: str = typer.Argument(help="The space key"),
    parent_id: str = typer.Argument(help="The parent page id"),
    page_file: str = typer.Argument(help="The page file")
    ):
    if page_file:
        with open(page_file,'r') as page_raw:
            page_content = page_raw.read()
    else:
        page_content = ""
    result = PageClient().createPage(page_title, space_key, page_content, parent_id)
    print(json.dumps(result, indent=2))
    return result

@app.command(help="Update a page")
def update(
    page_title: str = typer.Argument(help="The page title"),
    space_key: str = typer.Argument(help="The space key"),
    page_file: str = typer.Argument(help="The page file")
    ):
    with open(page_file,'r') as page_raw:
        page_content = page_raw.read()
        result = PageClient().updatePage(page_title, space_key, page_content)
        print(json.dumps(result, indent=2))
        return result

@app.command(help="Move a page")
def move(
    page_title: str = typer.Argument(help="The page title"),
    space_key: str = typer.Argument(help="The space key"),
    parent_id: str = typer.Argument(help="The parent page id")
    ):
    result = PageClient().movePage(page_title, space_key, parent_id)
    print(json.dumps(result, indent=2))
    return result
