import os
import logging
from agent.agent import AutomatedSoftwareEngineer
from browser_automation.browser import Browser
from terminal.terminal_window import TerminalWindow
from config import OPENAI_API_KEY


def setup_logger(log_file_path, log_level=logging.INFO):
    os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file_path),
            logging.StreamHandler()
        ]
    )


def main():
    setup_logger('logs/agent.log')
    logger = logging.getLogger(__name__)

    browser = Browser()
    terminal = TerminalWindow()
    tools = [browser, terminal]

    agent = AutomatedSoftwareEngineer("Agent", tools, OPENAI_API_KEY)

    while True:
        task = input("Enter a task (or 'quit' to exit): ")
        if task.lower() == "quit":
            break

        generated_code = agent.complete_task(task)
        logger.info("Generated Code:")
        logger.info(generated_code)

        # Save the generated code to a file
        with open("generated_code.py", "w") as file:
            file.write(generated_code)

        # Execute the generated code in the terminal
        terminal.execute_command("python generated_code.py")

        # Perform browser automation based on the task
        if "go to" in task.lower():
            url = task.split("go to")[1].strip()
            browser.navigate(url)
        elif "click" in task.lower():
            selector = task.split("click")[1].strip()
            browser.click(selector)
        elif "type" in task.lower():
            selector, text = task.split("type")[1].strip().split(",")
            browser.type(selector.strip(), text.strip())

    browser.quit()


if __name__ == "__main__":
    main()