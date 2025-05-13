import os
from google.adk.agents import Agent
from google.adk.tools import ToolContext
from google.adk.agents.callback_context import CallbackContext
from google.genai import types
from google.adk.artifacts import InMemoryArtifactService
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
import warnings
from typing import Any, Dict, List, Optional
import typing
from google.adk.sessions import Session
from google.adk.events import Event
import random
import vertexai
from vertexai.preview.reasoning_engines import AdkApp
from google.cloud import storage
from google.genai.types import Blob
from google.genai.types import Part
import logging
import base64
import mimetypes
import asyncio
import pdfplumber
import requests
import io
import json
# Load environment variables from .env file
from dotenv import load_dotenv
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from vertexai import agent_engines
load_dotenv()

warnings.filterwarnings("ignore")
GOOGLE_API_KEY = os.environ["GOOGLE_API_KEY"]
STORAGE_BUCKET = os.environ["STORAGE_BUCKET"]
GOOGLE_CLOUD_PROJECT = os.environ["GOOGLE_CLOUD_PROJECT"]
GOOGLE_CLOUD_LOCATION = os.environ["GOOGLE_CLOUD_LOCATION"]
GOOGLE_GENAI_USE_VERTEXAI=os.environ["GOOGLE_GENAI_USE_VERTEXAI"]
CHECK_ORDER_STATUS_ENDPOINT = os.environ["CHECK_ORDER_STATUS_ENDPOINT"]
STAGING_BUCKET = "gs://" + STORAGE_BUCKET
ROOT_AGENT_NAME = "adk_renovation_agent"
PROJECT_ID = GOOGLE_CLOUD_PROJECT
staging_bucket = STAGING_BUCKET
logger = logging.getLogger(__name__)

USER_ID = "user123"
SESSION_ID = "demo"
PROPOSAL_DOCUMENT_FILE_NAME =  "proposal_document_for_user.pdf"
MODEL_NAME = "gemini-2.5-pro-preview-03-25"
from fastapi import HTTPException


'''
Tools Definition Starts:
get_ordering_data
check_status
send_email
get_permits_compliance_codes
get_contract_from_gcs
store_pdf
get_suppliers_data
get_ordering_data
'''

def get_ordering_data(tool_context: ToolContext) -> str:
    '''
    # Make sure the tool context is not empty for contract content 
    # and other details are nonempty
    # Get materials, order and ordering information
    # Set ordering information to  the tool's context
    '''
    if not tool_context.state['contract_text'] :
        return
    order_data = (
        "Here is the supplier list for the contract detailed here : "
        + tool_context.state['contract_text']
        + ": \n"
        + get_suppliers_data()
    )

    tool_context.state['ordering_data'] = order_data
    return order_data




# check status
def check_status(tool_context: ToolContext) -> list:
    if not tool_context :
        return []
    # Invoke a cloud run functions endpoint here for checking the material and status of order:
    endpoint = CHECK_ORDER_STATUS_ENDPOINT
    try:
        response = requests.get(endpoint)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        status_list = response.json()  # Parse the JSON response into a list
        return status_list
    except requests.exceptions.RequestException as e:
        print(f"Error fetching status: {e}")
        return [] # Return an empty list in case of an error
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON response: {e}")
        return []




# Send email
def send_email() -> str:
    email_template =   """
    Subject: Permit and Compliance Checklist for Kitchen Renovation at 123 Main Street, Anytown, CA 91234

    Dear Authorities,

    Please find below a checklist of required permits and compliance codes for the kitchen renovation project at 123 Main Street, Anytown, CA 91234:

    Permits Required:
    - Electrical Permit
    - Plumbing Permit
    - Building Permit

    Compliance Codes:
    - CBC 2022
    - NEC 2023
    - CPC 2022

    Please let us know if you require any further information.

    Sincerely,
    [Your Name/Company Name]
    """
    return email_template



