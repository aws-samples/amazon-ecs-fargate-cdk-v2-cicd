# amazon-ecs-fargate-cdk-cicd-v2
## _Disclaimer!_ DRAFT SOFTWARE NOT FOR PRODUCTION

This is the CDK Version 2 evolution of this sample project.

_A complete DevOps enabled sample containerized application_

This project builds a complete sample containerized Flask application publically available on AWS, using Fargate, ECS, CodeBuild, and CodePipline to produce a fully functional pipline to continuously roll out
changes to your new app.

## Getting Started

The recommended approach is to [use Cloud9](#GiveMeALink) you can also use your
own Linux based env easily with this guide.


Launch a `t2.micro` [Cloud9 us-east-1](https://us-east-1.console.aws.amazon.com/codesuite/codepipeline/pipelines) terminal and prepare it with following commands:

```bash
sudo yum install -y jq
export ACCOUNT_ID=$(aws sts get-caller-identity --output text --query Account)
export AWS_REGION=$(curl -s 169.254.169.254/latest/dynamic/instance-identity/document | jq -r '.region')
echo "export ACCOUNT_ID=${ACCOUNT_ID}" | tee -a ~/.bash_profile
echo "export AWS_REGION=${AWS_REGION}" | tee -a ~/.bash_profile
aws configure set default.region ${AWS_REGION}
aws configure get default.region
```

Ensure the Cloud9 instance is assigned a role of an administrator and from Cloud9 -> AWS Settings -> Credentials -> Disable the Temporary Credentials

Prepare CDK prerequisite:


```bash sudo yum install -y npm
npm install -g aws-cdk
npm install -g typescript@latest
```

### Configure the GitHub Repository and upload the application
Open https://github.com/aws-samples/amazon-ecs-fargate-cdk-cicd.
Login to GitHub, and fork the repository into your account.

Access your Cloud9 environment and run the following command from the `~/environment` directory, replacing USER-NAME with your GitHub username. 

```bash
git clone https://github.com/USER-NAME/amazon-ecs-fargate-cdk-cicd.git
```

### Secure your source code access

As a security best practice, never hard-code your GitHub token in the code. We will make use of AWS Secrets Manager service to store the GitHub token and use the CDK APIs to access the token from our code.

#### Github Personal access token

Navigate to Settings/Developer Settings/Personal access tokens. Create a new
token. The name of the token does not have dependencies.
However, be sure to give the token the following permissions:


// TODO - NEED TO REVIEW THESE PERMISSIONS!
//
* repo
* admin:org
* admin:repo_hook
* admin_org_hook


#### AWS Secrets Manager

Link the Github token to secret. The default name for this secret is `/aws-samples/amazon-ecs-fargate-cdk-cicd/github/personal_access_token`. 

To change the secret name, make the proper subsititions below,and then specify the optional `githubPersonalTokenParameterName` parameter during the [`cdk deploy step`](#launch-infrastructure-with-aws-cloud-developement-kit-cdk).

```bash
aws configure set region $AWS_REGION
aws secretsmanager create-secret \
 --name /aws-samples/amazon-ecs-fargate-cdk-cicd/github/personal_access_token \
 --secret-string <GITHUB-TOKEN> 
```

Once the above command is run, check if the secret is stored as expected using below command:

```bash
aws secretsmanager get-secret-value \
 --secret-id /aws-samples/amazon-ecs-fargate-cdk-cicd/github/personal_access_token \
 --version-stage AWSCURRENT
```

#### Authorize CodeBuild


Replace and then run the <GITHUB-TOKEN> with your GitHub Personal access token in the following snippet in you developement environment.

```bash

aws codebuild import-source-credentials --server-type GITHUB --auth-type PERSONAL_ACCESS_TOKEN --token <GITHUB-TOKEN> 
```

Verify the credential import worked.

```
aws codebuild list-source-credentials 
```

### Launch infrastructure with AWS Cloud Developement Kit (CDK)

Navigate to the `cdk-v2` directory and run the following commands:

```bash
cd cdk-v2
cdk init
cdk bootstrap aws://$ACCOUNT_ID/$AWS_REGION
cdk ls
```


```bash
cdk synth
cdk deploy
```


```bash
cdk deploy --parameters githubUserName=<YOUR_GITHUB_HANDLE>\
           --parameters githubPersonalTokenParameterName=<YOUR_GITHUB_PAT_SECRETNAME> \
           --context stackName=<YOUR_STACK_NAME>

```

You may be asked to confirm the creation of the roles and authorization before the CloudFormation is executed, for which, you can respond with a “Y”. The infrastructure will take approximately 5-10 minutes time to create, please wait until you see the output of CloudFormation printed on the terminal.


### Review Infrastructure and Application


When the CloudFormation deployment is complete fetch the URL from the CDK outputs. You can also see this in the AWS Web console.

<img src="images/stack-launch.png" />

Initially the app represent the base image (TODO - update this) 

<img src="images/web-default.png" />

<!-- more edits here needed -->

Once the CodePipeline is triggered, CodeBuild will run the set of commands to dockerize the application and push it to the Amazon ECR repository. Before deploying it to the ECS infrastructue, it will ask you for manual approval to move to the next stage. Once approved, it will deploy the application into ECS platform, by creating the task definition, service and instantiating the tasks to the desired count. In our case, the default desired count is 1 and thus an instance of flask application will be accessible from Load Balancer as shown above.
The deployment on the ECS initially will take around 5 minutes to ensure the older application task is gracefully drained out and the new task is launched. You would see the ECS service reach a Steady State (shown below), after which the application is accessible. Also notice that the Desired count number is reached.

<img src="images/ecs-steadystate.png" alt="dashboard" style="border:1px solid black">

On accessing the application via ALB, the content will be updated to be below image:

<img src="images/ecs-deployed.png" alt="dashboard" style="border:1px solid black">

Once code commited and CodePipeline is kicked off, it will deploy the application to the fargate. The successful run of the CI/CD pipeline would look like below:

<img src="images/stage12-green.png" alt="dashboard" style="border:1px solid black">
<img src="images/stage34-green.png" alt="dashboard" style="border:1px solid black">



## License
This library is licensed under the MIT-0 License. See the [LICENSE](/LICENSE) file.
