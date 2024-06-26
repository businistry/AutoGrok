# event_handlers_workflow.py

import os
import streamlit as st
import yaml

from datetime import datetime
from base_models.workflow_base_model import WorkflowBaseModel, Sender, Receiver
from configs.config_local import DEBUG
from event_handlers.event_handlers_shared import update_project


def handle_workflow_close():
    if DEBUG:
        print("called handle_workflow_close()")
    st.session_state.current_workflow = None
    st.session_state.workflow_dropdown = "Select..."
    st.rerun()


def handle_workflow_delete(workflow_file):
    if DEBUG:
        print(f"called handle_workflow_delete({workflow_file})")
    os.remove(workflow_file)
    st.session_state.current_workflow = None
    st.session_state.workflow_dropdown = "Select..."
    st.success(f"Workflow '{workflow_file}' has been deleted.")


def handle_workflow_description_change():
    if DEBUG:
        print("called handle_workflow_description_change()")
    new_workflow_description = st.session_state.workflow_description.strip()
    if new_workflow_description:
        st.session_state.current_workflow.description = new_workflow_description
        update_workflow()


def handle_workflow_name_change():
    if DEBUG:
        print("called handle_workflow_name_change()")
    new_workflow_name = st.session_state.workflow_name_edit.strip()
    if new_workflow_name:
        old_workflow_name = st.session_state.current_workflow.name
        st.session_state.current_workflow.name = new_workflow_name
        update_workflow()
        
        # Update the workflow name in current_project.workflows
        if st.session_state.current_project and old_workflow_name in st.session_state.current_project.workflows:
            index = st.session_state.current_project.workflows.index(old_workflow_name)
            st.session_state.current_project.workflows[index] = new_workflow_name
            update_project()