# Get permits and compliance information
def get_permits_compliance_codes() -> str:
    permits_compliance_data = """
        Contextual Notes:

        Location: Anytown, CA (California) is the location to focus on for permits and compliance.
        Project Type: Kitchen Remodel
        Key Contractor: Bob's Renovations, Inc.
        Key Dates: Contract Date May 16th, 2025; Start Date: May 22nd, 2025; Completion Estimate: ~6 weeks.

        Local Permits and Guides:

        This would contain general information about living in Anytown, CA. While not directly related to the contract, it can provide context for certain permit requirements or common practices.

        Title: Welcome to Anytown, California: A Guide for Residents
        Description: A comprehensive guide to living in Anytown, CA, covering local services, schools, recreation, and community events.
        Content:
        Anytown is a vibrant city in California known for its family-friendly atmosphere and strong sense of community. The city offers a range of amenities, including parks, libraries, and community centers. The local economy is driven by technology, healthcare, and education. Residents enjoy a mild climate, access to nearby attractions, and a variety of cultural events throughout the year.


        Title: Kitchen Remodel Permits and Compliance in Anytown, CA
        Description: Information on permits and compliance requirements for kitchen remodeling projects in Anytown, California.
        Content:
        For kitchen remodeling projects in Anytown, CA, the following permits are typically required:

        Building Permit:  Required for structural changes, electrical work, and plumbing modifications. In this specific contract, the following work is covered under building permit as it needs modifications and alterations: Plumbing work necessary for sink and dishwasher connections, Electrical work necessary for lighting and appliance connections (GFCI outlets).
            Reference: Anytown Municipal Code, Section 101.
        Electrical Permit: Necessary if you are altering or adding electrical circuits or outlets.  Crucial since the contract specifies: "Electrical work necessary for lighting and appliance connections (GFCI outlets).
            Reference: California Electrical Code, Article 210.
        Plumbing Permit: Required for any changes to water supply or drain lines.  The contract includes: "Plumbing work necessary for sink and dishwasher connections."
            Reference: California Plumbing Code, Section 401.
        Mechanical Permit: May be needed if you're altering ventilation systems.  Potentially applicable if range hood installation affects existing ductwork. Not apparent in the contract, but worth checking.
            Reference: California Mechanical Code, Section 301.

        California Building Codes:

        California Building Code (CBC):  Governs the structural safety of buildings.  Ensure all structural work adheres to CBC standards.
            Reference: California Building Standards Code, Title 24.
        California Electrical Code (CEC): Sets standards for safe electrical installations, including GFCI outlet requirements.
        California Plumbing Code (CPC):  Specifies requirements for plumbing systems, including water supply and drainage.
        California Green Building Standards Code (CALGreen): Promotes sustainable building practices, including water and energy conservation.



        Compliance:

        1.  Verify contractor's license (Bob's Renovations, Inc., License #1234567).
        2.  Confirm liability and worker's compensation insurance.
        3.  Ensure GFCI outlets are installed per CEC requirements.
        4.  Plumbing connections meet CPC standards.
        5.  Structural work complies with CBC.

    """
    return permits_compliance_data


# Get pdf file from Google Cloud Storage and extract content  that is multimodal in nature
def get_contract_from_gcs(contract_file_name: str, tool_context: ToolContext) -> str:
   """Downloads a file from GCS and stores it in an artifact."""
   storage_client = storage.Client()
   bucket = storage_client.bucket(STORAGE_BUCKET)
   blob = bucket.blob(contract_file_name)
   pdf_text = ""


   try:
       if not blob.exists():
           raise FileNotFoundError(
               f"File not found in GCS: gs://{STORAGE_BUCKET}/{contract_file_name}"
           )


       logger.info(f"Attempting to access GCS path: gs://{STORAGE_BUCKET}/{contract_file_name}")


       file_bytes = base64.b64encode(blob.download_as_bytes())
       mime_type = mimetypes.guess_type(contract_file_name)[0]


       pdf_artifact = Part(inline_data=Blob(data=file_bytes, mime_type=mime_type))


       with io.BytesIO(base64.b64decode(pdf_artifact.inline_data.data)) as pdf_file_obj:
           with pdfplumber.open(pdf_file_obj) as pdf:
               for page in pdf.pages:
                   pdf_text += page.extract_text()
       logger.info(
       "Processed pdf %s from GCS [bucket=%s] to artifact %s",
       contract_file_name,
       STORAGE_BUCKET,
       pdf_text,
   )
   except FileNotFoundError as e:
       logger.error(str(e))
       raise
   except pdfplumber.pdf.PDFSyntaxError as e:
       logger.error(
           "Failed to process pdf %s from GCS [bucket=%s]: PDF Syntax Error %s",
           contract_file_name,
           STORAGE_BUCKET,
           e,
       )
       raise
   except Exception as e:
       logger.error(
           "Failed to process pdf %s from GCS [bucket=%s]: %s",
           contract_file_name,
           STORAGE_BUCKET,
           e,
       )
       raise
   tool_context.state['contract_text'] = pdf_text
   return pdf_text

