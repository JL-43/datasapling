from faker import Faker
import yaml
import os
from datetime import datetime
import pandas as pd

class DataGenerator:
  def __init__(self, config_path="config/config.yml"):
    self.fake = Faker()
    self.config = self._load_config(config_path)

    global_config = self.config.get('global', {})
    self.global_metadata = global_config.get('metadata', {})
    self.global_output = global_config.get('output', {})
      
  def _load_config(self, config_path):
    if not os.path.exists(config_path):
      return {}
    with open(config_path, 'r') as f:
      return yaml.safe_load(f)
    
  def generate(self):
      for dataset_name, dataset_config in self.config.get('datasets', {}).items():
        data = {}
        num_rows = dataset_config.get('rows', 100) # defaults 100 rows of data if not specified

        metadata_config = self._merge_configs(self.global_metadata, dataset_config.get('metadata', {}))
        output_config = self._merge_configs(self.global_output, dataset_config.get('output', {}))

        for field in dataset_config.get('fields', []):
          field_name = field['name']
          faker_method_name = field['type']
          faker_method = getattr(self.fake, faker_method_name)
          data[field_name] = [faker_method() for _ in range(num_rows)]
        
        if metadata_config.get('enable', False):
          for metadata_field in metadata_config.get('fields', []):
            if metadata_field == 'created_at' or metadata_field == 'modified_at':
              data[metadata_field] = [datetime.now() for _ in range(num_rows)]
            elif metadata_field == 'created_by' or metadata_field == 'modified_by':
              data[metadata_field] = [self.fake.name() for _ in range(num_rows)]

        df = pd.DataFrame(data)
        print(f"Generated {num_rows} rows for dataset '{dataset_name}'")
        print(df.head(10)) 

        output_directory = output_config.get('directory', 'output/')
        os.makedirs(output_directory, exist_ok=True)

        output_format = output_config.get('format', 'csv')
        output_file = os.path.join(output_directory, f"{dataset_name}.{output_format}")

        if output_format == 'csv':
          df.to_csv(output_file, index=False)
        elif output_format == 'tsv':
          df.to_csv(output_file, sep='\t', index=False)
        else:
          print(f"Unsupported output format: {output_format}")

  def _merge_configs(self, global_config, dataset_config):
    """Utility method to merge global and dataset-specific configurations."""
    merged_config = global_config.copy()
    merged_config.update(dataset_config)
    return merged_config

if __name__ == "__main__":
  generator = DataGenerator()
  generator.generate()