def handle_workflow_selection():
    if DEBUG:
        print("called handle_workflow_selection()")
    selected_workflow = st.session_state.workflow_dropdown
    if selected_workflow == "Select...":
        return
    if selected_workflow == "Create...":
        workflow_name = st.session_state.workflow_name_input.strip()
        if workflow_name:
            workflow = WorkflowBaseModel(
                name=workflow_name,
                description="This workflow is used for general purpose tasks.",
                agents=[],
                sender=Sender(
                    type="userproxy",
                    config={
                        "name": "userproxy",
                        "llm_config": {
                            "config_list": [
                                {
                                    "user_id": "default",
                                    "timestamp": "2024-03-28T06:34:40.214593",
                                    "model": "gpt-4o",
                                    "base_url": None,
                                    "api_type": None,
                                    "api_version": None,
                                    "description": "OpenAI model configuration"
                                }
                            ],
                            "temperature": 0.1,
                            "cache_seed": None,
                            "timeout": None,
                            "max_tokens": None,
                            "extra_body": None
                        },
                        "human_input_mode": "NEVER",
                        "max_consecutive_auto_reply": 30,
                        "system_message": "You are a helpful assistant.",
                        "is_termination_msg": None,
                        "code_execution_config": {
                            "work_dir": None,
                            "use_docker": False
                        },
                        "default_auto_reply": "TERMINATE",
                        "description": "A user proxy agent that executes code."
                    },
                    timestamp="2024-03-28T06:34:40.214593",
                    user_id="user",
                    tools=[
                        {
                            "title": "fetch_web_content",
                            "content": "from typing import Optional\nimport requests\nimport collections\ncollections.Callable = collections.abc.Callable\nfrom bs4 import BeautifulSoup\n\ndef fetch_web_content(url: str) -> Optional[str]:\n    \"\"\"\n    Fetches the text content from a website.\n\n    Args:\n        url (str): The URL of the website.\n\n    Returns:\n        Optional[str]: The content of the website.\n    \"\"\"\n    try:\n        # Send a GET request to the URL\n        response = requests.get(url)\n\n        # Check for successful access to the webpage\n        if response.status_code == 200:\n            # Parse the HTML content of the page using BeautifulSoup\n            soup = BeautifulSoup(response.text, \"html.parser\")\n\n            # Extract the content of the <body> tag\n            body_content = soup.body\n\n            if body_content:\n                # Return all the text in the body tag, stripping leading/trailing whitespaces\n                return \" \".join(body_content.get_text(strip=True).split())\n            else:\n                # Return None if the <body> tag is not found\n                return None\n        else:\n            # Return None if the status code isn't 200 (success)\n            return None\n    except requests.RequestException:\n        # Return None if any request-related exception is caught\n        return None",
                            "file_name": "fetch_web_content.json",
                            "description": None,
                            "timestamp": "2024-05-14T08:19:12.425322",
                            "user_id": "default"
                        }
                    ]
                ),
                receiver=Receiver(
                    type="assistant",
                    config={
                        "name": "primary_assistant",
                        "llm_config": {
                            "config_list": [
                                {
                                    "user_id": "default",
                                    "timestamp": "2024-05-14T08:19:12.425322",
                                    "model": "gpt-4o",
                                    "base_url": None,
                                    "api_type": None,
                                    "api_version": None,
                                    "description": "OpenAI model configuration"
                                }
                            ],
                            "temperature": 0.1,
                            "cache_seed": None,
                            "timeout": None,
                            "max_tokens": None,
                            "extra_body": None
                        },
                        "human_input_mode": "NEVER",
                        "max_consecutive_auto_reply": 30,
                        "system_message": "You are a helpful AI assistant. Solve tasks using your coding and language skills. In the following cases, suggest python code (in a python coding block) or shell script (in a sh coding block) for the user to execute. 1. When you need to collect info, use the code to output the info you need, for example, browse or search the web, download/read a file, print the content of a webpage or a file, get the current date/time, check the operating system. After sufficient info is printed and the task is ready to be solved based on your language skill, you can solve the task by yourself. 2. When you need to perform some task with code, use the code to perform the task and output the result. Finish the task smartly. Solve the task step by step if you need to. If a plan is not provided, explain your plan first. Be clear which step uses code, and which step uses your language skill. When using code, you must indicate the script type in the code block. The user cannot provide any other feedback or perform any other action beyond executing the code you suggest. The user can't modify your code. So do not suggest incomplete code which requires users to modify. Don't use a code block if it's not intended to be executed by the user. If you want the user to save the code in a file before executing it, put # filename: <filename> inside the code block as the first line. Don't include multiple code blocks in one response. Do not ask users to copy and paste the result. Instead, use 'print' function for the output when relevant. Check the execution result returned by the user. If the result indicates there is an error, fix the error and output the code again. Suggest the full code instead of partial code or code changes. If the error can't be fixed or if the task is not solved even after the code is executed successfully, analyze the problem, revisit your assumption, collect additional info you need, and think of a different approach to try. When you find an answer, verify the answer carefully. Include verifiable evidence in your response if possible. Reply 'TERMINATE' in the end when everything is done.",
                        "is_termination_msg": None,
                        "code_execution_config": None,
                        "default_auto_reply": "",
                        "description": "A primary assistant agent that writes plans and code to solve tasks. booger"
                    },
                    groupchat_config={},
                    timestamp=datetime.now().isoformat(),
                    user_id="default",
                    tools=[
                        {
                            "title": "fetch_web_content",
                            "content": "from typing import Optional\nimport requests\nimport collections\ncollections.Callable = collections.abc.Callable\nfrom bs4 import BeautifulSoup\n\ndef fetch_web_content(url: str) -> Optional[str]:\n    \"\"\"\n    Fetches the text content from a website.\n\n    Args:\n        url (str): The URL of the website.\n\n    Returns:\n        Optional[str]: The content of the website.\n    \"\"\"\n    try:\n        # Send a GET request to the URL\n        response = requests.get(url)\n\n        # Check for successful access to the webpage\n        if response.status_code == 200:\n            # Parse the HTML content of the page using BeautifulSoup\n            soup = BeautifulSoup(response.text, \"html.parser\")\n\n            # Extract the content of the <body> tag\n            body_content = soup.body\n\n            if body_content:\n                # Return all the text in the body tag, stripping leading/trailing whitespaces\n                return \" \".join(body_content.get_text(strip=True).split())\n            else:\n                # Return None if the <body> tag is not found\n                return None\n        else:\n            # Return None if the status code isn't 200 (success)\n            return None\n    except requests.RequestException:\n        # Return None if any request-related exception is caught\n        return None",
                            "file_name": "fetch_web_content.json",
                            "description": None,
                            "timestamp": "2024-05-14T08:19:12.425322",
                            "user_id": "default"
                        }
                    ],
                    agents=[]
                ),
                type="twoagents",
                user_id="user",
                timestamp=datetime.now().isoformat(),
                summary_method="last"
            )
            st.session_state.current_workflow = workflow
            st.session_state.workflow_dropdown = workflow_name
            WorkflowBaseModel.create_workflow(st.session_state.current_workflow.name)

            # Add the created workflow's name to current_project.workflows
            if st.session_state.current_project:
                st.session_state.current_project.workflows = [workflow_name] + st.session_state.current_project.workflows[1:]
                update_project()
    else:
        print ("Selected workflow: ", selected_workflow)
        workflow = WorkflowBaseModel.get_workflow(selected_workflow)
        st.session_state.current_workflow = workflow

        # Update current_project.workflows to reflect the selected workflow
        if st.session_state.current_project:
            st.session_state.current_project.workflows = [selected_workflow] + [wf for wf in st.session_state.current_project.workflows if wf != selected_workflow]
            update_project()



def handle_workflow_type_change():
    if DEBUG:
        print("called handle_workflow_type_change()")
    new_workflow_type = st.session_state.workflow_type.strip()
    if new_workflow_type:
        st.session_state.current_workflow.type = new_workflow_type
        update_workflow()


def handle_workflow_summary_method_change():
    if DEBUG:
        print("called handle_workflow_summary_method_change()")
    new_workflow_summary_method = st.session_state.workflow_summary_method.strip()
    if new_workflow_summary_method:
        st.session_state.current_workflow.summary_method = new_workflow_summary_method
        update_workflow()


def update_workflow():
    if DEBUG:
        print("called update_workflow()")
    st.session_state.current_workflow.updated_at = datetime.now().isoformat()
    workflow_name = st.session_state.current_workflow.name
    workflow_data = st.session_state.current_workflow.to_dict()
    with open(f"workflows/{workflow_name}.yaml", "w") as file:
        yaml.dump(workflow_data, file)