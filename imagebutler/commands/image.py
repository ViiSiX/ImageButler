import click
import progressbar
from ..models import ImageModel
from ..imagebutler import db


@click.group()
def image():
    pass


@image.command('gen_thumbnail')
@click.option('--type')
def thumbnail_regen(**kwargs):
    """Generate thumbnail for all|missing images. For first implement, we
    do not care about performance, save that task for later."""
    if kwargs['type'] in ('all', 'missing'):
        images_progressed = 0

        if kwargs['type'] == 'all':
            images_count = ImageModel.query.count()
            images = ImageModel.query.all()
        else:
            images_count = ImageModel.query.filter(
                ImageModel.file_thumbnail.is_(None)
            ).count()
            images = ImageModel.query.filter(
                ImageModel.file_thumbnail.is_(None)
            ).all()

        bar = progressbar.ProgressBar(max_value=images_count)
        for processing_image in images:
            processing_image.file_thumbnail = processing_image.gen_thumbnail()
            db.session.commit()
            images_progressed += 1
            bar.update(images_progressed)

    else:
        click.echo('Usage: flask image gen_thumbnail all|missing',
                   err=True)
