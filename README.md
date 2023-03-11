***ChatGPT Assistant***

*Author: q-kuwe-w*

*Date: 11th March 2023*

This Python script implements a chatbot assistant using the OpenAI GPT-3.5 Turbo model. The script allows users to interact with the chatbot via a command line interface, and saves the chat history to a text file for future reference.

**Prerequisites**

Before using this script, you'll need to have the following:

    - An OpenAI API key, which you can obtain by signing up for an account on the OpenAI website.
    - Store the OpenAI API key as an environment variable as OPENAI_API_KEY
    - The openai Python module, which you can install by running "pip install openai".
    - Python 3.x installed on your computer.

**Usage**

To run the script, simply navigate to the directory containing the **chatgpt_assistant.py** file and run the following command:

    python chatgpt_assistant.py

The script will prompt you to choose whether to load an existing chat history file or start a new chat. If you choose to load a chat history file, the script will display a list of available files in the history subdirectory, along with a summary of each file's contents. If you choose to start a new chat, the script will create a new chat history file with a default system prompt.

Once the chat has started, you can enter messages in the command line interface and receive responses from the chatbot. To end the chat and save the chat history to a text file, simply enter the command 'stop'. The script will then prompt you to provide a summary of the chat history, which it will save to the chat history file as metadata.

**License**

This script is provided under the MIT License. Feel free to use and modify it for your own purposes.
