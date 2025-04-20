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

