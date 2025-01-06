import os
import sys
import subprocess
import json

def sign_in():
    result = subprocess.run(["op", "whoami"])
    if result.returncode != 0:
        sign_in_result = subprocess.run(["op", "signin"])
        if sign_in_result.returncode != 0:
            print("Not logged in")
            sys.exit(1)

def sign_out():
    subprocess.run(["op", "signout"])

def get_vaults():
    result = subprocess.run(["op", "vault", "list", "--format=json"], capture_output=True)
    if result.returncode != 0:
        return RuntimeError("Command failed")
    return json.loads(result.stdout.decode("utf-8"))

def get_vault_json(vault_id):
    result = subprocess.run(["op", "vault", "get", vault_id, "--format=json"], capture_output=True)
    if result.returncode != 0:
        return RuntimeError("Command failed")
    return result.stdout.decode("utf-8")

def get_items(vault_id):
    result = subprocess.run(["op", "item", "list", "--vault", vault_id, "--format=json"], capture_output=True)
    if result.returncode != 0:
        return RuntimeError("Command failed")
    return json.loads(result.stdout.decode("utf-8"))

def get_item_json(item_id):
    result = subprocess.run(["op", "item", "get", item_id, "--format=json", "--reveal"], capture_output=True)
    if result.returncode != 0:
        return RuntimeError("Command failed")
    return result.stdout.decode("utf-8")

def get_documents(vault_id):
    result = subprocess.run(["op", "document", "list", "--vault", vault_id, "--format=json"], capture_output=True)
    if result.returncode != 0:
        return RuntimeError("Command failed")
    return json.loads(result.stdout.decode("utf-8"))

def save_document(document_id, path):
    result = subprocess.run(["op", "document", "get", document_id, "-o", path])
    if result.returncode != 0:
        return RuntimeError("Command failed")

def get_export_vault():
    if len(sys.argv) >= 3:
        return sys.argv[2]
    return

# Main

if len(sys.argv) < 2 or len(sys.argv) > 3:
    print("Usage: " + sys.argv[0] + " <export path> [vault]")
    sys.exit(0)

export_dir = sys.argv[1]
export_vault = get_export_vault()

if os.path.exists(export_dir):
    print("Export folder '" + export_dir + "' already exists")
    sys.exit(1)
os.makedirs(export_dir)

if export_vault:
    print("Exporting vault " + export_vault + " to " + export_dir)
else:
    print("Exporting to " + export_dir)

sign_in()

for vault in get_vaults():
    if export_vault and vault["name"] != export_vault:
        continue
    vault_folder = os.path.join(export_dir, vault["name"])
    os.makedirs(vault_folder)
    vault_items_folder = os.path.join(vault_folder, "items")
    os.makedirs(vault_items_folder)
    vault_documents_folder = os.path.join(vault_folder, "documents")
    os.makedirs(vault_documents_folder)
    vault_file = open(os.path.join(vault_folder, "vault.json"), "w")
    vault_file.write(get_vault_json(vault["id"]))
    vault_file.close()

    items_index_file = open(os.path.join(vault_folder, "index_items.txt"), "w")
    print("Exporting " + str(vault["items"]) + " items from vault '" + vault["name"] + "'")
    for item in get_items(vault["id"]):
        items_index_file.write(item["id"] + "\t" + item["title"] + "\t" + item["category"] + "\n")
        item_file = open(os.path.join(vault_items_folder, item["id"] + ".json"), "w")
        item_file.write(get_item_json(item["id"]))
        item_file.close()
    items_index_file.close()

    documents_index_file = open(os.path.join(vault_folder, "index_documents.txt"), "w")
    documents = get_documents(vault["id"])
    print("Exporting " + str(len(documents)) + " documents from vault '" + vault["name"] + "'")
    for document in documents:
        documents_index_file.write(document["id"] + "\t" + document["title"] + "\n")
        save_document(document["id"], os.path.join(vault_documents_folder, document["id"] + ".bin"))
    documents_index_file.close()

print("Completed")
sign_out()
