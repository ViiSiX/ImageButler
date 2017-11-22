import click
from ..models import UserModel
from ..imagebutler import db
from sqlalchemy import exc as sa_exc


@click.group()
def user():
    pass


@user.command('create')
@click.argument('email')
def create_user_command(email):
    """Create and activate an user."""
    try:
        new_user = UserModel(email)
        new_user.is_active = True
        db.session.add(new_user)
        db.session.commit()
        click.echo("Scc: User has been added successfully for \"{0}\"".format(
            email
        ))
        click.echo("- Username: {0}\n- Password: {1}".format(
            new_user.user_name, new_user.password
        ))
    except sa_exc.IntegrityError:
        click.echo("Err: This email has already been added.", err=True)

    db.session.close()


@user.command('get')
@click.argument('email')
def get_user_command(email):
    """Return a username and password of an given email."""
    existed_user = UserModel.query.filter_by(email=email).first()
    if existed_user:
        click.echo("Scc: User \"{0}\":".format(email))
        click.echo("- Username: {0}\n- Password: {1}".format(
            existed_user.user_name, existed_user.password
        ))
    else:
        click.echo("Err: User \"{0}\" has not existed in the system.".format(
            email
        ))


@user.command('change_pass')
@click.argument('email')
def set_user_new_password_command(email):
    """Set new password for user having given email."""
    existed_user = UserModel.query.filter_by(email=email).first()
    if existed_user:
        existed_user.change_password()
        db.session.commit()
        click.echo("Scc: User \"{0}\" has been updated:".format(email))
        click.echo("- Username: {0}\n- Password: {1}".format(
            existed_user.user_name, existed_user.password
        ))
    else:
        click.echo("Err: User \"{0}\" has not existed in the system.".format(
            email
        ))
