import pandas as pd
import subprocess
import re

def fetch_project_and_workflow(job_id):
    try:
        result = subprocess.run(['td', 'job:show', str(job_id)], capture_output=True, text=True, check=True, shell=True)
        output = result.stdout

        project_match = re.search(r'-- project_name:\s*(.+)', output)
        workflow_match = re.search(r'-- workflow_name:\s*(.+)', output)

        if not project_match or not workflow_match:
            return "ad-hoc", "ad-hoc"
        else:
            return project_match.group(1).strip(), workflow_match.group(1).strip()

    except subprocess.CalledProcessError:
        return "ERROR", "ERROR"

def enrich_csv(input_csv, output_csv):
    df = pd.read_csv(input_csv)
    df['project_name'] = ''
    df['workflow_name'] = ''

    for idx, row in df.iterrows():
        job_id = row['job_id']
        print(f"🔄 Processando job_id {job_id}...")
        project_name, workflow_name = fetch_project_and_workflow(job_id)
        df.at[idx, 'project_name'] = project_name
        df.at[idx, 'workflow_name'] = workflow_name

    df.to_csv(output_csv, index=False)
    print(f"✅ CSV salvo em: {output_csv}")

if __name__ == "__main__":
    enrich_csv("input/input_jobs.csv", "output/enriched_jobs_metadata.csv")