def store_pdf(pdf_text: str) -> str:
    """Writes text to a PDF file, then uploads it to Google Cloud Storage.
    Args:
        text: The text to write to the PDF.
        bucket_name: The name of the GCS bucket.
        file_name: The name to give the PDF file in the bucket.
    """
    try:
        # Use reportlab to create a PDF from the text, as pdfplumber is better for reading PDFs

        pdf_buffer = io.BytesIO()
        c = canvas.Canvas(pdf_buffer, pagesize=letter)
        textobject = c.beginText()
        textobject.setTextOrigin(10, 730)  # Adjust coordinates as needed
        textobject.setFont("Helvetica", 12)

        # Add the text, line by line, to the PDF
        for line in pdf_text.splitlines():
            textobject.textLine(line)

        c.drawText(textobject)
        c.save()

        pdf_buffer.seek(0)  # Reset buffer to start

        # Upload the PDF to GCS
        storage_client = storage.Client()
        bucket = storage_client.bucket(STORAGE_BUCKET)
        blob = bucket.blob(PROPOSAL_DOCUMENT_FILE_NAME)

        blob.upload_from_file(pdf_buffer, content_type="application/pdf")

        logger.info(f"Successfully uploaded PDF to gs://{STORAGE_BUCKET}/{PROPOSAL_DOCUMENT_FILE_NAME}")

    except Exception as e:
        logger.error(f"Error writing text to PDF and uploading: {e}")
        raise
    finally:
        if 'pdf_buffer' in locals():
            pdf_buffer.close() #Close the buffer
    return "Successfully uploaded PDF to GCS!!"

def get_suppliers_data() -> str:
    ordering_data =  """
    Description:  A list of suppliers and corresponding materials in and around Anytown, CA, specializing in kitchen remodeling materials.
    Content:
    *   Anytown Building Supply: 123 Oak St, Anytown, CA 91235. Specializes in lumber, drywall, and general construction materials. Phone: 555-1212.

    *   California Kitchen & Bath: 456 Main St, Anytown, CA 91234. Focuses on cabinets, countertops, sinks, and faucets.  Showroom available. Phone: 555-3434.

    *   Lowe's Home Improvement: (Nearby Location, e.g., 789 Elm St, Neighboring City, CA). Offers a wide variety of building materials, appliances, and fixtures. Phone: 555-5656.  Website: lowes.com

    *   The Home Depot: (Nearby Location, e.g., 901 Pine Ave, Neighboring City, CA). Similar to Lowe's. Phone: 555-7878. Website: homedepot.com
    *   Granite & Quartz Direct: Specializes in countertops.
    *   ABC Lighting: Lighting Specialists

    Look them in Google for respective product prices.

    """
    return ordering_data



def get_ordering_data(tool_context: ToolContext) -> str:
    '''
    # Make sure the tool context is not empty for contract content 
    # and other details are nonempty
    # Get materials, order and ordering information
    # Set ordering information to  the tool's context
    '''
    if not tool_context.state['contract_text'] :
        return
    order_data = (
        "Here is the supplier list for the contract detailed here : "
        + tool_context.state['contract_text']
        + ": \n"
        + get_suppliers_data()
    )

    tool_context.state['ordering_data'] = order_data
    return order_data



'''
Tools Definition Ends
'''

