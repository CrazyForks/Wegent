#!/usr/bin/env python

# SPDX-FileCopyrightText: 2025 Weibo, Inc.
#
# SPDX-License-Identifier: Apache-2.0

# -*- coding: utf-8 -*-

import os
import json
import subprocess
from typing import Dict, Any, Optional, List
from pathlib import Path

from shared.logger import setup_logger
from shared.status import TaskStatus
from executor.agents.base import Agent

logger = setup_logger("codex_agent")


class CodexAgent(Agent):
    """
    Codex Agent implementation that supports code generation and execution
    using OpenAI's Codex model or similar code-generation capabilities
    """

    def __init__(self, task_data: Dict[str, Any]):
        """
        Initialize the Codex agent

        Args:
            task_data: The task data dictionary containing configuration
        """
        super().__init__(task_data)
        self.codex_config = task_data.get("codex_config", {})
        self.model_name = self.codex_config.get("model_name", "codex")
        self.api_key = self.codex_config.get("api_key", "")
        self.temperature = self.codex_config.get("temperature", 0.3)
        self.max_tokens = self.codex_config.get("max_tokens", 1000)
        self.language = task_data.get("language", "python")
        self.code_requirements = task_data.get("code_requirements", "")

    def get_name(self) -> str:
        """Get the name of the agent"""
        return "CodexAgent"

    def pre_execute(self) -> TaskStatus:
        """
        Pre-execution setup for Codex agent

        Returns:
            TaskStatus: Status of pre-execution
        """
        try:
            logger.info(f"Agent[{self.get_name()}][{self.task_id}] pre_execute: Starting Codex agent setup")

            # Download code if git_url is provided
            self.download_code()

            # Validate Codex configuration
            if not self.api_key:
                logger.warning(f"Agent[{self.get_name()}][{self.task_id}] No API key provided for Codex")

            # Setup working directory
            if self.project_path:
                os.makedirs(self.project_path, exist_ok=True)
                logger.info(f"Agent[{self.get_name()}][{self.task_id}] Working directory: {self.project_path}")

            logger.info(f"Agent[{self.get_name()}][{self.task_id}] pre_execute: Setup completed successfully")
            return TaskStatus.SUCCESS

        except Exception as e:
            error_msg = f"Agent[{self.get_name()}][{self.task_id}] pre_execute failed: {str(e)}"
            logger.error(error_msg)
            return TaskStatus.FAILED

    def execute(self) -> TaskStatus:
        """
        Execute the main task using Codex capabilities

        Returns:
            TaskStatus: Status of execution
        """
        try:
            logger.info(f"Agent[{self.get_name()}][{self.task_id}] execute: Starting Codex execution")

            # Report initial progress
            self.report_progress(10, "generating_code", "Starting code generation with Codex")

            # Generate code based on requirements
            generated_code = self.generate_code()

            if not generated_code:
                logger.error(f"Agent[{self.get_name()}][{self.task_id}] Failed to generate code")
                return TaskStatus.FAILED

            # Report progress after code generation
            self.report_progress(50, "code_generated", "Code generated successfully")

            # Save generated code to file
            code_file_path = self.save_code_to_file(generated_code)

            if not code_file_path:
                logger.error(f"Agent[{self.get_name()}][{self.task_id}] Failed to save code to file")
                return TaskStatus.FAILED

            # Report progress after saving code
            self.report_progress(70, "code_saved", f"Code saved to {code_file_path}")

            # Execute the generated code if possible
            execution_result = self.execute_generated_code(code_file_path)

            # Report final progress
            self.report_progress(100, "completed", "Codex execution completed", {
                "generated_code": generated_code,
                "code_file_path": code_file_path,
                "execution_result": execution_result
            })

            logger.info(f"Agent[{self.get_name()}][{self.task_id}] execute: Codex execution completed successfully")
            return TaskStatus.SUCCESS

        except Exception as e:
            error_msg = f"Agent[{self.get_name()}][{self.task_id}] execute failed: {str(e)}"
            logger.error(error_msg)
            self.report_progress(0, "failed", error_msg)
            return TaskStatus.FAILED

    def generate_code(self) -> Optional[str]:
        """
        Generate code using Codex capabilities

        Returns:
            str: Generated code or None if failed
        """
        try:
            # Create prompt for Codex
            prompt = self.create_codex_prompt()

            logger.info(f"Agent[{self.get_name()}][{self.task_id}] Generating code with prompt: {prompt[:100]}...")

            # For now, simulate Codex API call
            # In a real implementation, this would call OpenAI's Codex API
            generated_code = self.simulate_codex_generation(prompt)

            logger.info(f"Agent[{self.get_name()}][{self.task_id}] Code generated successfully")
            return generated_code

        except Exception as e:
            logger.error(f"Agent[{self.get_name()}][{self.task_id}] Code generation failed: {str(e)}")
            return None

    def create_codex_prompt(self) -> str:
        """
        Create a prompt for Codex based on the requirements

        Returns:
            str: Formatted prompt for Codex
        """
        prompt = f"""
Generate {self.language} code that meets the following requirements:

{self.code_requirements}

Requirements:
- The code must be executable and follow {self.language} syntax rules
- Include proper error handling
- Add comments where necessary
- The code should be well-structured and maintainable

Please provide only the code without any additional explanation:
"""
        return prompt.strip()

    def simulate_codex_generation(self, prompt: str) -> str:
        """
        Simulate Codex code generation (placeholder for actual API call)

        Args:
            prompt: The prompt for code generation

        Returns:
            str: Generated code
        """
        # This is a simulation - in real implementation, this would call Codex API
        if self.language.lower() == "python":
            return f"""
# Generated code for: {self.code_requirements}

def main():
    \"\"\"
    Main function to execute the generated code
    \"\"\"
    try:
        # Implementation based on requirements
        print("Executing generated code...")
        # Add your implementation here
        return True
    except Exception as e:
        print(f"Error executing code: {{e}}")
        return False

if __name__ == "__main__":
    main()
"""
        elif self.language.lower() == "javascript":
            return f"""
// Generated code for: {self.code_requirements}

function main() {
    try {
        console.log("Executing generated code...");
        // Add your implementation here
        return true;
    } catch (error) {
        console.error("Error executing code:", error);
        return false;
    }
}

// Execute the function
main();
"""
        else:
            return f"""
// Generated code for: {self.code_requirements}
// Language: {self.language}

// Add your implementation here based on the requirements
console.log("Executing generated code...");
"""

    def save_code_to_file(self, code: str) -> Optional[str]:
        """
        Save generated code to a file

        Args:
            code: The generated code to save

        Returns:
            str: Path to the saved file or None if failed
        """
        try:
            if not self.project_path:
                self.project_path = os.path.join(os.getcwd(), f"task_{self.task_id}")
                os.makedirs(self.project_path, exist_ok=True)

            # Determine file extension based on language
            extension = self.get_file_extension()
            filename = f"generated_code.{extension}"
            file_path = os.path.join(self.project_path, filename)

            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(code)

            logger.info(f"Agent[{self.get_name()}][{self.task_id}] Code saved to {file_path}")
            return file_path

        except Exception as e:
            logger.error(f"Agent[{self.get_name()}][{self.task_id}] Failed to save code: {str(e)}")
            return None

    def get_file_extension(self) -> str:
        """
        Get file extension based on programming language

        Returns:
            str: File extension
        """
        extensions = {
            "python": "py",
            "javascript": "js",
            "java": "java",
            "c": "c",
            "cpp": "cpp",
            "c++": "cpp",
            "go": "go",
            "rust": "rs",
            "typescript": "ts",
            "html": "html",
            "css": "css",
            "sql": "sql",
            "bash": "sh",
            "shell": "sh"
        }
        return extensions.get(self.language.lower(), "txt")

    def execute_generated_code(self, code_file_path: str) -> Dict[str, Any]:
        """
        Execute the generated code file

        Args:
            code_file_path: Path to the generated code file

        Returns:
            Dict: Execution result
        """
        result = {
            "executed": False,
            "output": "",
            "error": None,
            "exit_code": None
        }

        try:
            if self.language.lower() in ["python", "javascript", "bash", "shell"]:
                # Execute the code
                process = subprocess.run(
                    [self.get_execution_command(), code_file_path],
                    capture_output=True,
                    text=True,
                    timeout=30
                )

                result["executed"] = True
                result["output"] = process.stdout
                result["error"] = process.stderr
                result["exit_code"] = process.returncode

                logger.info(f"Agent[{self.get_name()}][{self.task_id}] Code execution completed with exit code: {process.returncode}")

            else:
                logger.info(f"Agent[{self.get_name()}][{self.task_id}] Code execution not supported for language: {self.language}")
                result["output"] = f"Code execution not supported for language: {self.language}"

        except subprocess.TimeoutExpired:
            error_msg = "Code execution timed out"
            logger.error(f"Agent[{self.get_name()}][{self.task_id}] {error_msg}")
            result["error"] = error_msg

        except Exception as e:
            error_msg = f"Code execution failed: {str(e)}"
            logger.error(f"Agent[{self.get_name()}][{self.task_id}] {error_msg}")
            result["error"] = error_msg

        return result

    def get_execution_command(self) -> str:
        """
        Get the command to execute the generated code

        Returns:
            str: Execution command
        """
        commands = {
            "python": "python3",
            "javascript": "node",
            "bash": "bash",
            "shell": "bash"
        }
        return commands.get(self.language.lower(), "echo")

    def initialize(self) -> TaskStatus:
        """
        Initialize the Codex agent

        Returns:
            TaskStatus: Initialization status
        """
        try:
            logger.info(f"Agent[{self.get_name()}][{self.task_id}] initialize: Initializing Codex agent")

            # Validate required configuration
            if not self.language:
                logger.warning(f"Agent[{self.get_name()}][{self.task_id}] No language specified, using default: python")
                self.language = "python"

            if not self.code_requirements:
                logger.warning(f"Agent[{self.get_name()}][{self.task_id}] No code requirements specified")

            logger.info(f"Agent[{self.get_name()}][{self.task_id}] initialize: Codex agent initialized successfully")
            return TaskStatus.SUCCESS

        except Exception as e:
            error_msg = f"Agent[{self.get_name()}][{self.task_id}] initialize failed: {str(e)}"
            logger.error(error_msg)
            return TaskStatus.FAILED