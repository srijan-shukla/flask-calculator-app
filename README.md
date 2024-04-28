# Flask Calculator App

This is a simple calculator application built with Flask. The application supports basic arithmetic operations: addition, subtraction, multiplication, and division.

## Project Structure

The FLASK-CALCULATOR-APP project has the following structure:

```
FLASK-CALCULATOR-APP
│
├── app.py
├── templates/
│   ├── index.html
├── requirements.txt
|-- test_app.py
└── README.md
```

## Setup and Installation

1. Clone the repository to your local machine.
2. Install the required packages using pip:

```
pip3 install -r requirements.txt
```

3. Run the application:

```
python3 app.py
```

The application will be accessible at `http://localhost:5000`.

## Usage

Navigate to the home page and enter two numbers. Select the operation you want to perform (addition, subtraction, multiplication, or division) and click "Calculate". The result will be displayed on the page.



# GITHUB WORKFLOW EXPLANATION

# 1. Steps to Use IAM roles to connect GitHub Actions to actions in AWS

        1. Create an OIDC provider in aws account by running the below comamnd 

            ```
            aws iam create-open-id-connect-provider ‐‐url 
            "https://token.actions.githubusercontent.com" ‐‐thumbprint-list 
            <your-thumbprint-list> ‐‐client-id-list 
            'sts.amazonaws.com'
            ```

        2. Create IAM ROLE , Trust Relationship with below command 

            ```
            echo '{
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {
                        "Federated": "<arn:aws:iam::<aws-acoount-id>:oidc-provider/token.actions.githubusercontent.com>"
                    },
                    "Action": "sts:AssumeRoleWithWebIdentity",
                    "Condition": {
                        "StringEquals": {
                            "token.actions.githubusercontent.com:sub": "repo: <example/EXAMPLEREPO>:ref:refs/heads/<ExampleBranch>",
                            "token.actions.githubusercontent.com:aud": "sts.amazonaws.com"
                        }
                    }
                }
                ]
            }' > trust-policy.json

            aws iam create-role --role-name <ROLE-NAME> --assume-role-policy-document file://trust-policy.json
            ```

        3. Assign Required policies to the role by runing 

            ```
            aws iam attach-role-policy --role-name "ROLE_NAME" \
            --policy-arn "arn:${AWS_PARTITION}:iam::aws:policy/AmazonEKSWorkerNodePolicy"
            aws iam attach-role-policy --role-name "ROLE_NAME" \
            --policy-arn "arn:${AWS_PARTITION}:iam::aws:policy/AmazonEKSClusterPolicy"
            aws iam attach-role-policy --role-name "ROLE_NAME" \
            --policy-arn "arn:${AWS_PARTITION}:iam::aws:policy/AWSAppRunnerServicePolicyForECRAccess"
            aws iam attach-role-policy --role-name "ROLE_NAME" \
            --policy-arn "arn:${AWS_PARTITION}:iam::aws:policy/AWSECRPullThroughCache_ServiceRolePolicy"    
            ```

# 2. Working of  BUILD-PUSH-DEPLOY Workflow:

Store values of AWS_DEFAULT_REGION, AWS_ROLE_SESSION_NAME, AWS_ROLE_NAME, AWS_ACCOUNT_ID, SecurityGroupID, CertificateArn as Github Secrets.

The workflow gets triggered on every push to master branch.

There are 3 jobs in workflow test, build , deploy.

In test job the unit-tests are run on application.

In build job docker image is prepared and pushed to ecr with the latest COMMIT TAG.

In deploy job the image is pulled from ecr and depoloyed to kubernetes cluster with the help of helm chart.