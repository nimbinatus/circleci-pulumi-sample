"""A Google Cloud Python Pulumi program"""

import pulumi
import pulumi_gcp

config = pulumi.Config()

cloud_run = pulumi_gcp.cloudrun.Service(
    "gunicorn-service",
    location=pulumi.Config("gcp").require("region"),
    template=pulumi_gcp.cloudrun.ServiceTemplateArgs(
        spec=pulumi_gcp.cloudrun.ServiceTemplateSpecArgs(
            containers=[pulumi_gcp.cloudrun.ServiceTemplateSpecContainerArgs(
                image=f'gcr.io/{pulumi.Config("gcp").require("project")}/gunicorn-image:latest',
                ports=[pulumi_gcp.cloudrun.ServiceTemplateSpecContainerPortArgs(
                    container_port=8080
                )]
            )]
        )
    ),
    traffics=[
        pulumi_gcp.cloudrun.ServiceTrafficArgs(
            latest_revision=True,
            percent=100
        )
    ]
)

pulumi.export("cloud_run_url", cloud_run.statuses)
