#!/bin/bash

PROJECT_NAME="trusted-social"
D_FLAG=0
PROBE_FLAG=0

stop_docker() {
    docker compose stop
}

ACTION="${1:-start}"
shift || true

if [ "$ACTION" != "build" ] && [ "$ACTION" != "stop" ] && [ "$ACTION" != "start" ]; then
    echo "Error: first argument must be 'build', 'start', or 'stop'"
    echo "Usage: $0 [build|- start|- stop] [-p] [-lang] [-d] [-probe]"
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
        -probe)
            PROBE_FLAG=1
            shift
            ;;
        *)
            echo "Unknown option: $1"
            echo "Usage: $0 [build|- start|- stop] [-p] [-lang] [-d] [-probe]"
            exit 1
            ;;
    esac
done

stop_docker

if [ "$ACTION" = "stop" ]; then
    echo "social service stopped"
elif [ "$ACTION" = "build" ]; then
    docker compose -p "$PROJECT_NAME" build
    docker compose -p "$PROJECT_NAME" up
    echo "social service started"
    if [ "$PROBE_FLAG" -eq 1 ]; then
        .venv/bin/python -m app.probe.recon_probe.test_recon_probe
    fi
else
    docker compose -p "$PROJECT_NAME" up
    echo "social service started"
fi
