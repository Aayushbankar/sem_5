import re
with open('Case_Study_Digital_Rupee_CBDC.md','r') as f:
    content=f.read()
new_content=re.sub(r'```mermaid\n.*?\n```', r'![Architecture Diagram](mermaid_diagram.png)', content, flags=re.DOTALL, count=1)
with open('Case_Study_Digital_Rupee_CBDC_processed.md','w') as f:
    f.write(new_content)
print('Done')