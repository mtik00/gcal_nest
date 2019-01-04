import os
import click
from jinja2 import Environment, StrictUndefined, FileSystemLoader
import ruamel.yaml


def get_template(name):
    template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'templates'))
    with open(os.path.join(template_dir, name)) as fh:
        text = fh.read()

    return text


@click.command()
def build():
    """
    Build the utility
    """
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
    instance_dir = os.path.abspath(os.path.join(base_dir, 'instance'))
    outdir = os.path.join(base_dir, '_build')

    site_config_file = os.path.join(instance_dir, 'site.yaml')
    if not os.path.exists(site_config_file):
        click.echo('ERROR: Could not find %s' % site_config_file)
        click.echo('...a sample is located in `conf`')
        click.echo('...copy `conf/site-sample.yaml` to your instance folder as `site.yaml`, and modify it as needed')
        click.echo('...we think your instance folder is here: ' + instance_dir)
        raise click.Abort()

    options = ruamel.yaml.safe_load(open(site_config_file).read())

    if not os.path.isdir(outdir):
        os.makedirs(outdir)

    ###########################################################################
    click.echo('Creating `_build/gcal-nest-systemd.service')
    template = get_template('gcal-nest-systemd.service')
    content = template.format(**options)
    with open(os.path.join(outdir, 'gcal-nest-systemd.service'), 'wb') as fh:
        fh.write(content.encode('utf-8'))
    click.echo('...done')
    ###########################################################################

    ###########################################################################
    click.echo('Creating `_build/deploy.bash')
    template = get_template('deploy.bash')
    content = template.format(**options)
    with open(os.path.join(outdir, 'deploy.bash'), 'wb') as fh:
        fh.write(content.encode('utf-8'))
    click.echo('...done')
    ###########################################################################

    ###########################################################################
    click.echo('Creating `_build/circus.ini')
    template = get_template('circus.ini')
    content = template.format(**options)
    with open(os.path.join(outdir, 'circus.ini'), 'wb') as fh:
        fh.write(content.encode('utf-8'))
    click.echo('...done')
    ###########################################################################
