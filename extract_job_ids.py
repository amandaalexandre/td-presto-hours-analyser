import pandas as pd

# Caminho do arquivo CSV enviado anteriormente
csv_path = "input/input_jobs.csv"

# Lê os job_ids da coluna correspondente
df = pd.read_csv(csv_path)
job_ids = df["job_id"].dropna().astype(int).tolist()

# Gera o conteúdo de um arquivo de texto com todos os job_ids, um por linha
job_ids_txt_path = "output/job_ids.txt"
with open(job_ids_txt_path, "w") as f:
    for job_id in job_ids:
        f.write(f"{job_id}\n")

job_ids_txt_path
