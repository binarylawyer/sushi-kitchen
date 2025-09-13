#!/usr/bin/env bash
# Test the updated chef-themed templates

echo "🍣 Testing Updated Chef-Themed Templates"
echo "========================================"

# Create output directory
mkdir -p compose/generated

echo "Test 1: Redis Chef (Lightning-Fast Sous Chef)"
python3 scripts/assemble-templates.py --rolls hosomaki.redis --output=compose/generated/redis-chef.yml

echo ""
echo "Test 2: PostgreSQL Chef (Master Data Chef)"
python3 scripts/assemble-templates.py --rolls hosomaki.supabase --output=compose/generated/postgres-chef.yml

echo ""
echo "Test 3: n8n Chef (Orchestration Maestro)"
python3 scripts/assemble-templates.py --rolls hosomaki.n8n --output=compose/generated/n8n-chef.yml

echo ""
echo "Test 4: Full Kitchen (All Three Chefs)"
python3 scripts/assemble-templates.py --rolls hosomaki.redis hosomaki.supabase hosomaki.n8n --output=compose/generated/full-kitchen.yml

echo ""
echo "✅ Chef template tests completed!"
echo ""
echo "Check these files to see the chef commentary:"
echo "- compose/generated/redis-chef.yml"
echo "- compose/generated/postgres-chef.yml" 
echo "- compose/generated/n8n-chef.yml"
echo "- compose/generated/full-kitchen.yml"
echo ""
echo "🍣 Your chefs are ready to serve with style!"
