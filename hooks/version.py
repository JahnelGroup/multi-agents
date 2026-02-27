from pathlib import Path


def on_config(config):
    version_file = Path(config["docs_dir"]).parent / "VERSION"
    if version_file.exists():
        version = version_file.read_text().strip()
        config["extra"]["version"] = version
        config["copyright"] = f"v{version}"
    return config
