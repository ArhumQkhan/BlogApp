#!/bin/sh
# wait-for-rds.sh
# Usage: ./wait-for-rds.sh <host> <port> <command_to_run>

set -e

host="$1"
port="$2"
shift 2  # remove host and port from arguments
cmd="$@"

echo "Waiting for RDS at $host:$port ..."

# Loop until the database port is open
until nc -z "$host" "$port"; do
  echo "RDS is unavailable - sleeping 5s"
  sleep 5
done

echo "RDS is up - running command: $cmd"
exec $cmd
