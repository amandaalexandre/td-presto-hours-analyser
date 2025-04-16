import os
import re
import pandas as pd

# Caminho da pasta onde estão os arquivos
JOBS_DIR = "jobs"
OUTPUT_CSV = "output/extracted_job_metadata.csv"

def extract_metadata_from_text_file(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()

        job_id = os.path.splitext(os.path.basename(filepath))[0]

        # Se a linha 11 começar com o padrão de CDP Audience
        if len(lines) >= 11 and lines[10].startswith("Query       : -- CDP: Audience"):
            return {"job_id": job_id, "project_name": "cdp_audience", "workflow_name": "cdp_audience"}

        # Junta o texto para extrair os campos
        full_text = "".join(lines)

        project_match = re.search(r'-- project_name:\s*(.+)', full_text)
        workflow_match = re.search(r'-- workflow_name:\s*(.+)', full_text)

        project_name = project_match.group(1).strip() if project_match else "ad-hoc"
        workflow_name = workflow_match.group(1).strip() if workflow_match else "ad-hoc"

        return {"job_id": job_id, "project_name": project_name, "workflow_name": workflow_name}

    except Exception as e:
        return {"job_id": job_id, "project_name": "ERROR", "workflow_name": "ERROR"}

def main():
    results = []

    if not os.path.exists(JOBS_DIR):
        print(f"❌ Pasta '{JOBS_DIR}' não encontrada.")
        return

    print(f"🔍 Processando arquivos da pasta: {JOBS_DIR}")
    for filename in os.listdir(JOBS_DIR):
        if filename.endswith(".json"):  # mesmo não sendo JSON real
            filepath = os.path.join(JOBS_DIR, filename)
            metadata = extract_metadata_from_text_file(filepath)
            results.append(metadata)

    if results:
        df = pd.DataFrame(results)
        df.to_csv(OUTPUT_CSV, index=False)
        print(f"✅ Arquivo salvo como: {OUTPUT_CSV}")
    else:
        print("⚠️ Nenhum arquivo processado.")

if __name__ == "__main__":
    main()