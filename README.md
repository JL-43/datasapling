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

---

### Objective 2: Generate Fake Data Using Faker Configurable via a Configuration File

We'll use a YAML configuration file to define the schema and parameters for the fake data generation.

---

### Objective 3: Include Optional Metadata Fields

We've already included metadata options in the `config.yml` and modified the `generate_data` function to add these fields based on the configuration.

---

### Objective 4: Simulate Data Endpoints in Various Formats

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

---

### Objective 5: Manipulate Data Using SQL (DuckDB)

We're using DuckDB in-memory to allow SQL operations on the generated dat

#### Example Query in `main.py`:

```python
# Example query to fetch data
result = conn.execute("SELECT * FROM users WHERE created_by = 'John Doe'").fetchdf()
print(result)
```