#!/usr/bin/env node
/**
 * Generates TypeScript types from the API bundle
 */

import fs from 'fs';
import path from 'path';

interface APIBundle {
  version: string;
  generated_at: string;
  services: Record<string, Service>;
  combos: Record<string, Combo>;
  platters: Record<string, Platter>;
  capabilities: Record<string, Capability>;
  network_profiles: Record<string, NetworkProfile>;
  badges: Record<string, BadgeCategory>;
}

interface Service {
  id: string;
  name: string;
  category: string;
  provides: string[];
  requires: string[];
  resource_requirements: ResourceRequirements;
  docker: DockerConfig;
  description: string;
  status: string;
}

interface Combo {
  id: string;
  name: string;
  description: string;
  includes: string[];
  optional: string[];
  provides: string[];
  difficulty: string;
  estimated_setup_time_min: number;
  tags: string[];
}

interface Platter {
  id: string;
  name: string;
  description: string;
  includes: string[];
  optional: string[];
  provides: string[];
  resource_requirements: ResourceRequirements;
  difficulty: string;
  estimated_setup_time_min: number;
  tags: string[];
}

interface ResourceRequirements {
  cpu_min?: string;
  memory_min?: string;
  storage_min?: string;
  gpu_required?: boolean;
}

interface DockerConfig {
  image?: string;
  ports?: Array<string | number>;
  environment?: string[];
  volumes?: string[];
}

interface Capability {
  description: string;
  providers: string[];
}

interface NetworkProfile {
  name: string;
  description: string;
  security_level: string;
  suitable_for: string[];
}

interface BadgeCategory {
  [key: string]: {
    color: string;
    label: string;
  };
}

