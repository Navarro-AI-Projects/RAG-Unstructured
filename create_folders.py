import os

def create_directories():
    documents_index_path = os.path.join(os.path.expanduser("~"), "documents_index")
    local_qdrant_path = os.path.join(os.path.expanduser("~"), "local_qdrant")

    if not os.path.exists(documents_index_path):
        os.makedirs(documents_index_path)
    if not os.path.exists(local_qdrant_path):
        os.makedirs(local_qdrant_path)

    return documents_index_path, local_qdrant_path
 
def create_env_file():
    # Get the parent directory of the current script
    parent_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

    env_file_path = os.path.join(parent_dir, ".env")

    if not os.path.exists(env_file_path):
        with open(env_file_path, 'w') as f:
            pass

    return env_file_path
