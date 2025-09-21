# 🍣 Sushi Kitchen Manifest System Architecture

A comprehensive guide to understanding and extending the Docker Compose framework

## Understanding The Complete Manifest Architecture

The Sushi Kitchen manifest system represents a sophisticated approach to managing AI infrastructure complexity through a carefully designed multi-layered architecture. Rather than requiring users to understand Docker networking, dependency resolution, and resource allocation, this system creates multiple abstraction layers that work together to transform high-level user intentions into working deployments.

To truly understand how this system works, we need to examine both its philosophical approach and its concrete implementation across multiple directories and file types. Think of this as studying both the theory and practice of infrastructure automation - each reinforces the other to create a powerful, extensible platform.

## The Multi-Directory Architecture: Separation of Concerns

The manifest system organizes its complexity across six distinct directories, each serving a specific purpose in the overall architecture. This separation allows different types of users to interact with the system at appropriate levels of abstraction while enabling sophisticated tooling and automation.

### The Core Directory: The Foundation (`core/`)

The `core/` directory contains the five essential files that define what services exist and how they work together. These files represent the "source of truth" for the entire system and are designed to be both human-readable and machine-processable.

**menu-manifest.md** serves as the human-facing catalog that organizes all 52 services into intuitive categories using our sushi-themed taxonomy. This file answers the question "what can I deploy?" in terms that make sense to users who want to accomplish specific goals rather than configure individual containers.

**badges.yml** creates the visual vocabulary that communicates important service characteristics without overwhelming users with technical details. When you see a "GPU Required" badge, you immediately understand the hardware implications without needing to parse Docker device requests and CUDA compatibility matrices.

**contracts.yml** contains the complete technical specifications that enable automatic dependency resolution, resource calculation, and Docker Compose generation. This file transforms the user-friendly information in the menu into concrete deployment instructions.

**combos.yml** and **bento_box.yml** provide curated combinations that demonstrate how services work together to solve real problems. These files bridge the gap between "here are the available components" and "here's how to build something useful."

The beauty of organizing these files in a dedicated `core/` directory lies in how it enables sophisticated workflows. Build systems can watch this directory for changes and automatically regenerate dependent files. Documentation systems can process these files to create interactive service selectors. Validation systems can ensure consistency across all five files before changes are committed.

### The Schemas Directory: Ensuring Consistency (`schemas/`)

The `schemas/` directory contains JSON Schema definitions that serve as both validation rules and development aids. These schemas enable several powerful capabilities that would be impossible without formal structure definitions.

When you edit `core/badges.yml` in an IDE with JSON Schema support, you get automatic completion for valid badge categories, color validation for hex codes, and warnings when you violate combination rules. The schemas prevent common mistakes like typos in service names or invalid resource requirements before they cause deployment failures.

More importantly, these schemas enable automated validation in continuous integration systems. Every change to the manifest files can be automatically validated against their schemas, ensuring that the system maintains consistency as it grows. This allows multiple contributors to add services without accidentally breaking the dependency resolution or badge validation logic.

The schemas also serve as documentation for developers building tools that process the manifest files. Rather than reverse-engineering the expected structure from examples, tooling developers can reference the authoritative schema definitions to understand exactly what fields are required and what values are acceptable.

### The Templates Directory: Code Generation Foundation (`templates/`)

The `templates/` directory provides the foundation for automated Docker Compose generation. These templates demonstrate a crucial principle of the manifest system: separating the declaration of what should be deployed from the mechanism of how it gets deployed.

**base.compose.yml** provides the foundational Docker Compose structure that gets customized based on user selections and privacy profiles. This template includes the common networking, volume management, and service discovery patterns that apply regardless of which specific services are selected.