function generateTypes(bundlePath: string, outputPath: string) {
  console.log(`Reading API bundle from: ${bundlePath}`);

  if (!fs.existsSync(bundlePath)) {
    console.error(`Error: Bundle file not found at ${bundlePath}`);
    process.exit(1);
  }

  const bundle: APIBundle = JSON.parse(fs.readFileSync(bundlePath, 'utf-8'));

  // Extract unique categories
  const serviceCategories = new Set<string>();
  Object.values(bundle.services).forEach(service => {
    serviceCategories.add(service.category);
  });

  // Extract unique difficulty levels
  const difficultyLevels = new Set<string>();
  Object.values(bundle.combos).forEach(combo => {
    difficultyLevels.add(combo.difficulty);
  });
  Object.values(bundle.platters).forEach(platter => {
    difficultyLevels.add(platter.difficulty);
  });

  // Extract unique status values
  const statusValues = new Set<string>();
  Object.values(bundle.services).forEach(service => {
    statusValues.add(service.status);
  });

  let output = `// Auto-generated types from Sushi Kitchen manifests
// Generated: ${new Date().toISOString()}
// Bundle version: ${bundle.version}

export interface ResourceRequirements {
  cpu_min?: string;
  memory_min?: string;
  storage_min?: string;
  gpu_required?: boolean;
}

export interface DockerConfig {
  image?: string;
  ports?: Array<string | number>;
  environment?: string[];
  volumes?: string[];
}

export interface Service {
  id: string;
  name: string;
  category: ServiceCategory;
  provides: string[];
  requires: string[];
  resource_requirements: ResourceRequirements;
  docker: DockerConfig;
  description: string;
  status: ServiceStatus;
}

export interface Combo {
  id: string;
  name: string;
  description: string;
  includes: string[];
  optional: string[];
  provides: string[];
  difficulty: DifficultyLevel;
  estimated_setup_time_min: number;
  tags: string[];
}

export interface Platter {
  id: string;
  name: string;
  description: string;
  includes: string[];
  optional: string[];
  provides: string[];
  resource_requirements: ResourceRequirements;
  difficulty: DifficultyLevel;
  estimated_setup_time_min: number;
  tags: string[];
}

export interface Capability {
  description: string;
  providers: string[];
}

export interface NetworkProfile {
  name: string;
  description: string;
  security_level: 'low' | 'medium' | 'high';
  suitable_for: string[];
}

export interface Badge {
  color: string;
  label: string;
}

export interface BadgeCategory {
  [key: string]: Badge;
}

// Union types based on actual data
export type ServiceCategory = ${Array.from(serviceCategories)
    .map(cat => `'${cat}'`)
    .join(' | ')};

export type DifficultyLevel = ${Array.from(difficultyLevels)
    .map(level => `'${level}'`)
    .join(' | ')};

export type ServiceStatus = ${Array.from(statusValues)
    .map(status => `'${status}'`)
    .join(' | ')};

export type NetworkProfileType = ${Object.keys(bundle.network_profiles)
    .map(profile => `'${profile}'`)
    .join(' | ')};

// API Bundle interface
export interface APIBundle {
  version: string;
  generated_at: string;
  checksums: Record<string, string>;
  services: Record<string, Service>;
  combos: Record<string, Combo>;
  bentos: Record<string, any>; // Flexible for future bento structure
  platters: Record<string, Platter>;
  capabilities: Record<string, Capability>;
  badges: Record<string, BadgeCategory>;
  network_profiles: Record<string, NetworkProfile>;
  security_policies: Record<string, any>; // Flexible for security policies
}

// Request/Response types for API
export interface GenerateRequest {
  selection_type: 'platter' | 'combo' | 'roll';
  selection_id: string;
  privacy_profile: NetworkProfileType;
  include_optional?: boolean;
}

export interface GenerateResponse {
  yaml: string;
  services: string[];
  profile: NetworkProfileType;
  success: boolean;
  validation?: ValidationResult;
}

export interface ValidationResult {
  valid: boolean;
  warnings: string[];
  errors: string[];
}

// Utility types
export interface ComponentStats {
  services_count: number;
  combos_count: number;
  platters_count: number;
  capabilities_count: number;
  total_size_bytes: number;
}

// Specific service categories for type safety
export interface CoreService extends Service {
  category: 'hosomaki';
}

export interface KnowledgeService extends Service {
  category: 'futomaki';
}

export interface VoiceService extends Service {
  category: 'temaki';
}

export interface ImagingService extends Service {
  category: 'uramaki';
}

export interface DataScienceService extends Service {
  category: 'chirashi';
}

export interface DevToolsService extends Service {
  category: 'tamago';
}

export interface ObservabilityService extends Service {
  category: 'dragon';
}

// Constants derived from the bundle
export const SERVICE_CATEGORIES: ServiceCategory[] = [${Array.from(serviceCategories)
    .map(cat => `'${cat}'`)
    .join(', ')}];

export const DIFFICULTY_LEVELS: DifficultyLevel[] = [${Array.from(difficultyLevels)
    .map(level => `'${level}'`)
    .join(', ')}];

export const SERVICE_STATUSES: ServiceStatus[] = [${Array.from(statusValues)
    .map(status => `'${status}'`)
    .join(', ')}];

export const NETWORK_PROFILES: NetworkProfileType[] = [${Object.keys(bundle.network_profiles)
    .map(profile => `'${profile}'`)
    .join(', ')}];

// Bundle metadata
export const BUNDLE_VERSION = '${bundle.version}';
export const BUNDLE_GENERATED_AT = '${bundle.generated_at}';
`;

  // Ensure output directory exists
  const outputDir = path.dirname(outputPath);
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }

  fs.writeFileSync(outputPath, output);
  console.log(`TypeScript types generated: ${outputPath}`);
  console.log(`Generated types for:`);
  console.log(`  - ${Object.keys(bundle.services).length} services`);
  console.log(`  - ${Object.keys(bundle.combos).length} combos`);
  console.log(`  - ${Object.keys(bundle.platters).length} platters`);
  console.log(`  - ${serviceCategories.size} service categories`);
  console.log(`  - ${difficultyLevels.size} difficulty levels`);
}

// CLI interface
function main() {
  const args = process.argv.slice(2);

  if (args.length < 2) {
    console.error('Usage: generate-types.ts <bundle.json> <output.ts>');
    console.error('');
    console.error('Examples:');
    console.error('  npm run generate-types api-bundle.json src/types/sushi.ts');
    console.error('  node generate-types.js api-bundle.json lib/types.ts');
    process.exit(1);
  }

  const [bundlePath, outputPath] = args;

  try {
    generateTypes(bundlePath, outputPath);
  } catch (error) {
    console.error('Error generating types:', error);
    process.exit(1);
  }
}

// Run if called directly
if (require.main === module) {
  main();
}