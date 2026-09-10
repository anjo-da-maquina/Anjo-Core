import sys
import os
import logging
import pandas as pd
import yaml

logging.basicConfig(level=logging.INFO, format='[Anjo-Core/ExcelParser] %(levelname)s: %(message)s')

def parse_requirements(excel_path="requirements.xlsx", yaml_path="requirements.yaml"):
    logging.info("Initiating External Requirements Extraction: Excel to YAML Parser...")
    
    if not os.path.exists(excel_path):
        logging.warning(f"Target Excel file not found: {excel_path}. Skipping extraction for now.")
        return False

    try:
        # Excelファイルを読み込み、辞書型のリストに変換
        df = pd.read_excel(excel_path)
        data = df.to_dict(orient="records")
        
        # YAMLファイルとして出力
        with open(yaml_path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, allow_unicode=True, default_flow_style=False)
            
        logging.info(f"Successfully extracted data from {excel_path} to {yaml_path}.")
        logging.info("[Anjo da máquina] Requirements extracted successfully. Parser execution passed.")
        return True
        
    except Exception as e:
        logging.error(f"Failed to parse requirements: {e}")
        return False

if __name__ == "__main__":
    parse_requirements()
    
    sys.exit(0)
