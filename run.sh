#!/bin/bash

PROJECT_NAME="trusted-micros"
LANG_FLAG=0
D_FLAG=0

download_and_extract_model() {
    MODEL_URL="https://drive.usercontent.google.com/download?id=1r3hbTyLUemywwgsSkyonCOuY0fCYO2aW&export=download&authuser=0&confirm=t&uuid=70eb0256-8f74-44ac-b0e3-139c3362b17d&at=APcmpoxkYTa5yExi8JwRacxpvqtP%3A1744468036685"
    MODEL_DEST_DIR="app/raw/model"
    MODEL_DEST_FILE="$MODEL_DEST_DIR/ml_classifier.zip"
    MODEL_EXTRACTED_DIR="$MODEL_DEST_DIR/saved_model"
    mkdir -p "$MODEL_DEST_DIR"
    [ -d "$MODEL_EXTRACTED_DIR" ] && return
    for attempt in 1 2; do
        [ "$attempt" -eq 2 ] && rm -f "$MODEL_DEST_FILE"
        [ ! -f "$MODEL_DEST_FILE" ] && curl -# -L "$MODEL_URL" -o "$MODEL_DEST_FILE"
        if unzip -o "$MODEL_DEST_FILE" -d "$MODEL_DEST_DIR"; then
            return
        fi
        [ "$attempt" -eq 2 ] && exit 1
    done
}

model_initializer() {
    RAW_DIR="app/raw/translation"
    MODEL_ZIP_NAME="languages.zip"
    MODEL_URL="https://drive.usercontent.google.com/download?id=1hC9CutkBlOr6qmvlvrMuJFkYmg6dX2IF&export=download&authuser=0&confirm=t&uuid=32fa2b5d-456e-4d0e-abda-23d806383cbb&at=ALoNOgk2BeuMNXLF3O49TWh3awLX%3A1747840669375"
    REQUIRED_LANGS=("translate-ar_en-1_0" "translate-ru_en-1_9" "translate-zh_en-1_9")
    for lang_dir in "${REQUIRED_LANGS[@]}"; do
        if [ ! -d "$RAW_DIR/$lang_dir" ]; then
            break
        fi
        if [ "$lang_dir" == "${REQUIRED_LANGS[-1]}" ]; then
            return
        fi
    done
    rm -rf "$RAW_DIR"
    mkdir -p "$RAW_DIR"
    ZIP_PATH="$RAW_DIR/$MODEL_ZIP_NAME"
    curl -L -o "$ZIP_PATH" "$MODEL_URL"
    unzip "$ZIP_PATH" -d "$RAW_DIR"
    rm "$ZIP_PATH"
}

download_semantic_model() {
    MODEL_DEST_DIR="app/raw/model/semantic"
    MARKER_FILE="$MODEL_DEST_DIR/.done"
    [ -f "$MARKER_FILE" ] && return

    mkdir -p "$MODEL_DEST_DIR"
    python3 -m venv venv || true
    . venv/bin/activate

    pip install --upgrade pip sentence-transformers transformers torch

    python3 - <<'PY'
from sentence_transformers import SentenceTransformer
model = SentenceTransformer("BAAI/bge-small-en-v1.5")
model.save("app/raw/model/semantic")
PY

    touch "$MARKER_FILE"
}

stop_docker() {
    docker compose stop
}

ACTION="${1:-start}"
shift || true

if [ "$ACTION" != "build" ] && [ "$ACTION" != "stop" ] && [ "$ACTION" != "start" ]; then
    echo "Error: first argument must be 'build', 'start', or 'stop'"
    echo "Usage: $0 [build|- start|- stop] [-p] [-lang] [-d]"
    exit 1
fi

while [ $# -gt 0 ]; do
    case "$1" in
        -p)
            LANG_FLAG=1
            shift
            ;;
        -lang)
            LANG_FLAG=1
            shift
            ;;
        -d)
            D_FLAG=1
            shift
            ;;
        *)
            echo "Unknown option: $1"
            echo "Usage: $0 [build|- start|- stop] [-p] [-lang] [-d]"
            exit 1
            ;;
    esac
done

stop_docker

if [ "$ACTION" = "stop" ]; then
    echo "crawler service stopped"
elif [ "$ACTION" = "build" ]; then
    download_and_extract_model
    download_semantic_model
    if [ $LANG_FLAG -eq 1 ] && [ $D_FLAG -eq 0 ]; then
        model_initializer
    fi
    docker compose -p "$PROJECT_NAME" build
    docker compose -p "$PROJECT_NAME" up -d
    echo "crawler service started"
else
    docker compose -p "$PROJECT_NAME" up -d
    echo "crawler service started"
fi
