
import os
os.environ["TEAM_API_KEY"] = "a71cb641541aedfbdffdd8e4b32db084e96e4fadf1df3ca93899f7f6c57743a4"
from aixplain.factories import AgentFactory
import time
from config import API_KEY


def aispeechmode(query):

    
    try:
        
        agent = AgentFactory.create(
            name="NOVAAGENT3",
            # llm_id=API_KEY,
            description="This agent is designed to answer questions and assist with tasks."
        )

        # Run the agent with a specific query
        agent_response = agent.run(query)

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

    return agent_response

if __name__=="__main__":
    print(aispeechmode(input("enter your  query:")))



