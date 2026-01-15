
import re

file_path = '/home/sully-pro/Programmation/Python/organiseurAffaires/web/kanban/templates/kanban/activity_detail.html'

with open(file_path, 'r') as f:
    content = f.read()

# Fix split tags where {% is on one line and the rest is on the next
# 150: ... {%
# 151: endif %}
content = re.sub(r'({%)\n\s*(endif %})', r'\1 \2', content)

# Check specifically for the split found line 150
content = content.replace('style="cursor: pointer;" {%\n                                endif %}', 'style="cursor: pointer;" {% endif %}')
content = content.replace('style="cursor: pointer;" {%\n                                endif %}', 'style="cursor: pointer;" {% endif %}')

# Generalize: Fix any tag start {% followed by newline
# Matches {% \n  keyword ... %}
content = re.sub(r'({%)\n\s*([^%]+%})', r'\1 \2', content)

with open(file_path, 'w') as f:
    f.write(content)

print("File patched successfully (Round 3).")
