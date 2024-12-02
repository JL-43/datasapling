# Data Sapling

## Objectives

- Set up a portable local environment that can be easily deployed on various devices.
- Generate fake data using Faker, configurable via a configuration file.
- Include optional metadata fields (e.g., `created_by`, `modified_by`) with the ability to enable or disable them.
- Manipulate data using SQL, preferring DuckDB or SparkSQL dialects.
- Simulate real pipeline data sources. Some sources giving data meant for incremental load, some sources giving data for full load. With the ability to target where these data sources are dropped into.
- Simulate data endpoints in various formats (simple CSV/TSV, mock API, mock database connection). 
  - For the first draft, focus on creating a CSV/TSV endpoint.

### Objective 1: Set Up a Portable Local Environment

To ensure portability and ease of deployment across various devices, we'll use Docker to containerize the environment. This allows you to run the same setup anywhere Docker is installed.

#### Steps:

1. **Install Docker:**
   - Download and install Docker Desktop from Docker's official website.

2. **Create a Project Directory:**
   - Create a new directory for your project, e.g., `fake-data-generator`.

3. **Initialize a Dockerfile:**
   - Inside your project directory, create a Dockerfile to define your environment.

#### Dockerfile Example:

```dockerfile
# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt ./

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the working directory contents into the container
COPY . .

# Set the command to run the script when the container starts
CMD [ "python", "./main.py" ]
```

4. **Define Python Dependencies:**
   - Create a `requirements.txt` file to list your Python dependencies.

#### `requirements.txt` Example:

```bash
faker
duckdb
pandas
pyyaml  # For configuration file parsing
```

5. **Set Up Version Control (Optional):**
   - Initialize a Git repository to track your changes, which can help when deploying to different devices.

---

### Objective 2: Generate Fake Data Using Faker Configurable via a Configuration File

We'll use a YAML configuration file to define the schema and parameters for the fake data generation.

#### Steps:

1. **Create a Configuration File:**
   - Create a `config.yaml` file to define your data schema.

#### `config.yaml` Example:

```yaml
# config.yaml
tables:
  users:
    rows: 1000
    columns:
      - name: id
        type: integer
        faker: random_number
      - name: name
        type: string
        faker: name
      - name: email
        type: string
        faker: email
      - name: created_at
        type: datetime
        faker: date_time_between
        parameters:
          start_date: '-1y'
          end_date: 'now'
metadata:
  include_created_by: true
  include_modified_by: false
```

2. **Write the Data Generation Script (`main.py`):**

```python
import yaml
from faker import Faker
import pandas as pd
import duckdb
import argparse

def load_config(config_file):
    with open(config_file, 'r') as f:
        return yaml.safe_load(f)

def generate_data(table_config, metadata_options):
    faker = Faker()
    data = {}
    num_rows = table_config['rows']
    for column in table_config['columns']:
        faker_method = getattr(faker, column['faker'])
        params = column.get('parameters', {})
        data[column['name']] = [faker_method(**params) for _ in range(num_rows)]
    
    df = pd.DataFrame(data)

    # Add metadata columns if enabled
    if metadata_options.get('include_created_by'):
        df['created_by'] = faker.name()
    if metadata_options.get('include_modified_by'):
        df['modified_by'] = faker.name()
    
    return df

def main(config_file):
    config = load_config(config_file)
    tables = config['tables']
    metadata_options = config.get('metadata', {})
    
    conn = duckdb.connect(database=':memory:')
    
    for table_name, table_config in tables.items():
        df = generate_data(table_config, metadata_options)
        conn.execute(f"CREATE TABLE {table_name} AS SELECT * FROM df")
        print(f"Table {table_name} created with {len(df)} rows.")
    
    # Example query
    result = conn.execute("SELECT * FROM users LIMIT 5").fetchdf()
    print(result)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Fake Data Generator')
    parser.add_argument('--config', type=str, default='config.yaml', help='Path to the configuration file.')
    args = parser.parse_args()
    main(args.config)
```

3. **Update Dockerfile to Copy `config.yaml`:**

```dockerfile
# Copy the configuration file
COPY config.yaml ./
```

---

### Objective 3: Include Optional Metadata Fields

We've already included metadata options in the `config.yaml` and modified the `generate_data` function to add these fields based on the configuration.

---

### Objective 4: Manipulate Data Using SQL (DuckDB)

We're using DuckDB in-memory to allow SQL operations on the generated data.

#### Steps:

1. **Connect to DuckDB and Create Tables:**
   - In the `main.py`, after data generation, we connect to DuckDB and create tables.

2. **Run SQL Queries:**
   - We can execute SQL queries using DuckDB's Python API.

#### Example Query in `main.py`:

```python
# Example query to fetch data
result = conn.execute("SELECT * FROM users WHERE created_by = 'John Doe'").fetchdf()
print(result)
```

---

### Objective 5: Simulate Data Endpoints in Various Formats

Instead of directly creating source tables in DuckDB, we'll simulate data endpoints by generating data in formats like CSV/TSV files, mock APIs, or mock database connections. For the first draft, we'll focus on creating CSV/TSV endpoints.

This approach more closely aligns with real-world scenarios where data is received from various sources before being loaded into a database.

#### Steps:
1. Modify the Data Generation Script to Output CSV/TSV Files
- Update main.py to save the generated data as CSV or TSV files instead of loading it directly into DuckDB.
- Add command-line arguments to specify the output format and directory.
- Organize the output files to simulate different data sources and load types (full and incremental).

2. Simulate Incremental and Full Loads
- Implement logic to generate datasets representing both full and incremental loads.
- Output files will be named and stored in a way that reflects their load type.

3. Update the Dockerfile
- Adjust the Dockerfile to ensure that the generated data files are accessible outside the Docker container.
- Map a volume for the output directory.

4. Process the Data
- Create a separate script to load the generated CSV/TSV files into DuckDB or another database.
- This simulates the data ingestion step of your pipeline.