sample_proposal = """
*****************************Sample Proposal Document Template***********
PROPOSAL DOCUMENT 
This proposal is made and entered into this 16th day of March, 2025, by and between:
Homeowner: Alice Smith, residing at 123 Main Street, Anytown, CA 91234
Contractor: Bob's Renovations, Inc., a California corporation, with its principal place of
business at 456 Oak Avenue, Anytown, CA 91235 (License #1234567)
1. Scope of Work:
Contractor agrees to perform the following work:
Kitchen Remodel
Demolition of existing kitchen cabinets, countertops, and flooring.
Installation of new custom cabinets (specified in Exhibit A – Cabinet Design).
Installation of granite countertops (specified in Exhibit B – Countertop Selection).
Installation of tile backsplash (specified in Exhibit C – Backsplash Tile).
Installation of new stainless steel sink and faucet.
Installation of new recessed lighting (6 fixtures).
Installation of new flooring (specified in Exhibit D – Flooring Selection).
Painting of walls and ceiling (2 coats, color specified in Exhibit E – Paint Color).
Plumbing work necessary for sink and dishwasher connections.
Electrical work necessary for lighting and appliance connections (GFCI outlets).
All work will be performed in a professional and workmanlike manner in accordance with local
building codes.
2. Proposal Price:
The total contract price for the work described above is $30,000.00 (Thirty Thousand Dollars).
3. Payment Schedule:
Deposit: $10,000.00 due upon signing of this proposal.

Phase 1 (Demolition & Rough-in): $5,000.00 due upon completion of demolition and
rough-in plumbing and electrical.
Phase 2 (Cabinet & Countertop Installation): $10,000.00 due upon completion of cabinet
and countertop installation.
Final Payment: $5,000.00 due upon final inspection and completion of all work.
4. Change Orders:
Any changes to the scope of work must be agreed upon in writing and signed by both parties.
Changes may result in adjustments to the contract price and schedule. 
5. Timeline:
The work shall commence on May 22, 2025, and be substantially completed within 6 weeks.
This timeline is subject to change due to unforeseen circumstances (e.g., material delays,
weather).

6. Permits:
Contractor is responsible for obtaining all necessary permits for the work.
7. Insurance:
Contractor shall maintain general liability insurance and workers' compensation insurance. Proof
of insurance will be provided upon request.
8. Warranty:
Contractor warrants all labor for a period of one (1) year from the date of completion.
Manufacturer warranties apply to materials.
9. Dispute Resolution:
Any disputes arising out of this contract shall be resolved through mediation. If mediation fails,
the parties agree to binding arbitration.
10. Termination:
This proposal may be terminated by either party with written notice if the other party breaches
the proposal.
11. Entire Agreement:
This proposal constitutes the entire agreement between the parties and supersedes all prior
discussions and agreements.
IN WITNESS WHEREOF, the parties have executed this contract as of the date first written
above.

____________Alice Smith________________
Alice Smith (Homeowner)
_____________Bob_______________
Bob Johnson (Contractor, Bob's Renovations, Inc.)
Exhibits:
Exhibit A: Cabinet Design (detailed drawings, specifications)

Image of the design goes here.

I. Overall Style and Design
Style: Modern, European-style, minimalist.
Layout: Wall cabinets, base cabinets, and a tall pantry-style cabinet. An island is visible but not
fully detailed in the image.
Color Palette: Primarily white cabinets with a dark countertop. Walls are a neutral grey/beige.
II. Cabinet Construction Specifications
Cabinet Type: Frameless (European-style). This means the doors and drawers attach directly to
the cabinet boxes, without a face frame.
Box Material: Likely constructed from particleboard or MDF (Medium-Density Fiberboard). The
interior finish is not visible.
Door and Drawer Front Material: High-gloss white finish. Likely acrylic, laminate, or a high-gloss
lacquer applied to an MDF core.
Edge Banding: Color-matched to the door/drawer front, likely a thin PVC or ABS edge banding.
Hardware:
Pulls: Long, horizontal, stainless steel or brushed nickel finish pulls. Appear to be mounted on
the center of the drawers and doors.
Hinges: Concealed, European-style hinges (soft-close likely).
Drawer Slides: Full-extension, soft-close drawer slides.
Toe Kick: Recessed, likely white to match cabinets.
III. Cabinet Dimensions (Estimated).

Wall Cabinet Height: Appears to be close to ceiling height, perhaps 30-36" high depending on
ceiling height.
Wall Cabinet Depth: Standard depth, likely 12-14".
Base Cabinet Height: Standard counter height, approximately 36" including countertop.
Base Cabinet Depth: Standard depth, approximately 24".
Pantry Cabinet Height: Floor to ceiling.
Pantry Cabinet Depth: Likely 24".
IV. Cabinet Breakdown
Wall Cabinets:
Several cabinets above the countertop, configured to fit the available space.
The cabinet directly above the cooktop is likely shallower to accommodate the range hood.
Under-cabinet lighting is present (LED strip lights).
Base Cabinets:
One cabinet to the left of the tall cabinet.
Multiple drawers, including one directly under the cooktop.
A cabinet at the very end of the counter next to the right wall.
Tall Cabinet:
Full-height pantry-style cabinet.
Two doors, one above the other.
Island:
Dark countertop matching the perimeter countertops.
Cabinets on the visible side are white.

V. Countertop Specifications
Material: Dark solid surface or stone countertop. Could be quartz, granite, or a similar
engineered stone.
Edge Profile: Slightly eased edge, possibly a small radius.
Thickness: Likely 1 1/4" (3cm).
VI. Appliance Considerations
Cooktop: Integrated, flat, black cooktop (likely induction or electric).
Range Hood: Stainless steel, integrated into the wall cabinets.
Outlets: Outlets are present on the back splash.
VII. Additional Details
Backsplash: Rectangular tile with a horizontal orientation, likely ceramic or glass, in a light color
with some variation.
Lighting: Recessed ceiling lights and under-cabinet lighting.
   *************************************************************************

   """

