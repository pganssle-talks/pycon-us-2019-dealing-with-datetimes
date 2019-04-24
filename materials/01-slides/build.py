#!/usr/bin/env python3
"""
Builds the notebook and checks out the relevant files into gh-pages
"""

import logging

import os
import shutil
import subprocess
import tempfile

import click

try:
    import ruamel.yaml as yaml
except ImportError:
    import yaml


def load_config(config):
    with open(config, 'r') as yf:
        conf_dict = yaml.safe_load(yf)

    return conf_dict


def get_current_git_ref():
    # Gets the current branch_name for HEAD (or HEAD)
    branch_name = subprocess.check_output(
        ['git', 'rev-parse', '--symbolic-full-name', '--verify',
         '--abbrev-ref', 'HEAD'])
    branch_name = branch_name.decode().strip()

    if branch_name == 'HEAD':
        # Instead use the current commit if we're in detached head mode
        branch_name = subprocess.check_output(
            ['git', 'rev-parse', '--verify', 'HEAD']
        ).decode.strip()

    return branch_name


def make_nbconfig(fpath, options):
    nbconfig = [
        "c = get_config()"
    ]

    for option, option_val in options:
        option_val = repr(option_val)
        nbconfig.append(f'c.{option} = {option_val}')

    with open(fpath, 'w') as f:
        f.write('\n'.join(nbconfig))


def make_slides(config, serve=False, browser=False):
    reveal_prefix = config.get('reveal_prefix', 'reveal.js')

    convert_cmd = [
        'jupyter', 'nbconvert',
        '--to=slides',
        '--reveal-prefix={}'.format(reveal_prefix)
    ]

    nbconfig_options = []

    template_path = config.get('template', None)
    if template_path is not None:
        convert_cmd.append('--template={}'.format(template_path))

    if serve:
        convert_cmd.extend(['--post', 'serve'])

        if not browser:
            nbconfig_options.append(('ServePostProcessor.open_in_browser', False))

    with tempfile.TemporaryDirectory() as td:
        if nbconfig_options:
            # For whatever reason --config only seems to work with a proper file
            nbconfig_path = os.path.join(td, 'nbconfig.py')
            make_nbconfig(nbconfig_path, nbconfig_options)

            convert_cmd.extend(['--config', nbconfig_path])

        convert_cmd.append(config.get('notebook', 'notebook.ipynb'))

        rv = subprocess.check_call(convert_cmd)

    return rv

@click.group()
def cli():
    pass


@cli.command()
@click.option('-c', '--config', type=click.Path(exists=True),
              default='build_config.yml')
@click.option('--serve', is_flag=True, default=False,
              help='Whether or not to serve the notebook after the build.')
@click.option('--browser', is_flag=True, default=False,
              help='Whether or not to open the notebook in browser when serving')
def make(config, serve, browser):
    """
    Used to build the notebook in the local folder (on the local branch).
    """
    conf = load_config(config)

    make_slides(conf, serve=serve, browser=browser)


@cli.command()
@click.option('-c', '--config', type=click.Path(exists=True),
              default='build_config.yml')
def pages(config):
    """
    Used to generate the slides and copy the current branch's version of the
    slides to the gh-pages branch.
    """
    logging.getLogger().setLevel(logging.INFO)

    conf = load_config(config)
    try:
        slides_loc = conf['slides']
    except KeyError:
        raise KeyError('Must specify slides output location in config')

    # Build the slides
    make_slides(conf)

    if not os.path.exists(slides_loc):
        raise ValueError('Could not find {}'.format(slides_loc))

    cur_git_ref = get_current_git_ref()   # So we can check stuff out from here
    logging.info('Checking out gh-pages, leaving {}'.format(cur_git_ref))

    # Check out the gh-pages branch
    subprocess.check_call(['git', 'checkout', 'gh-pages'])

    # Move the slides to index.html to update them
    logging.info('Moving slides from {} to index.html'.format(slides_loc))

    if os.path.exists('index.html'):
        shutil.move('index.html', 'index.html.bak')
    try:
        shutil.move(slides_loc, 'index.html')

        # Update the remaining files
        logging.info('Checking out specified data from {}'.format(cur_git_ref))
        subprocess.check_call(
            ['git', 'checkout', cur_git_ref] +
            conf.get('files', []) +            # Standalone files
            conf.get('dirs', [])               # Directories
        )
    except:
        shutil.move('index.html.bak', 'index.html')
        raise
    finally:
        if os.path.exists('index.html.bak'):
            os.remove('index.html.bak')

if __name__ == "__main__":
    cli()
