"""A Python Pulumi program"""

import os
import pulumi
# import pulumi_gcp as gcp
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
    print('attempting')
    gcp_native.artifactregistry.v1beta2.get_repository(
        repository_id=f'{gimage}'
    )
except Exception as err:
    print(f'No artifact registry by that name: {err}. Spinning one up.')
    # gcp_native.artifactregistry.v1beta2.Repository(
    #     f'{gimage}',
    #     location=f'{pulumi.Config("gcp").require("region")}',
        # repository_id=f'{gimage}',
        # description="repo for docker images for test run",
        # format=gcp_native.artifactregistry.v1beta2.RepositoryFormat("DOCKER"),
    # )

# try:
#     gunicorn_image = docker.Image(
#         gimage,
#         build=f'{path.parents[1]}/api',
#         image_name=f'us-central-docker.pkg.dev/{pulumi.Config("gcp").require("project")}/{gimage}/{gimage}:{tag}'
#     )
# except pulumi_docker.docker.ResourceError as err:
#     print(f"Failure: {err}")

# pulumi.export("digest", gunicorn_image.digest)
