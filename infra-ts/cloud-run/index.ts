import * as pulumi from "@pulumi/pulumi";
import * as gcp from "@pulumi/gcp";
import * as ngcp from "@pulumi/google-native";

const config = new pulumi.Config('google-native');
const location = config.require('region');
const project = config.require('project');
const repo_name = "gunicorn-image";
const gimage = "gunicorn-image";
let container_tag;

if (process.env.CIRCLE_BRANCH && process.env.CIRCLE_BRANCH != 'main') {
    container_tag = process.env.CIRCLE_BUILD_NUM;
} else {
    container_tag = 'latest'
}

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
    })

const noauth = gcp.organizations.getIAMPolicy({
    bindings: [
        {
            role: "roles/run.invoker",
            members: ["allUsers"],
        }
    ]
})

const noauth_iam_policy = new gcp.cloudrun.IamPolicy(
    "noauthIamPolicy", {
        location: cloud_run.location,
        project: cloud_run.project,
        service: cloud_run.name,
        policyData: noauth.then(noauth => noauth.policyData)
    })

export const cloudRunUrl = cloud_run.statuses[0].url

