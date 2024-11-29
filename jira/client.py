import typer

# from tenant_tools import mongo
# from tenant_tools import tlm

app = typer.Typer()
# app.add_typer(mongo.app, name="mongo")
# app.add_typer(tlm.app, name="tlm")

if __name__ == '__main__':
    app()
