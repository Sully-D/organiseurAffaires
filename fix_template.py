import re

path = 'web/kanban/templates/kanban/activity_detail.html'
with open(path, 'r') as f:
    content = f.read()

# Fix split if tags. 
# Pattern: {% if ... [newline] ... %}
# Regex: \{% if [^%]*\n\s*%\}
# We want to replace newline+whitespace with space

def replacer(match):
    return match.group(0).replace('\n', ' ').replace('  ', ' ')

new_content = re.sub(r'\{% if [^%]*\n\s*%\}', replacer, content)

# Also fix the weird case on line 61/62 if exists
# 61: ... {% endif
# 62: %}
new_content = re.sub(r'\{% endif\s*\n\s*%\}', '{% endif %}', new_content)

# General join for split tag closings
new_content = re.sub(r'(user\.is_superuser)\s*\n\s*%\}', r'\1 %}', new_content)

if content == new_content:
    print("No changes made by regex.")
else:
    with open(path, 'w') as f:
        f.write(new_content)
    print("File updated.")

