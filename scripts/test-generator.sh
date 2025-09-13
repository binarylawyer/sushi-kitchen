#!/usr/bin/env bash
# Test script for the manifest generator

echo "🧪 Testing Sushi Kitchen Manifest Generator"
echo "=========================================="

# Create output directory
mkdir -p compose/generated

# Test 1: Generate a single roll
echo "Test 1: Single roll (hosomaki.redis)"
python3 scripts/generate-compose.py --roll=hosomaki.redis --output=compose/generated/test-redis.yml

echo ""
echo "Test 2: Single combo (combo.dev-tools)"
python3 scripts/generate-compose.py --combo=combo.dev-tools --output=compose/generated/test-dev-tools.yml

echo ""
echo "Test 3: Simple platter (platter.starter)"
python3 scripts/generate-compose.py --platter=platter.starter --output=compose/generated/test-starter.yml

echo ""
echo "✅ Tests completed! Check compose/generated/ for output files."
