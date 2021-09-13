import numpy
import os
import pandas as pd
from glob import glob

configfile: 'config.yaml'

FOLDER = os.path.abspath('.')
PUBLIS = {row["Key"]: row["Title"] for id, row in list(pd.read_csv(config["INPUT_FILE"]).iterrows())}

rule all:
    input: config["OUTPUT_FILE"]

rule scrape:
    input:
        script='scholarly_scraper.py',
    output:
        name="tmp/{id}.csv",
    params:
        search=lambda w: '--search "{0}" --api_key {1}'.format(PUBLIS[w.id], config["SCRAPER_API_KEY"])
    shell:
        'python3 {input.script} {params.search} --name {output.name}'

rule intersect:
    input:
        script='intersect.py',
        cites=expand("tmp/{id}.csv", id=list(PUBLIS.keys()))
    output:
        file=config["OUTPUT_FILE"]
    shell:
        'python3 {input.script} --input {input.cites} --output {output.file}'
