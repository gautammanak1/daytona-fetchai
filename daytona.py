#!/usr/bin/env python3
"""
Job Search with Daytona Sandbox
Combines job search functionality with Daytona sandbox execution and Flask web preview
"""

import requests
import json
import os
from typing import Dict, List, Any
import time
from daytona import Daytona, DaytonaConfig, SessionExecuteRequest

from dotenv import load_dotenv

load_dotenv()

class JobSearcher:
    """Main class for job searching with AI enhancement"""
    
    def __init__(self):
        """Initialize API credentials from environment variables"""
        self.jsearch_api_key = os.getenv('JSEARCH_API_KEY', '')
        self.jsearch_host = "jsearch.p.rapidapi.com"
        self.asi_api_key = os.getenv('ASI_ONE_API_KEY', '')
        self.asi_url = "https://api.asi1.ai/v1/chat/completions"
    
    def parse_job_query(self, user_prompt: str) -> Dict[str, str]:
        """Parse user prompt to extract job search parameters"""
        query_parts = {
            'job_type': self._extract_job_type(user_prompt),
            'location': self._extract_location(user_prompt),
            'employment_type': self._extract_employment_type(user_prompt),
            'experience_level': self._extract_experience_level(user_prompt),
        }
        return query_parts
    
    def _extract_job_type(self, text: str) -> str:
        """Extract job title/type from prompt"""
        keywords = ['internship', 'job', 'position', 'role', 'remote', 'onsite', 'hybrid']
        words = text.split()
        job_words = [w for w in words if w.lower() not in keywords and len(w) > 2]
        return ' '.join(job_words[:3]) if job_words else text
    
    def _extract_location(self, text: str) -> str:
        """Extract location from prompt"""
        locations = ['new york', 'san francisco', 'chicago', 'los angeles', 'seattle', 
                    'boston', 'austin', 'denver', 'miami', 'remote', 'anywhere', 'us', 'uk']
        text_lower = text.lower()
        for loc in locations:
            if loc in text_lower:
                return loc.replace(' ', '_').upper()
        return 'US'
    
    def _extract_employment_type(self, text: str) -> str:
        """Extract employment type"""
        text_lower = text.lower()
        if 'internship' in text_lower:
            return 'INTERNSHIP'
        elif 'part.time' in text_lower or 'part-time' in text_lower:
            return 'PART_TIME'
        elif 'contract' in text_lower or 'contractor' in text_lower:
            return 'CONTRACTOR'
        else:
            return 'FULLTIME'
    
    def _extract_experience_level(self, text: str) -> str:
        """Extract experience level"""
        text_lower = text.lower()
        if 'intern' in text_lower or 'junior' in text_lower or 'entry' in text_lower:
            return 'entry_level'
        elif 'senior' in text_lower or 'lead' in text_lower or 'staff' in text_lower:
            return 'senior'
        else:
            return 'mid_level'
    
    def search_jobs(self, user_prompt: str, num_pages: int = 1) -> List[Dict[str, Any]]:
        """Search for jobs based on user prompt"""
        params = self.parse_job_query(user_prompt)
        query = f"{params['job_type']} jobs in {params['location']}"
        
        headers = {
            "x-rapidapi-key": self.jsearch_api_key,
            "x-rapidapi-host": self.jsearch_host
        }
        
        querystring = {
            "query": query,
            "page": "1",
            "num_pages": str(num_pages),
            "country": "us",
            "date_posted": "all"
        }
        
        try:
            response = requests.get(
                f"https://{self.jsearch_host}/search",
                headers=headers,
                params=querystring
            )
            
            if response.status_code == 200:
                data = response.json()
                jobs = data.get('data', [])
                return jobs
            else:
                print(f"API Error: {response.status_code}")
                return []
        except Exception as e:
            print(f"Error searching jobs: {str(e)}")
            return []
    
    def format_job_listing(self, job: Dict[str, Any]) -> Dict[str, str]:
        """Format a single job listing for web display"""
        return {
            'title': job.get('job_title', 'N/A'),
            'company': job.get('employer_name', 'N/A'),
            'location': job.get('job_location', 'N/A'),
            'employment_type': job.get('job_employment_type', 'N/A'),
            'apply_link': job.get('job_apply_link', '#'),
            'website': job.get('employer_website') or job.get('employer_url') or '',
            'description': job.get('job_description', '')[:200] + '...' if job.get('job_description') else 'No description',
        }


def create_flask_app(jobs: List[Dict[str, Any]]) -> str:
    """Create Flask web app code with job results"""
    searcher = JobSearcher()
    formatted_jobs = [searcher.format_job_listing(job) for job in jobs[:10]]
    jobs_html = ""
    
    for i, job in enumerate(formatted_jobs, 1):
        jobs_html += f"""
        <div class="job-card">
            <h3>{i}. {job['title']}</h3>
            <p><strong>Company:</strong> {job['company']}</p>
            <p><strong>Location:</strong> {job['location']}</p>
            <p><strong>Type:</strong> {job['employment_type']}</p>
            <p><strong>Description:</strong> {job['description']}</p>
            <a href="{job['apply_link']}" target="_blank" class="btn">Apply Now</a>
        </div>
        """
    
    flask_code = f'''
from flask import Flask
import os

app = Flask(__name__)

@app.route('/callback')
def callback():
    return "ok", 200

@app.route('/healthz')
def healthz():
    return "ok", 200

@app.route('/')
def jobs():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Job Search Results</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                max-width: 1000px;
                margin: 0 auto;
                padding: 20px;
                background-color: #f5f5f5;
            }}
            h1 {{
                text-align: center;
                color: #333;
            }}
            .job-card {{
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 8px;
                padding: 20px;
                margin: 15px 0;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            .job-card h3 {{
                margin-top: 0;
                color: #2c3e50;
            }}
            .job-card p {{
                margin: 10px 0;
                color: #555;
            }}
            .job-card strong {{
                color: #333;
            }}
            .btn {{
                display: inline-block;
                padding: 10px 20px;
                background-color: #007bff;
                color: white;
                text-decoration: none;
                border-radius: 4px;
                margin-top: 10px;
                transition: background-color 0.3s;
            }}
            .btn:hover {{
                background-color: #0056b3;
            }}
        </style>
    </head>
    <body>
        <h1>🔍 Job Search Results</h1>
        {jobs_html}
    </body>
    </html>
    """

if __name__ == '__main__':
    port = int(os.environ.get('PORT', '3000'))
    app.run(host='0.0.0.0', port=port)
'''
    return flask_code


