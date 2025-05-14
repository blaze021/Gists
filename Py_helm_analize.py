# pip install pyyaml

import os
import yaml
from pathlib import Path
from subprocess import check_output

# Config
helm_release_name = "sample-app-dev"
output_base = Path("resources")
kind_map = {
    "Deployment": "deployment",
    "Service": "svc"
}

# Helper: Render HelmRelease using flux
def render_helmrelease(name):
    print(f"Rendering HelmRelease: {name}")
    output = check_output([
        "flux", "build", "hr", name,
        "--kustomization", "default"  # Change as needed
    ])
    return output.decode()

# Helper: Save each resource as individual file
def save_resources(resources):
    for res in resources:
        if not res or "kind" not in res or "metadata" not in res:
            continue

        kind = res["kind"]
        name = res["metadata"].get("name", "unnamed")
        folder_name = kind_map.get(kind, "others")

        folder_path = output_base / folder_name
        folder_path.mkdir(parents=True, exist_ok=True)

        filename = f"{name}_{kind}.yaml"
        file_path = folder_path / filename

        with open(file_path, "w") as f:
            yaml.dump(res, f, sort_keys=False)
        print(f"Saved: {file_path}")

# Main execution
if __name__ == "__main__":
    yaml_text = render_helmrelease(helm_release_name)
    resources = list(yaml.safe_load_all(yaml_text))
    save_resources(resources)
