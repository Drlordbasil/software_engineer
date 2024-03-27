import logging
import os
import subprocess
import re
import venv
from language_model import openai_api
from browser_automation.browser import Browser

logger = logging.getLogger(__name__)

class AutomatedSoftwareEngineer:
    def __init__(self, name, tools, api_key):
        self.name = name
        self.tools = tools
        self.openai_api = openai_api.OpenAIAPI(api_key)
        self.inner_thoughts = []
        self.browser = Browser()
        self.repo_path = "agent_workspace"
        self.task_completed = False

    def complete_task(self, task_description):
        logger.info(f"Completing task: {task_description}")

        while not self.task_completed:
            # Step 1: Reflect on the task
            self.reflect_on_task(task_description)

            # Step 2: Browse the web for relevant information and save it for reference
            self.browse_and_save_references(task_description)

            # Step 3: Generate code using OpenAI API with verbose logging
            generated_code = self.generate_code_with_logging(task_description)

            # Step 4: Create requirements.txt based on the generated code
            self.create_requirements_file(generated_code, task_description)

            # Step 5: Create a virtual environment and install requirements
            self.create_venv_and_install_requirements(task_description)

            # Step 6: Save the generated code to a file
            self.save_code_to_file(generated_code, task_description)

            # Step 7: Execute the generated code and test it
            self.execute_and_test_code(task_description)

            # Step 8: Reflect on the results and improve systematically
            self.reflect_and_improve(task_description)

            # Step 9: Commit and push changes to version control
            self.commit_and_push_changes(task_description)

            # Step 10: Ask the user for thoughts and satisfaction
            self.ask_user_for_feedback(task_description)

        logger.info(f"Task completed: {task_description}")
        return generated_code

    def reflect_on_task(self, task_description):
        prompt = f"Please take a moment to reflect on the task: {task_description}. What are your initial thoughts and approach to completing this task?"
        reflection = self.openai_api.complete(prompt)
        logger.info(f"Reflection: {reflection}")
        self.inner_thoughts.append(reflection)

    def browse_and_save_references(self, task_description):
        prompt = f"Based on the task '{task_description}', what libraries or tools might be useful? Please provide a list of relevant libraries and their documentation URLs."
        references = self.openai_api.complete(prompt)
        logger.info(f"References: {references}")

        urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', references)
        for url in urls:
            try:
                self.browser.navigate(url)
                logger.info(f"Navigated to: {url}")
                self.save_reference(url)
            except Exception as e:
                logger.error(f"Error navigating to URL: {url}. Error: {e}")

    def save_reference(self, url):
        file_name = re.sub(r'[^\w\-_\. ]', '_', url.lower())
        file_name = '_'.join(file_name.split())
        file_path = os.path.join(self.repo_path, f"{file_name}.txt")

        with open(file_path, "w") as file:
            file.write(self.browser.get_page_source())

        logger.info(f"Reference saved to: {file_path}")

    def generate_code_with_logging(self, task_description):
        prompt = f"Based on the task '{task_description}', please provide the code to complete the task. Include verbose logging statements for debugging purposes."
        generated_code = self.openai_api.complete(prompt)
        logger.info(f"Generated code: {generated_code}")
        return generated_code

    def create_requirements_file(self, generated_code, task_description):
        prompt = f"Based on the following generated code:\n\n{generated_code}\n\nWhat are the required Python packages and their versions? Provide the packages and versions in the format suitable for a requirements.txt file."
        requirements = self.openai_api.complete(prompt)

        file_name = re.sub(r'[^\w\-_\. ]', '_', task_description.lower())
        file_name = '_'.join(file_name.split())
        requirements_path = os.path.join(self.repo_path, f"{file_name}_requirements.txt")

        with open(requirements_path, "w") as file:
            file.write(requirements)

        logger.info(f"Generated requirements saved to: {requirements_path}")

    def create_venv_and_install_requirements(self, task_description):
        dir_name = re.sub(r'[^\w\-_\. ]', '_', task_description.lower())
        dir_name = '_'.join(dir_name.split())
        venv_path = os.path.join(self.repo_path, f"{dir_name}_venv")

        venv.create(venv_path, with_pip=True)
        logger.info(f"Created virtual environment: {venv_path}")

        file_name = re.sub(r'[^\w\-_\. ]', '_', task_description.lower())
        file_name = '_'.join(file_name.split())
        requirements_path = os.path.join(self.repo_path, f"{file_name}_requirements.txt")

        if os.path.exists(requirements_path):
            subprocess.run([os.path.join(venv_path, "Scripts", "pip"), "install", "-r", requirements_path], check=True)
            logger.info(f"Installed requirements from {requirements_path}")
        else:
            logger.warning("Requirements file not found. Skipping package installation.")

    def save_code_to_file(self, generated_code, task_description):
        os.makedirs(self.repo_path, exist_ok=True)

        file_name = re.sub(r'[^\w\-_\. ]', '_', task_description.lower())
        file_name = '_'.join(file_name.split())
        file_path = os.path.join(self.repo_path, f"{file_name}.py")

        with open(file_path, "w") as file:
            file.write(generated_code)

        logger.info(f"Generated code saved to: {file_path}")

    def execute_and_test_code(self, task_description):
        file_name = re.sub(r'[^\w\-_\. ]', '_', task_description.lower())
        file_name = '_'.join(file_name.split())
        file_path = os.path.join(self.repo_path, f"{file_name}.py")

        dir_name = re.sub(r'[^\w\-_\. ]', '_', task_description.lower())
        dir_name = '_'.join(dir_name.split())
        venv_path = os.path.join(self.repo_path, f"{dir_name}_venv")

        try:
            subprocess.run([os.path.join(venv_path, "Scripts", "python"), file_path], check=True)
            logger.info(f"Executed code: {file_path}")
        except subprocess.CalledProcessError as e:
            logger.error(f"Error executing code: {file_path}. Error: {e}")

    def reflect_and_improve(self, task_description):
        prompt = f"Based on the execution of the code for the task '{task_description}', what improvements or optimizations can be made? Please provide your thoughts and any updated code snippets."
        reflection = self.openai_api.complete(prompt)
        logger.info(f"Reflection: {reflection}")
        self.inner_thoughts.append(reflection)

    def commit_and_push_changes(self, task_description):
        try:
            subprocess.run(["git", "add", "."], cwd=self.repo_path, check=True)

            commit_message = f"Implement task: {task_description}"
            subprocess.run(["git", "commit", "-m", commit_message], cwd=self.repo_path, check=True)

            subprocess.run(["git", "push"], cwd=self.repo_path, check=True)

            logger.info("Changes committed and pushed to version control.")
        except subprocess.CalledProcessError as e:
            logger.error(f"Error committing and pushing changes. Error: {e}")

    def ask_user_for_feedback(self, task_description):
        user_feedback = input(f"The task '{task_description}' has been completed. Please provide your thoughts and satisfaction level (0-5): ")
        if user_feedback.lower() == 'quit':
            self.task_completed = True
        elif int(user_feedback) >= 4:
            self.task_completed = True
            logger.info("User is satisfied with the task completion.")
        else:
            logger.info("User has requested further improvements.")

    def quit(self):
        self.browser.quit()