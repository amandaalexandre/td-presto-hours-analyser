# td-presto-hours-analyser
This script reads a list of Treasure Data job IDs from a CSV file, gets workflow and project details about each job and outputs it into another CSV file.

## 1. Extract job IDs from CSV file
Run 
``` python .\extract_job_ids.py ```

Edit the csv_path variable with the input file given by Treasure Data.

## 2. Run API calls per each job_id in the job_ids.txt file
```for id in $(cat job_ids.txt); do td job:show $id -x --format json > jobs/$id.json; done```

The -x option exists to not output the job result - it takes too long.

## 3. Extract the project name and workflow_name in the job results
If they don't find anything, it files the job as "ad-hoc".
If they find the query starts with -- CDP: Audience, it flags the process as an MS build.

Run 
``` python .\extract_job_metadata.py ```