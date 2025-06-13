
graph TD
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
