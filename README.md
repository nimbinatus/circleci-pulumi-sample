# circleci-pulumi-sample
Sample app built to run on Google Cloud (GCP) with Pulumi and CircleCI

This app is a simple RESTful API built with Falcon. There are two endpoints. `/` should return `{'response': 'OK'}`.
`/hello` should return `{'response': 'hello, world'}`. If you add a query string with a name parameter (e.g.,
`/hello?name=Laura`), you will receive `{'response': 'hello, <name>'}` (e.g., `{'response': 'hello, Laura'}`) instead.
