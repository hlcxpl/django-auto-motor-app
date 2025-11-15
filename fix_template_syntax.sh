#!/bin/bash
# Fix Django template syntax errors in vehiculo_list.html

FILE="vehiculo/templates/vehiculo/vehiculo_list.html"

echo "Fixing template syntax errors in $FILE..."

# Fix 1: Add spaces around == in marca comparison
sed -i 's/{% if marca==current_marca %}/{% if marca == current_marca %}/g' "$FILE"

# Fix 2: Add spaces around == in categoria comparison
sed -i 's/{% if categoria==current_categoria %}/{% if categoria == current_categoria %}/g' "$FILE"

# Fix 3: Fix broken {% endif %} tag that spans multiple lines
# This will join the split {% endif tag
sed -i ':a;N;$!ba;s/{% if categoria == current_categoria %}selected{% endif\n *%}/{% if categoria == current_categoria %}selected{% endif %}/g' "$FILE"

echo "Template syntax fixes applied!"
echo ""
echo "Verifying changes:"
grep -n "marca == current_marca" "$FILE" || echo "Warning: marca fix not found"
grep -n "categoria == current_categoria" "$FILE" || echo "Warning: categoria fix not found"
