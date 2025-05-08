# Tracker simulation

This project simulates tracker.

## Prerequisites

- Kafka
- Python 3.x
- Required Python packages (see `requirements.txt`)

## Setup Instructions

### 1. Setup Kafka

First, navigate to the project folder and run the setup script:
```bash
bash scripts/setup.sh
````

Afterward, source your `.bashrc` to apply environment changes:

```bash
source ~/.bashrc
```

### 2. Create Kafka Topic

Next, create the necessary Kafka topic:

```bash
bash scripts/create_topic.sh
```

### 3. Start Kafka

To start Kafka, use the following command:

```bash
bash scripts/start_kafka.sh
```

### 4. Install Python Dependencies

Ensure all the required Python packages are installed:

```bash
pip install -r requirements.txt
```

### 5. Run

Run producer.py and consumer.py.

## Stop and clear topic's message

To stop run:
```bash
bash scripts/stop_kafka.sh
```

To clear topic's message run:
```bash
bash scripts/clear_topics.sh
```