def run_job_search_sandbox(user_prompt: str):
    """Run job search in Daytona sandbox with web preview"""
    
    # Initialize Daytona
    daytona_api_key = os.getenv('DAYTONA_API_KEY')
    if not daytona_api_key:
        print("Error: DAYTONA_API_KEY environment variable not set")
        return
    
    daytona = Daytona(DaytonaConfig(api_key=daytona_api_key))
    
    # Create sandbox
    print("Creating Daytona sandbox...")
    sandbox = daytona.create()
    
    # Search for jobs
    print(f"Searching jobs for: {user_prompt}")
    searcher = JobSearcher()
    jobs = searcher.search_jobs(user_prompt, num_pages=1)
    
    if jobs:
        print(f"Found {len(jobs)} jobs!")
        
        # Create Flask app with results
        flask_code = create_flask_app(jobs)
        
        # Upload Flask app to sandbox
        print("Uploading Flask app to sandbox...")
        sandbox.fs.upload_file(flask_code.encode(), "app.py")
        
        # Create session and run Flask app
        print("Starting Flask app in sandbox...")
        exec_session_id = "job-search-session"
        sandbox.process.create_session(exec_session_id)
        
        # Ensure Flask is available in the sandbox using the interpreter that will execute the app
        install_cmds = [
            "python3 -m pip install --no-cache-dir flask",
            "python -m pip install --no-cache-dir flask",
            "pip3 install --no-cache-dir flask",
            "pip install --no-cache-dir flask",
        ]
        for cmd in install_cmds:
            try:
                resp = sandbox.process.execute_session_command(
                    exec_session_id,
                    SessionExecuteRequest(
                        command=cmd,
                        run_async=False
                    )
                )
                # Best-effort; stop trying if one succeeds
                break
            except Exception:
                continue

        # Verify the uploaded app exists and is readable
        try:
            sandbox.process.execute_session_command(
                exec_session_id,
                SessionExecuteRequest(
                    command="ls -l app.py || true",
                    run_async=False
                )
            )
        except Exception:
            pass

        # Print interpreter details for debugging
        try:
            sandbox.process.execute_session_command(
                exec_session_id,
                SessionExecuteRequest(
                    command="python3 -V || true; which python3 || true; python -V || true; which python || true",
                    run_async=False
                )
            )
        except Exception:
            pass

        # Start Flask app inside the session (keeps running via session)
        sandbox.process.execute_session_command(
            exec_session_id,
            SessionExecuteRequest(
                command="python3 app.py || python app.py",
                run_async=True
            )
        )
        
        # Get preview link
        preview_info = sandbox.get_preview_link(3000)
        terminal_info = None
        try:
            terminal_info = sandbox.get_preview_link(22222)
        except Exception:
            pass

        # Wait until the app is reachable
        url = preview_info.url
        health_url = url.rstrip('/') + '/callback'
        ready = False
        for _ in range(45):  # ~45s
            try:
                r = requests.get(health_url, timeout=2)
                if r.status_code == 200:
                    ready = True
                    break
            except Exception:
                pass
            time.sleep(1)

        # If not ready, try to show recent logs and running processes for debugging
        if not ready:
            try:
                sandbox.process.execute_session_command(
                    exec_session_id,
                    SessionExecuteRequest(
                        command="ps aux | grep -E 'python(3)? /app.py' | grep -v grep",
                        run_async=False
                    )
                )
            except Exception:
                pass
            try:
                sandbox.process.execute_session_command(
                    exec_session_id,
                    SessionExecuteRequest(
                        command="tail -n 200 /app.log || true",
                        run_async=False
                    )
                )
            except Exception:
                pass

        print(f"\n✅ Job search app is running!")
        print(f"Preview URL: {url}")
        if terminal_info:
            print(f"Terminal URL: {terminal_info.url}")
        print(f"Sandbox ID: {sandbox.id}")
        if not ready:
            print("Note: App is starting up; if you see 502, wait a few seconds and refresh.")
        
        return sandbox, url
    else:
        print("No jobs found for your search.")
        sandbox.delete()
        return None, None


def main():
    """Main entry point"""
    user_input = input("Enter your job search query (e.g., 'Remote Python developer in San Francisco'): ").strip()
    
    if user_input:
        sandbox, preview_url = run_job_search_sandbox(user_input)
        if sandbox:
            print("\nSandbox is running. Press Ctrl+C to stop and clean up.")
            try:
                import time
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\nCleaning up sandbox...")
                sandbox.delete()
                print("Done!")
    else:
        print("Please enter a valid job search query.")


if __name__ == "__main__":
    main()
