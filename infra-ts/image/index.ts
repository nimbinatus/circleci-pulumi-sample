// Modified from https://gist.github.com/cnunciato/32e9d52a5bd45e47dcdde71f6ac24c5f

import * as path from "path";
import * as pulumi from "@pulumi/pulumi";
import * as docker from "@pulumi/docker";
import * as ngcp from "@pulumi/google-native";

const config = new pulumi.Config('google-native');
const location = config.require('region');
const project = config.require('project');
let tag;
let gimage;
let repo_name

if (process.env.CIRCLE_BRANCH && process.env.CIRCLE_BRANCH != 'main') {
    tag = process.env.CIRCLE_BUILD_NUM;
    gimage = `gunicorn-image-${tag}`;
    repo_name = `gunicorn-image-${tag}`;
} else {
    tag = 'latest';
    gimage = 'gunicorn-image';
    repo_name = 'gunicorn-image';
}



const my_provider = new ngcp.Provider(
    "gcp-config",
    {
        project: process.env.GOOGLE_PROJECT_ID,
        region: process.env.GOOGLE_COMPUTE_REGION,
        zone: process.env.GOOGLE_COMPUTE_ZONE
    }
)

const registry = new ngcp.artifactregistry.v1beta2.Repository(
    gimage, {
        location: `${config.require("region")}`,
        repositoryId: gimage,
        format: "DOCKER",
    }, {
        provider: my_provider
    });

const gunicornImage = new docker.Image(
    gimage, {
        build: `${path.join(__dirname, '../../')}api`,
        imageName: `${location}-docker.pkg.dev/${project}/${repo_name}/${gimage}:${tag}`
    }, {
        dependsOn: [registry],
        provider: my_provider
    })

export const imageName = gunicornImage.imageName