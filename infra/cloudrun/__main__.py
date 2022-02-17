"""A Google Cloud Python Pulumi program"""
import os
import pulumi
import pulumi_gcp as gcp

config = pulumi.Config('google-native')
location = config.require('region')
project = config.require('project')
repo_name = "gunicorn-image"
gimage = "gunicorn-image"

if 'CIRCLE_BRANCH' in os.environ and os.environ['CIRCLE_BRANCH'] != 'main':
    container_tag = os.environ['CIRCLE_BUILD_NUM']
else:
    container_tag = 'latest'

cloud_run = gcp.cloudrun.Service(
    "gunicorn-service",
    location=pulumi.Config("gcp").require("region"),
    template=gcp.cloudrun.ServiceTemplateArgs(
        spec=gcp.cloudrun.ServiceTemplateSpecArgs(
            containers=[gcp.cloudrun.ServiceTemplateSpecContainerArgs(
                image=f'{location}-docker.pkg.dev/{project}/{repo_name}/{gimage}:{container_tag}',
                ports=[gcp.cloudrun.ServiceTemplateSpecContainerPortArgs(
                    container_port=8080
                )]
            )]
        )
    ),
    traffics=[
        gcp.cloudrun.ServiceTrafficArgs(
            latest_revision=True,
            percent=100
        )
    ]
)

noauth_iam_policy = gcp.organizations.get_iam_policy(
    bindings=[gcp.organizations.GetIAMPolicyBindingArgs(
        role="roles/run.invoker",
        members=["allUsers"],
    )]
)

noauth_iam_policy = gcp.cloudrun.IamPolicy(
    "noauthIamPolicy",
    location=cloud_run.location,
    project=cloud_run.project,
    service=cloud_run.name,
    policy_data=noauth_iam_policy.policy_data
)

pulumi.export("cloud_run_url", cloud_run.statuses)
