import os
import autogen
from dotenv import load_dotenv

load_dotenv()

def prompt_generator():
   global printer
   prompt_generator_system_message = """
   you are a prompt generator for a flowchart
   first you understand prompt given by user
   then generate a small and simple stept for creating flowchart
   also write a symbol for flowchart in bracket 
   Start (oval shape)
   Decision (diamond shape)
   give also clearification if decision is yes then go right and if no then go left
   Process (rectangle shape)
   End (oval shape)
   and also provide full instruction for how to create vertical flow chart from given 
   main focused in decision right and left side
   """

   prompt_generator_agent = autogen.AssistantAgent(
      "prompt_generator_agent",
      system_message=prompt_generator_system_message,
      llm_config={"config_list": [{"model": "gpt-4o-mini", "api_key": os.environ["OPENAI_API_KEY"]}]},
   )

   user_proxy = autogen.UserProxyAgent(
      name="user_proxy",
      human_input_mode="NEVER",
      max_consecutive_auto_reply=1,
      is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
      code_execution_config={"work_dir": "prompt", "use_docker": False},
   )

   task = input("Enter your prompt: ")

   users = user_proxy.initiate_chat(
      prompt_generator_agent,
      message=task
   )
   printer = users.chat_history[-3]["content"]




def flowchart_generator():

   code_writer_system_message = """
   You are a helpful AI assistant.
   Solve tasks using your coding and language skills.
   In the following cases, suggest python code (in a python coding block) or shell script (in a sh coding block) for the user to execute.
   1. When you need to collect info, use the code to output the info you need, for example, browse or search the web, download/read a file, print the content of a webpage or a file, get the current date/time, check the operating system. After sufficient info is printed and the task is ready to be solved based on your language skill, you can solve the task by yourself.
   2. When you need to perform some task with code, use the code to perform the task and output the result. Finish the task smartly.
   Solve the task step by step if you need to. If a plan is not provided, explain your plan first. Be clear which step uses code, and which step uses your language skill.
   When using code, you must indicate the script type in the code block. The user cannot provide any other feedback or perform any other action beyond executing the code you suggest. The user can't modify your code. So do not suggest incomplete code which requires users to modify. Don't use a code block if it's not intended to be executed by the user.
   If you want the user to save the code in a file before executing it, put # filename: <filename> inside the code block as the first line. Don't include multiple code blocks in one response. Do not ask users to copy and paste the result. Instead, use 'print' function for the output when relevant. Check the execution result returned by the user.
   If the result indicates there is an error, fix the error and output the code again. Suggest the full code instead of partial code or code changes. If the error can't be fixed or if the task is not solved even after the code is executed successfully, analyze the problem, revisit your assumption, collect additional info you need, and think of a different approach to try.
   When you find an answer, verify the answer carefully. Include verifiable evidence in your response if possible.

   Create a flowchart with the following characteristics:

   Write a Python code to create a traditional flowchart of the following scenario use Graphviz:

   ------>  Main important thing is Align symbols vertically where possible step by step and maintain symbol shape

   Flowchart Creation Guidelines:

   1. Structure:
   Use a top-down layout with a single entry point at the top and one or more exit points at the bottom.
   Ensure all steps are included with no dead ends or unclear paths.

   2. Symbols:
   Use ovals for start and end points.
   Use rectangles for processes.
   Use diamonds for decision points.
   Ensure symbols are sized to fit text well.

   3. Connectors:
   Use straight lines with arrows to indicate flow direction.
   Avoid crossing lines; use curves if necessary.

   4. Text:
   Keep text concise and centered within symbols.
   Ensure text does not overlap with lines or other text.

   5. Layout:
   Align symbols vertically where possible.
   Use horizontal spacing for parallel processes.
   Maintain consistent symbol sizes and spacing.

   6. Color Scheme:
   Use a consistent color for shapes (e.g., light blue).
   Use black for text and connector lines.

   7. Branching and Looping:
   Clearly show branching for decision outcomes.
   Indicate loops with backward-flowing arrows.

   8.Readability:
   Ensure the flowchart is readable from top to bottom.
   Keep all text horizontal and legible.

   9. Formatting:
   Use clean, straight lines for a professional appearance.
   Avoid unnecessary decorations.

   10. Scale:
   Size the flowchart to fit on a single page or screen.
   Ensure all elements are visible and legible.
   Reply 'TERMINATE' in the end when everything is done.

   Remember to adapt the flowchart to the specific process being illustrated, while maintaining these structural and stylistic guidelines for clarity and consistency.

   Save the traditional flowchart to a file named 'traditional.png.'
   terminate program when you finish the task
   """

   file_manager_system_message = """
   You are a file management assistant. Your primary role is to save files and manage file-related operations.
   When asked to save a file, use the appropriate Python code to save the file in the specified format and location.
   Always confirm when a file has been successfully saved and provide the file path.
   If there are any issues with file saving or management, report the error and suggest possible solutions.
   """
   link = r"D:\AUTOGEN\flow\Flowchart-Example2.png"
   tester_system_message =f"""
   you are flowchart tester agent 
   {link} follow this for referance and check flowchart are organized according to this format
   text are fit in shape symbol if text not fit in shape then make enter in new line or make shape bigger but arreng in in correct position
   your role is check flowchart is follows user prompt or not, if not make it proper
   must check flowchart are in vertical format or not if not make it vertical
   symbols are in their shape according to user prompt or not if not make it proper
   text not overlap with lines and other text
   terminate program when you finish the task
   """

   code_writer_agent = autogen.AssistantAgent(
      "code_writer_agent",
      system_message=code_writer_system_message,
      llm_config={"config_list": [{"model": "gpt-4o-mini", "api_key": os.environ["OPENAI_API_KEY"]}]},
      code_execution_config={"use_docker": False},  # Turn off code execution for this agent.
   )

   file_manager_agent = autogen.AssistantAgent(
      "file_manager_agent",
      system_message=file_manager_system_message,
      llm_config={"config_list": [{"model": "gpt-4o-mini", "api_key": os.environ["OPENAI_API_KEY"]}]},
      code_execution_config={"work_dir": "flow", "use_docker": False},
   )

   tester_agent = autogen.AssistantAgent(
      "tester_agent",
      system_message=tester_system_message,
      llm_config={"config_list": [{"model": "gpt-4o-mini", "api_key": os.environ["OPENAI_API_KEY"]}]},
      code_execution_config={"use_docker": False},
   )

   user_proxy = autogen.UserProxyAgent(
      name="user_proxy",
      human_input_mode="TERMINATE",
      max_consecutive_auto_reply=1,
      is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
      code_execution_config={"use_docker": False},
   )

   task = printer

   # Create a group chat
   groupchat = autogen.GroupChat(
      agents=[user_proxy, code_writer_agent, file_manager_agent, tester_agent],
      messages=[],
      max_round=50
   )

   # Create a group chat manager
   manager = autogen.GroupChatManager(groupchat=groupchat)

   # Start the group chat
   user_proxy.initiate_chat(
      manager,
      message=task
   )

prompt_generator()
flowchart_generator()