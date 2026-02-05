#!/bin/bash

PROJECT_NAME="trusted-social"
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
    docker compose -p "$PROJECT_NAME" build
    docker compose -p "$PROJECT_NAME" up
    echo "crawler service started"
else
    docker compose -p "$PROJECT_NAME" up
    echo "crawler service started"
fi
