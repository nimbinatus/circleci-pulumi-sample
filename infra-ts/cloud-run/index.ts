import * as pulumi from "@pulumi/pulumi";
import * as gcp from "@pulumi/gcp";

const config = new pulumi.Config('google-native');
const location = config.require('region');
const project = config.require('project');
let repo_name;
let gimage;
let container_tag;

if (process.env.CIRCLE_BRANCH && process.env.CIRCLE_BRANCH != 'main') {
    container_tag = process.env.CIRCLE_BUILD_NUM;
    gimage = `gunicorn-image-${container_tag}`;
    repo_name = `gunicorn-image-${container_tag}`;
} else {
    container_tag = 'latest';
    gimage = 'gunicorn-image';
    repo_name = 'gunicorn-image';
}

const my_provider = new gcp.Provider(
    "gcp-provider",
    {
        project: process.env.GOOGLE_PROJECT_ID,
        region: process.env.GOOGLE_COMPUTE_REGION,
        zone: process.env.GOOGLE_COMPUTE_ZONE
    }
)

const cloud_run = new gcp.cloudrun.Service(
    "gunicorn-service", {
        location: `${config.require("region")}`,
        template: {
            spec: {
                containers: [{
                    image: `${location}-docker.pkg.dev/${project}/${repo_name}/${gimage}:${container_tag}`,
                    ports: [{
                        containerPort: 8080
                    }]
                }]
            }
        },
        traffics: [{
            latestRevision: true,
            percent: 100,
        }],
    }, {
        provider: my_provider
    })

const noauth = gcp.organizations.getIAMPolicy({
    bindings: [
        {
            role: "roles/run.invoker",
            members: ["allUsers"],
        }
    ]
}, {
    provider: my_provider
})

const noauth_iam_policy = new gcp.cloudrun.IamPolicy(
    "noauthIamPolicy", {
        location: cloud_run.location,
        project: cloud_run.project,
        service: cloud_run.name,
        policyData: noauth.then(noauth => noauth.policyData)
    }, {
        provider: my_provider
    })

export const cloudRunUrl = cloud_run.statuses[0].url

