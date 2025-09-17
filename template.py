import os
from pathlib import Path

project_name = "src"

list_of_files = [

    f"{project_name}/__init__.py",
    f"{project_name}/components/__init__.py",
    f"{project_name}/components/add_doc_to_qdrant.py",  
    f"{project_name}/components/generate_message.py",
    f"{project_name}/components/get_graph.py",
    f"{project_name}/components/initialise_components.py",
    f"{project_name}/components/set_sidebar.py",
    f"{project_name}/exception/__init__.py",
    f"{project_name}/logger/__init__.py",
    f"{project_name}/pipline/__init__.py",
    f"{project_name}/pipline/pipeline.py",
    "app.py",
    "requirements.txt",
    "setup.py",
    "pyproject.toml",
]

for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)
    if filedir != "":
        os.makedirs(filedir,exist_ok=True)
    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, "w") as f:
            pass
    else:
        print(f"file is already present at : {filepath}")