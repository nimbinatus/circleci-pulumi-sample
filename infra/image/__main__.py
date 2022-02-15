"""A Python Pulumi program"""

import os
import pulumi
import pulumi_gcp as gcp
import pulumi_google_native as gcp_native
import pulumi_docker as docker
from pathlib import Path

import pulumi_docker.docker

path = Path(os.getcwd())
config = pulumi.Config()

gimage = "gunicorn-image"
if 'CIRCLE_BRANCH' in os.environ and os.environ['CIRCLE_BRANCH'] != 'main':
    tag = os.environ['CIRCLE_BUILD_NUM']
else:
    tag = 'latest'

try:
    # First, we check if the Artifact Registry exists, and we add it to Pulumi if it does and isn't already imported.
    print('attempting')
    registry_name = gcp_native.artifactregistry.v1beta2.get_repository(
        location=pulumi.Config("google-native").require("region"),
        project=pulumi.Config("google-native").require("project"),
        repository_id=gimage
    )
    registry = gcp.artifactregistry.Repository(
        f'{gimage}',
        location=f'{pulumi.Config("google-native").require("region")}',
        project=f'{pulumi.Config("google-native").require("project")}',
        repository_id=f'{gimage}',
        format=gcp_native.artifactregistry.v1beta2.RepositoryFormat("DOCKER"),
        opts=pulumi.ResourceOptions(import_=f'gcp:artifactregistry/repository:Repository default {registry_name.name}')
    )
    gcp_native.artifactregistry.v1beta2.get_repository_output(repository_id=gimage).apply(lambda registry: print(registry.name))
except Exception as err:
    # If the registry does not exist, we make it.
    print(f'No artifact registry by that name. Spinning one up.')
    registry = gcp_native.artifactregistry.v1beta2.Repository(
        f'{gimage}',
        location=f'{pulumi.Config("google-native").require("region")}',
        repository_id=f'{gimage}',
        description="repo for docker images for test run",
        format=gcp_native.artifactregistry.v1beta2.RepositoryFormat("DOCKER"),
    )
    gcp_native.artifactregistry.v1beta2.get_repository_output(repository_id=registry.id).apply(lambda registry: print(registry.name))

try:
    image_name = gcp_native.artifactregistry.v1beta2.get_repository_output(
        location=pulumi.Config("google-native").require("region"),
        project=pulumi.Config("google-native").require("project"),
        repository_id=gimage
    ).apply(
        lambda registry: f'{pulumi.Config("google-native").require("region")}-docker.pkg.dev/{registry.name}/{gimage}:{tag}'
    )
    gunicorn_image = docker.Image(
        gimage,
        build=f'{path.parents[1]}/api',
        image_name=image_name,
        opts=pulumi.ResourceOptions(depends_on=[registry])
    )
    pulumi.export("image name", gunicorn_image.image_name)
except pulumi_docker.docker.ResourceError as err:
    print(f"Failure: {err}")