root_agent_system_instruction = """
    You are a proposal , permits and ordering agent for executing and managing the kitchen renovation proposal for a home owner. 
    You are tasked with:

    1. Creating Proposal Document if the user doesn't have one already.
    2. Creating permits and compliance documentation.
    3. Creating a material list for ordering along with quality control checklists.
    4. Placing orders and tracking the status of materials delivery.

    Here's how you should operate:

    - First, greet the user and ask them what they need help with. Provide a brief overview of your capabilities.
    - Clarify the user's intent. If the user is unclear, ask clarifying questions.
    - The user will ask you to create a proposal document or will directly provide the proposal document. 
    - If the user provides the proposal document, using the corresponding subagent you will be able to extract the doc and its content.
    - If the user asks you to create a proposal document then you need to go to the corresponding sub-agent to create proposal document.
    - Based on the user's intent, determine which sub-agent is best suited to handle the request.
    - Then follow the instructions below. Ultimately your goal is to route the user's request to the appropriate sub-agent and 
      ensure that the task is completed successfully.
    """



'''
Defining children agents permits_agent and ordering_agent 
followed by the orchestration agent root_agent that 
controls the flow with instructions, tools, 
children agents and the context state.
'''


'''
# Proposal Agent Definition
'''
proposal_agent = Agent(
   model=MODEL_NAME,
   name="proposal_agent",
   description="Agent that creates the kitchen renovation proposal pdf for the customer based on a few details that the user provides about the renovation request.",
   instruction= f"""
   You are a home renovation proposal document  generator agent that helps with creating 
   the renovation proposal document with the following details from the user:
   1) the necessary renovation requirement from the user
   2) preference for contractor location (optional)
   3) budget constraints (optional)
   Do not ask any other questions to the user. Use the infomration in the template for filling details taht you don't know.
   After clarifiying the user's intent on the options, generate the PDF file content for the renovation proposal. 
   Then upload the content as a pdf file in a Cloud Storage Bucket using the tool "store_pdf"  
   Once the proposal document pdf content is created and uploaded in the Cloud Storage Bucket,
   confirm to the user that the proposal document has been created and uploaded to the Cloud Storage Bucket defined.
   Here is a sample content for the proposal document, use this as a reference and create the one 
   that matches the user requirements : {sample_proposal}
   """,
   generate_content_config=types.GenerateContentConfig(temperature=0.2),
   tools=[store_pdf],
)

