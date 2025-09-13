#!/usr/bin/env bash
# Test the template assembler

echo "🧪 Testing Template Assembler"
echo "============================="

# Create output directory
mkdir -p compose/generated

echo "Test 1: Assemble redis template"
python3 scripts/assemble-templates.py --rolls hosomaki.redis --output=compose/generated/test-redis-template.yml

echo ""
echo "Test 2: Assemble multiple templates"
python3 scripts/assemble-templates.py --rolls hosomaki.redis hosomaki.supabase --output=compose/generated/test-multi-template.yml

echo ""
echo "✅ Template tests completed!"
echo "Check these files:"
echo "- compose/generated/test-redis-template.yml"
echo "- compose/generated/test-multi-template.yml"
