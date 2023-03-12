# Necessary packages to import
import openai # Can be installed by using pip install openai
import os
import datetime

# Get the OpenAI api key from the environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

# LISTS, DICIONARIES AND FOLDERS
# Initialize messages as an empty list
messages = []
# Initialize system_messages as a dictionary
system_messages = {
    "load_history": "Do you want to load a chat history file? (y/n): ",
    "choose_file": "Please choose a chat history file to load:\n",
    "file_info": "{0}.\t{1} - Last modified: {2}\n{3}\n",
    "loaded_history": "Loaded chat history from file: {}\n",
    "history_content": "Chat history content:\n",
    "start_chat": "\t*** Starting the chat ***\n\n",
    "stored_history": "\t** Above chat history stored on {}! **\n\n",
    "stop_script": "\nChat history stored and script stopped."
}
# Defining the default chat history folder name
folder_name = 'history'

# FUNCTIONS
def get_filename():
    """Returns a string representing a filename that includes the current date 
    and time.

    This function uses the current date and time to create a filename in the 
    following format: 'chat_YYYY-MM-DD HH-MM-SS.txt'. The filename can be used 
    to save chat logs, for example.

    Returns:
    --------
    filename : str
        A string representing a filename with the current date and time 
        included, in the format 'chat_YYYY-MM-DD HH-MM-SS.txt'.
    """
    now = datetime.datetime.now()
    date_string = now.strftime("%Y-%m-%d %H-%M-%S")
    return f"chat_{date_string}.txt"

def replace_summary(filename, new_text):
    """Replaces the 'Summary' section in a text file with new text.

    This function searches for the 'Summary' section identified by the keyword 
    "Summary: " in the specified text file, and replaces it with the provided 
    `new_text`. If the keyword is not found in the file, no modifications are 
    made.

    Parameters:
    -----------
    filename : str
        The name of the text file to modify.
    new_text : str
        The new text to replace the existing 'Summary' section with.

    Returns:
    --------
    None
        This function does not return any values; it modifies the specified 
        file in place.
    """
    with open(filename, "r+") as f:
        text = f.read()

        # Find the index of the keyword in the text
        index = text.find("Summary: ")

        if index != -1:
            # Find the index of the next occurrence of "System:"
            end_index = text.find("\t*** Starting the chat ***", index)

            # Replace the text between "Summary:" and "System:"
            new_text = f"Summary: {new_text}\n\n"
            text = text[:index] + new_text + text[end_index:]

            # Write the modified text back to the file
            f.seek(0)
            f.write(text)
            f.truncate()
            print("\nSummary updated successfully!")
        else:
            print("\nKeyword not found in file.")

def read_summary(filename):
    """Reads the 'Summary' section from a text file.

    This function reads the contents of a text file with the specified filename 
    and extracts the 'Summary' section identified by the keyword "Summary: ". 
    If the keyword is not found in the file, the function returns 
    'No summary found.'.

    Parameters:
    -----------
    filename : str
        The name of the text file to read the summary from.

    Returns:
    --------
    summary : str
        The text of the 'Summary' section in the specified file. If the summary 
        is not found, returns 'No summary found.'.
    """
    with open(filename, "r") as f:
        text = f.read()

        # Find the index of the keyword in the text
        index = text.find("Summary: ")

        if index != -1:
            # Find the index of the next occurrence of "System:"
            end_index = text.find("\t*** Starting the chat ***", index)

            # Extract the text between the keyword and "System:"
            summary = text[index + len("Summary: "):end_index].strip()

            return summary
        else:
            return("No summary found.")
        
def get_response(messages_lod):
        """
        Sends a list of messages to the OpenAI GPT-3 model and returns
        a response generated by the model.

        Args:
        - messages_lod (list of dictionaries): A list of dictionaries 
          representing each message sent to the model. Each dictionary must 
          contain a 'text' key with the text of the message and a 'user' key 
          with the name of the user sending the message.

        Returns:
        - response (str): A string representing the response generated by the 
          GPT-3 model in response to the messages received.
        """
        # Sends the list of messages to the OpenAI GPT-3 model    
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages_lod
        )
        # Returns the first response in the list of choices returned by model
        response = completion.choices[0].message.content
        return response

# MAIN CODE SECTION
# Check for a 'history'-folder in the cwd and if it does not exist make it
cwd = os.getcwd()
history_folder = os.path.join(cwd, folder_name)

if not os.path.exists(history_folder):
    os.makedirs(history_folder)

# Ask the user if they want to load a chat history file
load_file = input(system_messages["load_history"])

# If 'yes' display selection of available files, prompt to choose and load file 
if load_file.lower() == "y":
    # Display a list of chat history files in the 'history' subdirectory
    history_files = [f for f in os.listdir(folder_name) if f.endswith(".txt")]
    print('\n')
    print(system_messages["choose_file"])
    for i, filename in enumerate(history_files):
        # Get the file modification time in a human-readable format
        mod_time = datetime.datetime.fromtimestamp(os.path.getmtime(os.path.join(folder_name, filename)))
        mod_time_str = mod_time.strftime("%Y-%m-%d %H:%M:%S")
        summary = read_summary(os.path.join(folder_name, filename),)
        # Print file infos
        print(system_messages["file_info"].format(i+1, filename, mod_time_str, summary))

    # Prompt the user to choose a file to load
    selection = int(input()) - 1
    filename = os.path.join(folder_name, history_files[selection])

    # Load the chat history to list of dictionaries 'messages' from selected file
    with open(filename, "r") as f:
        for line in f:
            if line.startswith("User:"):
                messages.append({"role": "user", "content": line[6:].strip()})
            elif line.startswith("ChatGPT:"):
                messages.append({"role": "assistant", "content": line[9:].strip()})
    print(system_messages["loaded_history"].format(filename))
    
    # Display the chat history in the console
    print(system_messages["history_content"])
    with open(filename, "r") as f:
        print(f.read())

# If 'no' make new chat history file in the  default folder
else:
    filename = os.path.join(folder_name, get_filename())
    with open(filename, "a") as f:
        # Write the system prompt to the file
        f.write("Summary: \n")
        f.write(system_messages["start_chat"])

while True:
    content = input("User: ")

    # Check if the user input is "stop"
    if content.lower() == "stop":
        # Summarize the contents of the chat and write it in txt-file
        content = "Summarize the chat history so far in 255 characters max"
        messages.append({"role": "user", "content": content})
        # Get chatbot summary of chat history
        summary = get_response(messages)
        # Call the replace summary function for the chat history file
        replace_summary(filename, summary)
        # Get current datetime and add it the chat history
        now = datetime.datetime.now()
        with open(filename, "a") as f:
            f.write(system_messages["stored_history"].format(now.strftime("%Y-%m-%d %H:%M:%S")))
        print(system_messages["stop_script"])
        break  # Exit the loop
    
    # Append the user prompt to the chat history file
    messages.append({"role": "user", "content": content})
    # Get chatbot response
    chat_response = get_response(messages)
    
    # Print chatbot response
    print(f'\nChatGPT: {chat_response}\n')

    # Append the chatbot response to the chat history file
    with open(filename, "a") as f:
        f.write(f"User: {content}\n\n")
        f.write(f"ChatGPT: {chat_response}\n\n")
    # Append the chatbot response to the messages list of dictionaries
    messages.append({"role": "assistant", "content": chat_response})
