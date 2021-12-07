"""A Python Pulumi program"""

import os
import pulumi
# import pulumi_gcp as gcp
import pulumi_docker as docker
from pathlib import Path

path = Path(os.getcwd())
config = pulumi.Config()

gimage = "gunicorn-image"
if 'CIRCLE_BRANCH' in os.environ and os.environ['CIRCLE_BRANCH'] != 'main':
    tag = os.environ['CIRCLE_BUILD_NUM']
else:
    tag = 'latest'

print(f'gcr.io/{pulumi.Config("gcp").require("project")}/{gimage}:{tag}')
gunicorn_image = docker.Image(
    gimage,
    build=f'{path.parents[1]}/api',
    image_name=f'gcr.io/{pulumi.Config("gcp").require("project")}/{gimage}:{tag}'
)

# pulumi.export("digest", gunicorn_image.digest)
