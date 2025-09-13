#!/usr/bin/env bash
# Simple test for template assembler

echo "🧪 Testing Template Assembler"
echo "============================="

# Create output directory
mkdir -p compose/generated

echo "Test: Assemble redis template"
python3 scripts/assemble-templates.py --rolls hosomaki.redis --output=compose/generated/test-redis-template.yml

echo ""
echo "✅ Test completed! Check compose/generated/test-redis-template.yml"