The **network-profiles/** subdirectory contains templates for the three privacy isolation levels we support. When a user selects "legal privilege" privacy requirements, the system automatically applies network segmentation, audit logging, and data retention policies appropriate for sensitive data handling.

**environment-configs/** houses pre-configured environment variable sets for different deployment scenarios. These templates encode best practices for development, production, and compliance deployments, eliminating the guesswork involved in properly configuring complex AI infrastructure.

This template-based approach enables the manifest system to support multiple deployment targets. The same service definitions can generate Docker Compose files, Kubernetes manifests, or Terraform configurations by applying different templates to the same underlying data.

### The Examples Directory: Learning Through Practice (`examples/`)

The `examples/` directory bridges the gap between understanding the individual components and knowing how to combine them effectively. Each example represents a complete learning experience that demonstrates both the technical implementation and the reasoning behind design decisions.

**basic-rag-setup/** walks through the simplest possible deployment of a document question-answering system. This example explains not just which services to select, but why those specific services work well together, what the dependency resolution process looks like, and how to validate that the resulting system functions correctly.

**enterprise-deployment/** demonstrates the full complexity of a production-ready AI platform with authentication, monitoring, backup systems, and compliance features. This example shows how the manifest system scales from simple development scenarios to sophisticated enterprise requirements without requiring users to understand all the underlying complexity.

**compliance-ready/** focuses specifically on deployments that must meet regulatory requirements. This example demonstrates how the privacy profiles, audit logging, and data retention features work together to create legally defensible AI infrastructure.

Each example includes the complete journey from user requirements to working deployment, with detailed explanations of why specific choices were made. These examples serve as both learning resources and templates that users can adapt for their specific requirements.

### The Assets Directory: Visual Communication (`assets/`)

The `assets/` directory provides the visual elements that make the manifest system approachable and understandable. Rather than treating visual design as an afterthought, this directory recognizes that effective visual communication is essential for managing complex technical systems.

**badges/** contains the SVG icons that give each badge its distinctive visual identity. These icons aren't just decorative - they create an immediate visual vocabulary that helps users quickly understand service characteristics across the entire platform.

**diagrams/** houses architectural diagrams that explain how services connect together and how data flows through different deployment configurations. These diagrams serve both as documentation and as troubleshooting aids when deployments don't behave as expected.

**screenshots/** provides visual examples of what working deployments look like, helping users set appropriate expectations and recognize when their systems are functioning correctly.

## The Metadata File: The System's Self-Description

The `_metadata.json` file serves as the manifest system's "table of contents" and enables sophisticated tooling integration. This file allows MCP servers, build systems, and documentation generators to understand the complete structure of the manifest system without parsing every individual file.

The metadata file includes not just basic directory listings, but also information about file dependencies, update frequencies, and the types of tooling that each file supports. This enables build systems to make intelligent caching decisions and allows development tools to provide context-appropriate assistance.

For MCP servers specifically, the metadata file provides pre-computed cross-references and quick lookup tables that eliminate the need to parse large YAML files for simple queries. When an AI agent needs to find all services that provide vector storage capability, it can reference the generated cross-reference files rather than parsing the entire contracts definition.

## How The Architecture Enables Advanced Capabilities

The multi-directory architecture enables several advanced capabilities that would be difficult or impossible with a simpler file organization. Understanding these capabilities helps explain why the system is organized as it is.

**Automated Validation** becomes straightforward when schemas define expected structure and business rules. Build systems can automatically validate that new service additions follow established patterns, that badge combinations are consistent, and that dependency relationships are valid.

**Multi-Target Generation** is enabled by the template system. The same service definitions can generate Docker Compose files for local development, Kubernetes manifests for cloud deployment, or Terraform configurations for infrastructure as code workflows.

**Progressive Disclosure** allows different types of users to interact with the system at appropriate levels of detail. End users browse the menu and select combos, while platform engineers work with contracts and templates, and tooling developers reference schemas and metadata.

**Extensibility Without Breaking Changes** is supported by the version-aware schema system. New capabilities can be added to service contracts without disrupting existing tooling, and new badge types can be introduced without affecting existing service definitions.

**Intelligent Caching and Optimization** becomes possible when the metadata file clearly describes dependencies and update patterns. Build systems can avoid unnecessary work when only documentation files change, and development tools can provide faster feedback by caching expensive operations.

## The Development Workflow: How Changes Propagate

Understanding how changes flow through the manifest system helps explain why the directory structure is organized as it is. Each type of change has a different impact pattern and requires different validation steps.

When someone adds a new service, they must update both `core/menu-manifest.md` to make the service visible to users and `core/contracts.yml` to define its technical implementation. The schema validation ensures that the service follows established naming conventions and includes required fields. The automated cross-reference generation updates the lookup tables that enable efficient MCP server queries.

When badge definitions change in `core/badges.yml`, the validation system checks that existing service badge combinations remain valid, the asset management system verifies that required icons exist, and the documentation system regenerates UI components that display badges.

Template changes trigger regeneration of example deployments to ensure that the examples remain consistent with current best practices. This automated consistency checking prevents the common problem of documentation that becomes outdated as the underlying system evolves.

## Supporting Multiple Use Cases Simultaneously

The directory architecture enables the manifest system to serve multiple distinct use cases without compromising any of them. This is crucial for a platform that must support everyone from individual developers exploring AI capabilities to enterprise teams deploying production infrastructure.

**End User Service Selection** is supported by the menu, badges, and combo definitions in the `core/` directory. These files provide the human-friendly abstractions that make complex infrastructure deployment approachable for users who want to focus on their applications rather than deployment details.

**Automated Tooling Development** is enabled by the schemas, metadata, and generated cross-reference files. Developers building deployment automation, monitoring dashboards, or cost calculation tools can rely on well-defined interfaces rather than parsing arbitrary file formats.

**Educational Content Creation** benefits from the examples directory and the rich documentation embedded throughout the manifest files. Training materials, tutorials, and best practice guides can reference concrete examples and established patterns rather than creating artificial scenarios.

**Enterprise Governance and Compliance** requirements are addressed by the privacy profiles, audit capabilities, and resource management features defined in the contracts and templates. Organizations can deploy AI infrastructure while maintaining appropriate controls and meeting regulatory requirements.

## The Evolution Strategy: Maintaining Consistency While Growing

The manifest system includes several mechanisms that support evolution without breaking existing functionality. This forward-thinking approach recognizes that AI infrastructure is rapidly evolving and the platform must adapt while maintaining reliability for existing users.

**Schema Versioning** enables gradual introduction of new features without disrupting existing deployments. New optional fields can be added to service contracts while maintaining backward compatibility with existing tooling.

**Capability Extension** allows new types of services to be integrated by defining additional capabilities in the contracts file. This extensibility means the platform can support emerging AI technologies without requiring architectural changes.

**Template Evolution** supports new deployment targets and configuration patterns by adding templates without modifying the core service definitions. This separation allows the platform to adapt to new infrastructure approaches while preserving the investment in service curation and validation.

**Generated File Management** ensures that optimization files remain consistent with source definitions through automated regeneration. This approach eliminates the maintenance burden of keeping derived files synchronized while providing the performance benefits of pre-computed data structures.

## Conclusion: Architecture That Scales With Complexity

The Sushi Kitchen manifest system demonstrates how thoughtful architecture can make complex systems both powerful and approachable. By organizing functionality across multiple directories with clear responsibilities, the system provides appropriate interfaces for different types of users while enabling sophisticated automation and tooling integration.

The separation between human-friendly presentation in the `core/` directory and machine-optimized structures in the `generated/` and `templates/` directories allows the platform to optimize for both usability and performance. The schema-driven validation and the comprehensive examples ensure that the system maintains consistency as it grows.

This architectural approach positions the platform to evolve with the rapidly changing AI ecosystem while providing the stability and reliability that organizations need for production deployments. Whether you're a developer exploring AI capabilities, a team building production systems, or an organization implementing governance controls, the manifest system provides the appropriate level of abstraction for your needs while maintaining the flexibility to adapt as requirements change.