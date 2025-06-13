
# Multi-Agentic Anime Series Creator

This system uses the crewAI framework and Google's Gemini Pro models to autonomously create and upload a continuous anime series to a YouTube channel.

## Overview

The system is built around a "crew" of specialized AI agents, each responsible for a specific part of the anime production pipeline. It follows a dual-process architecture:
1.  A **Daily Production Loop** that autonomously creates and uploads a new 5-minute episode.
2.  An **On-Demand Character Creation** utility to introduce new characters to the series.

This structure ensures creative flexibility while maintaining strict narrative and visual consistency for the established cast.

## Features

- **Autonomous Daily Production:** Runs on a schedule to create and upload a new 5-minute episode.
- **Multi-Agent System:** Uses `crewAI` to orchestrate specialized agents for story, script, multimedia production, and distribution.
- **Long-Term Memory:** Employs a ChromaDB vector store to remember past episodes, ensuring a coherent and continuous storyline.
- **Static "Series Bible":** Uses a `config.py` file to store foundational information like character personalities and the core story premise, ensuring consistency.
- **On-Demand Character Creation:** A separate script allows a "showrunner" to generate new characters, which can then be permanently added to the series bible.
- **Automated YouTube Uploads:** An agent handles the entire process of uploading the final video to a specified YouTube channel.

## Architecture

The system's architecture is split into two distinct workflows:

### 1. Daily Production Loop (Automated)

This is the core pipeline that runs every day:

1.  **Story Development:** The `StorylineAgent` queries the memory of past episodes and reads the `config.py` "Series Bible" to generate a plot for the new episode.
2.  **Script Writing:** The `ScriptWriterAgent` takes the plot and writes a detailed script, including dialogue, actions, and emotional cues, referencing the character personalities from the config.
3.  **Parallel Asset Generation:** The `ProductionAgent` generates all visual and audio assets based on the script. *(Note: This is currently simulated).*
4.  **Post-Production:** The `CompilerAgent` stitches all generated assets (video, voice, music, SFX) into a single MP4 file.
5.  **Distribution & Memory:** The `YouTubeUploaderAgent` uploads the final video and saves a summary of the episode back to the vector memory database for future context.

### 2. Character Management (On-Demand & Manual)

This process is used to expand the cast without disrupting the daily flow:

1.  **Initiation:** The "showrunner" (you) decides a new character is needed.
2.  **Execution:** You run the `create_new_character.py` script.
3.  **Generation:** The `CharacterCreatorAgent` generates a detailed character sheet based on a simple concept provided by the showrunner.
4.  **Integration (Human-in-the-Loop):** The showrunner reviews the generated character sheet and, if approved, manually copies the information into the `CHARACTERS` dictionary within the `config.py` file.

Once a character is added to `config.py`, they become a permanent part of the series and are known to all agents in the daily production loop.

## Setup

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd anime_creator
```

### 2. Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```



4. Install Dependencies
```bash
pip install -r requirements.txt
```

5. Environment Variables

Create a .env file in the root directory and add your Google API Key:

```bash
# .env file
GOOGLE_API_KEY="your_google_api_key_here"
```
5. YouTube API Setup (Crucial!)

To upload videos, you need to enable the YouTube Data API v3.

Go to the Google Cloud Console.

Create a new project.

Enable the "YouTube Data API v3".

Go to "Credentials", create an "OAuth 2.0 Client ID", and select "Desktop app".

Download the JSON file. Rename it to client_secrets.json and place it in the root directory of your project.

First Run: The first time the system attempts an upload, it will open a browser window asking you to authorize the application. After you grant permission, it will create a token.json file for all future automated uploads.

How to Run
Daily Episode Production

To start the daily production cycle, run the main script:
```bash
python main.py
```


The system is configured to run once immediately for testing. You can uncomment the schedule lines in main.py to have it run automatically every day.

Creating a New Character

When you need to introduce a new character to the story:

```bash
python create_new_character.py
```



```graph TD
    
    subgraph On-Demand Character Creation (Run as needed)
    direction LR
    AA[Showrunner decides to add a new character] --> BB(Run `create_new_character.py`);
    BB -- Generates Character Sheet --> CC{Human-in-the-Loop};
    CC -- Approves & Adds to config.py --> DD[config.py - Series Bible];
    end

    subgraph Daily Production Loop (Scheduled)
    direction TD
    A[Start Daily Job] --> B(Storyline Agent);
    B -- Queries --> C[Vector DB Memory - Past Episodes];
    B -- Reads --> DD;
    C -- Past Context --> B;
    DD -- Character & Story Info --> B;
    
    B -- Episode Plot --> D(Script Writer Agent);
    D -- Reads --> DD;
    D -- Final Script & Scene Breakdown --> E{Parallel Asset Production};

    subgraph Parallel Asset Production
        direction LR
        E --> F[Production Agent: Video];
        E --> G[Production Agent: Audio];
        E --> H[Production Agent: Music];
        E --> I[Production Agent: SFX];
    end

    F -- Visual Assets --> J;
    G -- Voiceovers --> J;
    H -- Background Music --> J;
    I -- Sound Effects --> J;
    
    J(Compiler Agent) -- Combines all assets --> K[Final Episode Video];
    K --> L(YouTube Uploader Agent);
    L -- Uploads --> M[YouTube Channel];
    L -- Episode Summary --> C;
    M --> N[End];
    end
```




