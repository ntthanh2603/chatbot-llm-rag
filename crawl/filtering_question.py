import json

def filter_json_data(json_data):
    """
    Filter JSON data to keep only entries where 'keep' is True
    
    Args:
        json_data (list): List of dictionaries containing the JSON data
        
    Returns:
        list: Filtered list with only entries where 'keep' is True
    """
    filtered_data = [item for item in json_data if item.get('keep') is True]
    return filtered_data

def process_json_file(input_file, output_file):
    """
    Process a JSON file to remove entries where 'keep' is False
    
    Args:
        input_file (str): Path to the input JSON file
        output_file (str): Path to save the filtered JSON
    """
    try:
        # Read the input JSON file
        with open(input_file, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
        
        # Filter the data
        filtered_data = filter_json_data(json_data)
        
        # Write the filtered data to the output file
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(filtered_data, f, ensure_ascii=False, indent=2)
            
        print(f"Filtered JSON successfully saved to {output_file}")
        print(f"Removed {len(json_data) - len(filtered_data)} entries, kept {len(filtered_data)} entries")
        
    except Exception as e:
        print(f"Error processing JSON file: {e}")

# Example usage
if __name__ == "__main__":
    input_file = "demo_wiki_questions.json"  # Replace with your input file path
    output_file = "demo_wiki_questions.json"  # Replace with your desired output file path
    
    process_json_file(input_file, output_file)