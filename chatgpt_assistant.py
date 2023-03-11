import openai
import os
import datetime

openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize messages as an empty list
messages = []

# Define a function to generate the filename for the chat history file
def get_filename():
    now = datetime.datetime.now()
    date_string = now.strftime("%Y-%m-%d %H-%M-%S")
    return f"chat_{date_string}.txt"

# Define a function to replace the summary in the chat history file
def replace_summary(filename, new_text):
    with open(filename, "r+") as f:
        text = f.read()

        # Find the index of the keyword in the text
        index = text.find("Summary: ")

        if index != -1:
            # Find the index of the next occurrence of "System:"
            end_index = text.find("System:", index)

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
    with open(filename, "r") as f:
        text = f.read()

        # Find the index of the keyword in the text
        index = text.find("Summary: ")

        if index != -1:
            # Find the index of the next occurrence of "System:"
            end_index = text.find("System:", index)

            # Extract the text between the keyword and "System:"
            summary = text[index + len("Summary: "):end_index].strip()

            return summary
        else:
            return("No summary found.")

# Ask the user if they want to load a chat history file
load_file = input("Do you want to load a chat history file? (y/n): ")

if load_file.lower() == "y":
    # Display a list of chat history files in the "history" subdirectory
    history_files = [f for f in os.listdir("history") if f.endswith(".txt")]
    print("Please choose a chat history file to load:")
    for i, filename in enumerate(history_files):
        # Get the file modification time in a human-readable format
        mod_time = datetime.datetime.fromtimestamp(os.path.getmtime(os.path.join("history", filename)))
        mod_time_str = mod_time.strftime("%Y-%m-%d %H:%M:%S")
        summary = read_summary(os.path.join("history", filename),)
        # Print file infos
        print(f"{i+1}.\t{filename} - Last modified: {mod_time_str}\n{summary}\n")

    # Prompt the user to choose a file to load
    selection = int(input()) - 1
    filename = os.path.join("history", history_files[selection])

    # Load the chat history from the selected file
    with open(filename, "r") as f:
        for line in f:
            if line.startswith("User:"):
                messages.append({"role": "user", "content": line[6:].strip()})
            elif line.startswith("ChatGPT:"):
                messages.append({"role": "assistant", "content": line[9:].strip()})

    print(f"Loaded chat history from file: {filename}\n")
    print("Chat history content:\n")
    with open(filename, "r") as f:
        print(f.read())
else:
    filename = os.path.join("history", get_filename())
    with open(filename, "a") as f:
        # Write the system prompt to the file
        f.write("Summary: \n")
        f.write("System: You’re a kind and helpful assistant\n\n\t*** Starting the chat ***\n\n")

while True:
    content = input("User: ")

    # Check if the user input is "stop"
    if content.lower() == "stop":
        # Summarize he contents of the chat and write it in txt-file
        content = "Summarize the chat history so far in 255 characters max"
        messages.append({"role": "user", "content": content})
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        summary = completion.choices[0].message.content
        replace_summary(filename, summary)
        # Get current datetime and add it the chat history
        now = datetime.datetime.now()
        with open(filename, "a") as f:
            f.write(f"\t** Above chat history stored on {now:%Y-%m-%d %H:%M:%S}! **\n\n")
        print("\nChat history stored and script stopped.")
        break  # Exit the loop
    
    messages.append({"role": "user", "content": content})

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    chat_response = completion.choices[0].message.content
    print(f'\nChatGPT: {chat_response}\n')

    # Append the chatbot response to the chat history file
    with open(filename, "a") as f:
        f.write(f"User: {content}\n\n")
        f.write(f"ChatGPT: {chat_response}\n\n")

    messages.append({"role": "assistant", "content": chat_response})
