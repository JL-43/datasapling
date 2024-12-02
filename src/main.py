from faker import Faker
import yaml
import os
from datetime import datetime

class DataGenerator:
  def __init__(self, config_path="config/config.yml"):
      self.fake = Faker()
      self.config = self._load_config(config_path)
    
  def _load_config(self, config_path):
    if not os.path.exists(config_path):
      return {}
    with open(config_path, 'r') as f:
      return yaml.safe_load(f)
  
  def generate(self):
    print(Faker)
    print(yaml)
    print(os)
    pass

if __name__ == "__main__":
    generator = DataGenerator()
    generator.generate()