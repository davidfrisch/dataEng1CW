#!/usr/bin/env bash
SPARK_HOME="/Users/david/development/ucl/DataEng1/coursework/code/venv/bin/pyspark"
HOSTNAME="localhost"
PORT = 7077
WEBUI_PORT = 8080

# Check if SPARK_HOME is set
if [ -z "$SPARK_HOME" ]; then
  echo "Error: SPARK_HOME is not set."
  exit 1
fi

# Set the Spark master URL (e.g., spark://hostname:7077)
MASTER_URL=spark://$HOSTNAME:$PORT

# Start the Spark master
$SPARK_HOME/sbin/start-master.sh --host $HOSTNAME --port $PORT --webui-port $WEBUI_PORT

# Print the Spark master URL
echo "Spark master started at $MASTER_URL"