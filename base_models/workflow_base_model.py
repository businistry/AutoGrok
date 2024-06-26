# workflow_base_model

import os
import yaml

from base_models.agent_base_model import AgentBaseModel
from configs.config import DEBUG
from datetime import datetime
from typing import List, Dict, Optional


class Sender:
    def __init__(
        self,
        type: str,
        config: Dict,
        timestamp: str,
        user_id: str,
        tools: List[Dict],
    ):
        self.type = type
        self.config = config
        self.timestamp = timestamp
        self.user_id = user_id
        self.tools = tools

    def to_dict(self):
        return {
            "type": self.type,
            "config": self.config,
            "timestamp": self.timestamp,
            "user_id": self.user_id,
            "tools": self.tools,
        }

    @classmethod
    def from_dict(cls, data: Dict):
        return cls(
            type=data["type"],
            config=data["config"],
            timestamp=data["timestamp"],
            user_id=data["user_id"],
            tools=data["tools"],
        )
    

class Receiver:
    def __init__(
        self,
        type: str,
        config: Dict,
        groupchat_config: Dict,
        timestamp: str,
        user_id: str,
        tools: List[Dict],
        agents: List[AgentBaseModel],
    ):
        self.type = type
        self.config = config
        self.groupchat_config = groupchat_config
        self.timestamp = timestamp
        self.user_id = user_id
        self.tools = tools
        self.agents = agents

    def to_dict(self):
        return {
            "type": self.type,
            "config": self.config,
            "groupchat_config": self.groupchat_config,
            "timestamp": self.timestamp,
            "user_id": self.user_id,
            "tools": self.tools,
            "agents": [agent.to_dict() for agent in self.agents],
        }

    @classmethod
    def from_dict(cls, data: Dict):
        return cls(
            type=data["type"],
            config=data["config"],
            groupchat_config=data["groupchat_config"],
            timestamp=data["timestamp"],
            user_id=data["user_id"],
            tools=data["tools"],
            agents=[AgentBaseModel.from_dict(agent) for agent in data.get("agents", [])],
        )

class WorkflowBaseModel:
    def __init__(
        self,
        name: str,
        description: str,
        agents: List[AgentBaseModel],
        sender: Sender,
        receiver: Receiver,
        type: str,
        user_id: str,
        timestamp: str,
        summary_method: str,
        settings: Dict = None,
        groupchat_config: Dict = None,
        id: Optional[int] = None,
        created_at: Optional[str] = None,
        updated_at: Optional[str] = None,
    ):
        self.id = id
        self.name = name
        self.description = description
        self.agents = agents
        self.sender = sender
        self.receiver = receiver
        self.type = type
        self.user_id = user_id
        self.timestamp = timestamp
        self.summary_method = summary_method
        self.settings = settings or {}
        self.groupchat_config = groupchat_config or {}
        self.created_at = created_at or datetime.now().isoformat()
        self.updated_at = updated_at

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "agents": [agent.to_dict() for agent in self.agents],
            "sender": self.sender.to_dict(),
            "receiver": self.receiver.to_dict(),
            "type": self.type,
            "user_id": self.user_id,
            "timestamp": self.timestamp,
            "summary_method": self.summary_method,
            "settings": self.settings,
            "groupchat_config": self.groupchat_config,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @classmethod
    def create_workflow(cls, workflow_name: str) -> "WorkflowBaseModel":
        if DEBUG:
            print(f"Creating workflow {workflow_name}")
        workflow = cls(
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
                        "content": "...",  # Omitted for brevity
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
                    "system_message": "...",  # Omitted for brevity
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
                        "content": "...",  # Omitted for brevity
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

        # Create a YAML file for the workflow with the default values
        workflow_data = workflow.to_dict()
        with open(f"workflows/{workflow_name}.yaml", "w") as file:
            yaml.dump(workflow_data, file)

        return workflow
    
    @classmethod
    def from_dict(cls, data: Dict):
        sender = Sender.from_dict(data["sender"])
        receiver = Receiver.from_dict(data["receiver"])
        return cls(
            id=data.get("id"),
            name=data["name"],
            description=data["description"],
            agents=[AgentBaseModel.from_dict(agent) for agent in data.get("agents", [])],
            sender=sender,
            receiver=receiver,
            type=data["type"],
            user_id=data["user_id"],
            timestamp=data["timestamp"],
            summary_method=data["summary_method"],
            settings=data.get("settings", {}),
            groupchat_config=data.get("groupchat_config", {}),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
        )
    

    @classmethod
    def get_workflow(cls, workflow_name: str) -> "WorkflowBaseModel":
        if DEBUG:
            print(f"Loading workflow: {workflow_name}")
        file_path = f"workflows/{workflow_name}.yaml"
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                workflow_data = yaml.safe_load(file)
                return cls.from_dict(workflow_data)
        else:
            raise FileNotFoundError(f"Workflow file not found: {file_path}")
    

    @staticmethod
    def load_workflows() -> List[str]:
        if DEBUG:
            print("Loading workflows")
        project_names = []
        for file in os.listdir("workflows"):
            if file.endswith(".yaml"):
                project_name = file[:-5]  # Remove the ".yaml" extension
                project_names.append(project_name)
        return project_names