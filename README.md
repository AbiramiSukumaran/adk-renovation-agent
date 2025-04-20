# adk-renovation-agent
Multiagent system (for kitchen renovation) using Vertex AI ADK and Gemini 2.5

## What is a multiagent system?

When your application has multiple agents working together autonomously and together as required to cater to it’s larger purpose with each of it’s agents being independently knowledgeable and responsible for a specific focus area, then your application becomes a multiagent system. Agents are autonomous programs that can make decisions generatively and based on instructions and information made available to them and are responsible for the specific area of focus for which they are created.

## Things to keep in mind for a multiagent system!

First, It’s important to have a proper understanding and reasoning of the specialization for each agent. - “do you know why you need a specific sub-agent for something”, work that out first.
Second, How to bring them together with a root agent to route and make sense of each of the responses.
Third, There are multiple types of agent routing that you can find here in this documentation. Make sure which one suits your application’s flow. Also what are the various contexts and states that you need for your multiagent system’s flow control.

## What are we building today?
Let’s build a multiagent system to handle kitchen renovations. That’s what we’ll do. We’ll build a system with 3 agents. 

Renovation Proposal Agent
Permits and Compliance Check Agent
Order Status Check Agent

## Renovation Proposal Agent, to generate the kitchen renovation proposal document. Permits and Compliance Agent, to take care of permits and compliance and Order Status Check Agent, to check order status. We have a root agent that orchestrates these agents based on the requirement.
Let’s dive right in!
Let’s get started with getting the multiagent system implemented.

### Setup GCP Project

Login to Google Cloud console.  
Make sure you have an active project with an active billing account. Create a new project if you don’t already have one. 
Also if you are reading this and would like to get hold of some credits to help you get started with Google Cloud and to use ADK, use this link to redeem credits. You can follow the instructions here to redeem it. Please note that this link is valid only till the end of May for redemption.
Activate Cloud Shell by clicking this link. You can toggle between Cloud Shell Terminal (for running cloud commands) and Editor (for building projects) by clicking on the corresponding button from Cloud Shell.
Make sure to have Python 3.9+


### Set up Environment & Install ADK
#### Create & Activate Virtual Environment (Recommended)
From your Cloud Shell Terminal, create a Virtual Environment: 
python -m venv .venv

#### Activate the Virtual Environment:
source .venv/bin/activate

#### Install ADK:
pip install google-adk

#### From Cloud Shell Terminal, create a directory in your desired project location:
mkdir renovation-agent

#### Go to Cloud Shell editor and create the following project structure by creating the files (empty to begin with):
renovation-agent/
        __init__.py
        agent.py
        .env
#### Go to __init__.py and update with the following content:
from . import agent

#### Go to agent.py and update the file with content from the following location:
Refer agent.py in this repo
Comment out the sub agent "ordering_agent" if you do not want to create a Cloud Run Function for getting order status from AlloyDB.

##### But if you want to try the Ordering Agent, steps are as follows:

###### Create AlloyDB cluster and instance, table and data
To create cluster and instance, follow the step mentioned in STEP 4. Database Setup: https://codelabs.developers.google.com/smart-stylist-app#3
To create table and insert data, run the sql statements from here: https://github.com/AbiramiSukumaran/adk-renovation-agent/blob/main/database_script.sql

###### Create a Cloud Run Function in Java to extract order status information
Create Cloud Run Function from here: https://console.cloud.google.com/run/create?deploymentType=function
Set the name of the function to "**check-order-status**" and choose the "**Java 17**" as runtime. 
You can set authentication to "Allow unauthenticated invocations" since it is a demo application.
Follow steps in the link below to make sure your Cloud Run Function can talk to your AlloyDB data and retrieve:
        _Go to "Create the Cloud Run Function" section in step 9 of the codelab [https://codelabs.developers.google.com/smart-shop-agent-alloydb#9](https://codelabs.developers.google.com/smart-stylist-app#9) link._
        _Follow all instructions from points 4 to 15 in that section._
Click "Create".

###### Once the function is created and placeholder code loaded:
Change the name of the Java file to "ProposalOrdersTool.java" and the class name to "ProposalOrdersTool". 
Replace the placeholder code in ProposalOrdersTool.java & pom.xml with code from the respective files in the folder "Cloud Run Function" in this repo. 
In line 73 of ProposalOrdersTool.java that contains the following code, replace the placeholder values with values from your configuration:
        _String ALLOYDB_INSTANCE_NAME = "projects/<<YOUR_PROJECT_ID>>/locations/us-central1/clusters/<<YOUR_CLUSTER>>/instances/<<YOUR_INSTANCE>>";_

Deploy the function and test it.

#### Set up .env variables
Set up your values for the parameters in the template .env file in this repo

#### Make sure you have the Cloud Storage Bucket
This is to store the proposal document that the agent generates.
Create it and provide access so the multiagent system created with Vertex AI can access it.
Here is how you can do it: https://cloud.google.com/storage/docs/creating-buckets#console

### Execute
You can run the following to test it in the terminal:
adk run .

You can run the following to test it in an ADK provisioned UI:
adk web

