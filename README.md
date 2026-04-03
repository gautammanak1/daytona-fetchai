# Job Search Agent

[![Fetch.ai](https://img.shields.io/badge/Fetch.ai-uAgents-purple)](https://fetch.ai)
[![Daytona](https://img.shields.io/badge/Daytona-Sandbox-orange)](https://www.daytona.io)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)](https://python.org)
![innovationlab](https://img.shields.io/badge/innovationlab-3D8BD3)
![tag:uagents](https://img.shields.io/badge/tag-uagents-blue)

A natural-language job search agent built with Fetch.ai uAgents and Daytona sandboxes. Parses job queries, searches via RapidAPI JSearch, and deploys a live Flask preview of matching results inside a secure sandbox.

## Features

- **Natural Language Queries** — Parses job type, location, employment type, and experience level from free-text input
- **JSearch Integration** — Searches real job listings via the RapidAPI JSearch API
- **Sandbox Deployment** — Spins up a Daytona sandbox with a Flask app to display results
- **Live Preview URL** — Returns a browsable URL with formatted job listings
- **Chat Protocol** — Works as a uAgent with standard chat protocol for agent-to-agent messaging
- **Smart Parsing** — Extracts keywords like "remote", "internship", "senior" from natural language

## Architecture

```
User Chat → uAgent → Parse Query → JSearch API → Daytona Sandbox
                                                      ├── Generate Flask app
                                                      ├── Render job listings
                                                      └── Return preview URL
```

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Agent Framework | Fetch.ai uAgents + Chat Protocol |
| Sandbox | Daytona |
| Job Search API | JSearch (RapidAPI) |
| Web Preview | Flask |
| NLP Parsing | Built-in keyword extraction |

## Getting Started

### Prerequisites

- Python 3.10+
- Daytona API key
- RapidAPI JSearch API key

### Installation

```bash
git clone https://github.com/gautammanak1/daytona-fetchai.git
cd daytona-fetchai
pip install -r requirements.txt
```

### Configuration

Create a `.env` file:

```env
DAYTONA_API_KEY=your_daytona_api_key
JSEARCH_API_KEY=your_rapidapi_key
```

### Run

**CLI Mode** (no agents):

```bash
python job_search.py
```

**Agent Mode** (uAgents chat protocol):

```bash
python agent.py
```

### Example Query

```
Remote data science internship in New York
```

The agent parses this into job type, location, and employment type, then returns a live preview URL with matching listings.

## Project Structure

```
├── agent.py           # uAgents chat agent
├── job_search.py      # Core job search + Daytona sandbox logic
├── requirements.txt   # Python dependencies
└── README.md
```

## License

MIT