'''
# Permits Agent Definition
'''
permits_agent = Agent(
   model=MODEL_NAME,
   name="permits_agent",
   description="Agent that reads the home renovation contract for the customer details and helps create the validation of whether the necessary permits are obtained and compliances are met",
   instruction="""
   You are a Contract Permits and Compliance Agent for validating the home renovation contracts to
   confirm and help the contractor with
   1) the necessary permits to be obtained and
   2) local building compliance checks to be met.
   3) Creating email content to respective authorities for permits.
   
   After clarifiying the user's intent on the options, get the file name of the contract. 
   If the user asked you to create a proposal document in the previous step,
    you already have the file name which is "proposal_document_for_user.pdf". 
   If the user has the proposal document created on their own, ask them to provide the file name 
   for the proposal document file from their Cloud Storage bucket.
   The tool get_contract_from_gcs is capable of processing the path to it on its own.
   
   Based on the information in the proposal document about the locality of the construction,
   and information from the tool: get_permits_compliance_codes, extract the information and 
   create a checklist with all important permits and compliance codes and guidelines.
   Additionally when a user asks you specific questions, you must be able to answer with truth from the contract document.
   Share your response in the checklist format with green tick mark icons for each checklist item.
   
   If the user asks you to send an email to respective authorities, use the sample email template in the tool send_email as a reference only, to draft the body which can be sent to the respective authorities for approval.
   If for some reason this fails, please inform the user and let them know you can't extract the contract.""",
   generate_content_config=types.GenerateContentConfig(temperature=0.2),
   tools=[
       get_contract_from_gcs,
       get_permits_compliance_codes,
       send_email
   ],
)



'''
# Ordering Agent Definition
'''
ordering_agent = Agent(
   model=MODEL_NAME,
   name="ordering_agent",
   description="Agent that understands the home renovation contract and creates material order checklist, quality control specification for materials and delivery order",
   instruction="""
   You are an ordering agent for a construction contractor company. You can ask the document name from the user.
   The tool get_contract_from_gcs is capable of extracting the file and its content on its own.
   1. Based on the user preferences and the contract document, and using the tool get_ordering_data you will generate the list of materials needed for the project.
   along with the quality control specification checklist for each material in the list.
   2. You will be able to trigger the order submission to suppliers - for this generate the list of materials, quality checks, 
   quantity required in a list format along with the supplier details in the header of the list.
   3. You will also be able to check the status of delivery of the material supply using the tool check_status.
   If for some reason this fails, please inform the user and let them know you can't extract or save the contractor review information.
   """,
   generate_content_config=types.GenerateContentConfig(temperature=0.2),
   tools=[
       get_contract_from_gcs,
       get_ordering_data,
       check_status
   ],
)



'''
# Root Agent Definition
'''
root_agent = Agent(
   model=MODEL_NAME,
   name=ROOT_AGENT_NAME,
   description=("Agent that manages and executes the building renovation proposal for a home owner."),

# Instructions for intent detection: Combine guardrails string
# and the sub-agent routing instruction

   instruction=(
   f""" {root_agent_system_instruction} 
    **********************************************************************************************************
    **********************************************************************************************************
    - If the user asks you to create a proposal document 
      invoke the proposal_agent
    - If the user wants to create a checklist of permits or 
    compliance documentation, invoke the permits_agent.
    - If the user wants to execute ordering of materials,
    place order or get the status of delivery, 
    invoke the ordering_agent without asking more questions.
    **********************************************************************************************************
    **********************************************************************************************************
   """),

    generate_content_config=types.GenerateContentConfig(temperature=0.2),

    # Orchestrating sub agents
    sub_agents=[
        proposal_agent,
        permits_agent,
        ordering_agent
    ],
)


'''
# Agent Engine Deployment:
# Create a remote app for our multiagent with agent Engine.
# This may take 1-2 minutes to finish.
# Uncomment the below segment when you're ready to deploy it to Agent Engine

app = AdkApp(
    agent=root_agent,
    enable_tracing=True,
)

vertexai.init(
    project=PROJECT_ID,
    location=GOOGLE_CLOUD_LOCATION,
    staging_bucket=STAGING_BUCKET,
)

remote_app = agent_engines.create(
    app,
    requirements=[
        "google-cloud-aiplatform[agent_engines,adk]>=1.88",
        "google-adk",
        "pysqlite3-binary",
        "toolbox-langchain==0.1.0",
        "pdfplumber",
        "google-cloud-aiplatform",
        "cloudpickle==3.1.1",
        "pydantic==2.10.6",
        "pytest",
        "overrides",
        "scikit-learn",
        "reportlab",
        "google-auth",
        "google-cloud-storage",
    ],
)

# Deployment to Agent Engine related code ends

# Example response:
# ...
# To use this deployed ReasoningEngine in another session:
# reasoning_engine = vertexai.preview.reasoning_engines.
# ReasoningEngine('projects/123456789/locations/us-central1/reasoningEngines/123456')

agent_engine = vertexai.agent_engines.get('projects/233708879341/locations/us-central1/reasoningEngines/4232125808426090496')
'''
