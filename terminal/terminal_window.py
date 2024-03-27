import subprocess
import logging

logger = logging.getLogger(__name__)

class TerminalWindow:
    def execute_command(self, command):
        try:
            output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
            logger.info(f"Executed command: {command}")
            return output.decode('utf-8')
        except subprocess.CalledProcessError as e:
            logger.error(f"Command execution failed: {command}\nError: {e.output.decode('utf-8')}")
            return None

    def send_input(self, input_text):
        try:
            subprocess.run(f"echo '{input_text}' > /dev/tty", shell=True, check=True)
            logger.info(f"Sent input to terminal: {input_text}")
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to send input to terminal: {input_text}\nError: {e}")