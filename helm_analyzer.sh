#!/bin/bash

set -e

RELEASE_NAME=$1
CHART_PATH=$2
shift 2
FILTER_RESOURCES=("$@")

# Output folder
OUTPUT_DIR="./output"
rm -rf "$OUTPUT_DIR"
mkdir -p "$OUTPUT_DIR"

# Temp file to hold manifest
MANIFEST_FILE=$(mktemp)

# Run helm dry-run and capture manifest
helm install "$RELEASE_NAME" "$CHART_PATH" --dry-run --debug > "$MANIFEST_FILE"

# Extract rendered manifests from helm output
START_LINE=$(grep -n "^---$" "$MANIFEST_FILE" | head -n 1 | cut -d: -f1)
tail -n +"$START_LINE" "$MANIFEST_FILE" > "$MANIFEST_FILE.rendered"

# Split YAML docs
csplit -s -f manifest- "$MANIFEST_FILE.rendered" "/^---$/" {*}

# Process each manifest
for f in manifest-*; do
    # Get Kind and Name
    KIND=$(yq e '.kind' "$f")
    NAME=$(yq e '.metadata.name' "$f")

    # Skip empty docs or docs without kind
    if [[ "$KIND" == "null" || -z "$KIND" || -z "$NAME" ]]; then
        continue
    fi

    # If filter is specified, skip unlisted kinds
    if [[ ${#FILTER_RESOURCES[@]} -gt 0 ]]; then
        MATCH=false
        for r in "${FILTER_RESOURCES[@]}"; do
            if [[ "${KIND,,}" == "${r,,}" ]]; then
                MATCH=true
                break
            fi
        done
        if [[ "$MATCH" == false ]]; then
            continue
        fi
    fi

    KIND_DIR="$OUTPUT_DIR/$KIND"
    mkdir -p "$KIND_DIR"
    cp "$f" "$KIND_DIR/$NAME.yaml"
done

# Clean up
rm -f manifest-* "$MANIFEST_FILE" "$MANIFEST_FILE.rendered"

echo "Resources exported to $OUTPUT_DIR"
