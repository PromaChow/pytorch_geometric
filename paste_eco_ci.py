import sys
import os

def modify_github_action_yaml(file_path):
    header_snippet = """
      - name: Start Energy Measurement
        uses: green-coding-solutions/eco-ci-energy-estimation@v4
        with:
          task: start-measurement
"""
    
    footer_snippet = """
      - name: Display Energy Results
        uses: green-coding-solutions/eco-ci-energy-estimation@v4
        with:
          task: display-results
          json-output: true

      - name: Convert JSON to CSV
        if: always()
        run: |
          if [ -f /tmp/eco-ci/total-data.json ]; then
            jq -r '(.[0] | keys_unsorted) as $keys | $keys, map([.[ $keys[] ]])[] | @csv' /tmp/eco-ci/total-data.json > eco_results.csv
          else
            echo "No JSON output found, skipping conversion."
          fi
"""
    
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
        
        jobs_index = next((i for i, line in enumerate(lines) if line.strip().startswith("jobs:")), None)
        steps_index = next((i for i, line in enumerate(lines) if line.strip().startswith("steps:")), None)
        
        if jobs_index is None or steps_index is None:
            print(f"Skipping {file_path}, no valid jobs or steps section found.")
            return
        
        # Insert the header snippet after 'steps:'
        if header_snippet.strip() not in ''.join(lines):
            lines.insert(steps_index + 1, header_snippet)
        
        # Append the footer snippet before the last job step
        if footer_snippet.strip() not in ''.join(lines):
            lines.append(footer_snippet)
        
        with open(file_path, 'w') as file:
            file.writelines(lines)
        
        print(f"Updated: {file_path}")
    except Exception as e:
        print(f"Error modifying {file_path}: {e}")

def process_all_yaml_files(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".yml") or file.endswith(".yaml"):
                modify_github_action_yaml(os.path.join(root, file))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <directory>")
        sys.exit(1)
    
    directory = sys.argv[1]
    process_all_yaml_files(directory)
