**🎙️ Voice Enabled AI Agent (RAG Based)**

This project is a voice-enabled AI assistant built using Streamlit, Deepgram Speech-to-Text, Retrieval-Augmented Generation (RAG), and multiple LLMs.

Users can speak their question in real time, the system converts speech to text, retrieves relevant information from website documents, and generates accurate answers using AI models.


**🧠 Architecture Diagram (Text Version)**

+--------------------------------------------------+

|                  USER BROWSER                    |

|                                                  |

|   🎤 Voice Input     ⌨ Text Input               |

|                                                   |

|   🔊 Browser Text-to-Speech                     |

+-------------------------+------------------------+

                          |
                          
                          v
                          
+--------------------------------------------------+

|               STREAMLIT FRONTEND                 |

|                 agent_app.py                     |

|                                                  |

| - UI handling                                    |

| - Session state                                  |

| - Input validation                               |

+-------------------------+------------------------+

                          |
                          
                          v
                          
+--------------------------------------------------+

|           SPEECH TO TEXT (DEEPGRAM)              |

|                                                  |

|   Audio (.wav) → Transcript (text)               |

+-------------------------+------------------------+

                          |
                          
                          v
                          
+--------------------------------------------------+

|              RAG PIPELINE                         |

|                                                   |

|  - Text Chunking                                  |

|  - Embeddings (HuggingFace)                       |

|  - Vector Search (Chroma DB)                      |

|                                                   |

|  Output: Relevant Context                         |

+-------------------------+------------------------+

                          |
                          
                          v
                          
+--------------------------------------------------+

|               LLM ORCHESTRATION                   |

|                                                   |

|   🤖 Gemini                                       |

|                                                   |

|   🤖 DeepSeek                                     |

|                                                   |

|  Prompt = Context + User Query                    |

+-------------------------+------------------------+

                          |
                          
                          v
                          
+--------------------------------------------------+

|              RESPONSE OUTPUT                      |

|                                                   |

|  - Text responses                                 |

|  - Browser speech synthesis                       |

+--------------------------------------------------+

**✨ Features**

🎤 Voice input using Deepgram (stable & production ready)

⌨ Manual text input

🧠 RAG-based document understanding

🔍 Chroma vector database

🤖 Multiple LLM comparison

Google Gemini


DeepSeek

🔊 Browser-native Text-to-Speech 

📚 Website / document ingestion

⚡ Real-time Streamlit UI

**🏗️ Tech Stack**
Component Technology

Frontend	Streamlit

Speech to Text	Deepgram

Embeddings	HuggingFace

Vector DB	Chroma

LLM APIs	Gemini, DeepSeek

TTS	Browser SpeechSynthesis

Backend	Python

⚙️ Setup Instructions

1️⃣ Clone Repository

git clone 

cd voice-ai-agent

2️⃣ Create Virtual Environment

python -m venv venv

venv\Scripts\activate  

3️⃣ Install Dependencies

pip install -r requirements.txt

5️⃣ Ingest Website or Documents

Edit ingest.py with your website URLs or documents.

Then run:

python ingest.py

6️⃣ Run the Application

streamlit run agent_app.py

⚠️ Limitations

These are known limitations of the current system:

Free API limitations

Deepgram free tier has usage limits

LLM free tiers may return limited or generic responses

No real-time streaming transcription

Audio is recorded first, then transcribed

True live transcription is not implemented

RAG quality depends on ingestion

If documents are not properly ingested, answers may be incomplete

“No information available” appears when retriever returns 0 documents

No authentication
