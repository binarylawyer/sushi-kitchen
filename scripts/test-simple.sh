#!/usr/bin/env bash
# Simple test for the generator

echo "🧪 Testing Generator with hosomaki.redis"
echo "========================================"

# Create output directory
mkdir -p compose/generated

# Test with redis roll
python3 scripts/generate-compose.py --roll=hosomaki.redis --output=compose/generated/test-redis.yml

echo ""
echo "✅ Test completed! Check compose/generated/test-redis.yml"
