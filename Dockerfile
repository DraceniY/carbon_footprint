# Import Docker container based on a minimal Ubuntu installation that includes conda-forge's
FROM docker.io/condaforge/miniforge3:latest

RUN apt-get update && apt-get install -y wget && apt-get clean && rm -rf /var/lib/apt/lists/*

# Clone clinshot repository
COPY . /

# Create the environment for packages
RUN conda env create -f environment_footprint.yml
SHELL ["/bin/bash", "-c"]
RUN conda init bash
RUN conda activate footprint_env
SHELL ["cd", "src"]
ENTRYPOINT ["python", "main.py"] 