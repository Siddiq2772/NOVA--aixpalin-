import os
import AppOpener
import json
os.environ["TEAM_API_KEY"] = "a71cb641541aedfbdffdd8e4b32db084e96e4fadf1df3ca93899f7f6c57743a4"
from aixplain.factories import AgentFactory
from config import API_KEY

def scanapp():
    app_keys=AppOpener.give_appnames()
    return app_keys

commands_list = [
    "go to <website name>",
    "search on google <query>",
    "open <app/system tool>",
    "close <app/system tool>",
    "ip address of my device",
    "search on wikipedia <topic>",
    "send message <message>",
    "current temperature <city_name>",
    "play video on youtube <video_name>",
    "current time",
    "battery",
    "current date",
    "ai mode <query>",
    "shutdown",
    "restart",
    "sleep",
    "mute",
    "unmute",
    "Incomplete command: <correct_command>",
    "minimise window",
    "maximise window",
    "close window",
    "help"
    "exit"
]

def aiprocess(command):
    
    app_keys=scanapp()
    
    with open('task.json', 'r') as file:
        task_data = json.load(file)
    
    json_data_str = json.dumps(task_data, indent=2)
    
    prompt = (
        f"Your name is NOVA. You are a command assistant designed to help users, including those who may be illiterate or make mistakes in their input. "
        f"Your task is to interpret the user's intent and correct any spelling mistakes, command structure errors, or word choice issues. "
        f"Consider the following possibilities for mistakes:\n"
        f"- The user might confuse 'go to' for websites and apps. If they say 'go to' followed by a website name, change it to 'go to <website>.com' if not specified. For apps, return 'open <app>' or 'close <app>' as needed, but only if the app name exists in the user's installed apps, which are listed in {app_keys}.\n"
        f"- If the user says 'open' or 'close' followed by a website name, change it to 'go to <website>.com'.\n"
        f"- Ensure the command returns the exact app name required by the AppOpener library from this list: {app_keys}. If the user provides an app name not listed in {app_keys}, inform the user that the app is not available.\n"
        f"- Match user input to the correct app name supported by the AppOpener library from {app_keys}. This includes handling common variations, abbreviations, and misspellings.\n"
        f"- Handle spelling errors or typos in app names and correct them automatically.\n"
        f"- If the user says something like 'go to <website>' or 'open <website>', check if it's a website. Append '.com' if it's missing, and ensure the response is 'go to <website>.com'.\n"
        f"- If the user says 'search on wikipedia', 'wikipedia search', or any variation of that command, return 'search on wikipedia <topic>' and extract the topic from the command.\n"
        f"- If the user only types 'AI' instead of 'AI mode', assume they meant 'AI mode'.\n"
        f"- The user might give incomplete commands. For example, if the user types 'go to google', it should be interpreted as a web search with the command 'go to google.com'. If they say 'search on google' without a query, return 'Incomplete command: search on google <query>'.\n"
        f"- If the user gives an incomplete command, such as 'open app' without specifying the app, respond with 'Incomplete command: open <app_name>'. This will guide the user towards the correct format.\n"
        f"- If the user says anything resembling 'help', such as 'run help function', 'show help', 'assist', or 'guide', return the 'help' command.\n"
        f"- If the user says anything resembling 'exit', 'no thanks', 'close', or any phrase indicating the intent to stop or exit the software, return 'exit'.\n"
        f"- If the user asks a question related to any domain or field, interpret the question and provide a relevant answer, returning it in the format: 'AI mode: <answer>'.\n"
        f"- If the user asks for the temperature or weather of a particular city, return 'current temperature <city_name>'.\n\n"
        f"Commands List:\n"
        f"{commands_list}\n\n"
        f"Here is the app name mapping from the user's system (available apps):\n"
        f"{app_keys}\n\n"
        f"Task Data:\n"
        f"{json_data_str}\n\n"
        f"User Input: {command}\n\n"
        f"Response:\n"
        f"- If the user wants to open a website and says something like 'go to <website_name>' or 'open <website_name>', return 'go to <website_name>.com'.\n"
        f"- For apps, return 'open <app_name>' or 'close <app_name>' if the app exists in {app_keys}, or inform the user that the app is not available if it's not in {app_keys}.\n"
        f"- If the command is incomplete based on {commands_list} and does not match, return 'Incomplete command: <correct_command>'.\n"
        f"- If the user asks a question related to any domain or field, interpret the question and return 'AI mode: <answer>'.\n"
        f"- If the user asks for the temperature or weather of a particular city, return 'current temperature <city_name>'.\n"
        f"You are a professional web developer, app developer, and coder who can provide code or programming help in various languages."
    )

    try:
        agent = AgentFactory.create(
            name="NOVAagent3",
            # llm_id=API_KEY,
            description="This agent is designed to answer questions and assist with tasks."
        )

        # Run the agent with the custom prompt
        agent_response = agent.run(prompt)

        # Check if the response is successful and completed
        if agent_response['completed'] and agent_response['status'] == 'SUCCESS':
            output = agent_response['data']['output']
            session_id = agent_response['data']['session_id']
            run_time = agent_response['data']['intermediate_steps'][0]['runTime']
            used_credits = agent_response['data']['intermediate_steps'][0]['usedCredits']

            # Standardized output format
            print("----- NOVAagent Response -----")
            print(f"Response: {output}")
            print(f"Session ID: {session_id}")
            print(f"Run Time: {run_time:.2f} seconds")
            print(f"Credits Used: {used_credits:.5f}")
            print("-------------------------------")
            return output
        else:
            print("Error: ", agent_response)

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        agent.delete()
