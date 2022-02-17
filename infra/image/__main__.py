"""A Python Pulumi program"""

import os
import pulumi
import pulumi_gcp as gcp
import pulumi_google_native as gcp_native
import pulumi_docker as docker
from pathlib import Path

path = Path(os.getcwd())
config = pulumi.Config('google-native')
location = config.require('region')
project = config.require('project')
repo_name = "gunicorn-image"
gimage = "gunicorn-image"

if 'CIRCLE_BRANCH' in os.environ and os.environ['CIRCLE_BRANCH'] != 'main':
    tag = os.environ['CIRCLE_BUILD_NUM']
else:
    tag = 'latest'

registry = gcp_native.artifactregistry.v1beta2.Repository(
    f'{gimage}',
    location=f'{pulumi.Config("google-native").require("region")}',
    repository_id=f'{gimage}',
    format=gcp_native.artifactregistry.v1beta2.RepositoryFormat("DOCKER"),
)

gunicorn_image = docker.Image(
    gimage,
    build=f'{path.parents[1]}/api',
    image_name=f'{location}-docker.pkg.dev/{project}/{repo_name}/{gimage}:{tag}',
    opts=pulumi.ResourceOptions(depends_on=[registry])
)
pulumi.export("image name", gunicorn_image.image_name)
