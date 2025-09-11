# Contributing to Sushi Kitchen

Thank you for your interest in contributing! Sushi Kitchen thrives on community participation.  
This document explains how to add new rolls/platters, follow security best practices, and understand the CI/CD checks that protect the project.

---

## How to Contribute

- Fork the repo, branch off `main`, and submit a pull request (PR).
- Discuss larger changes in GitHub Issues or on Discord before opening a PR.
- Follow coding conventions (TypeScript/JavaScript with pnpm workspaces, YAML for configs).
- Write clear commit messages and PR descriptions.

---

## Local Development Setup

To get started locally:

1. **Install prerequisites**
   - [Docker](https://docs.docker.com/get-docker/) + Docker Compose plugin  
   - [Node.js 20+](https://nodejs.org/)  
   - [pnpm](https://pnpm.io/installation)

2. **Clone the repo**
   ```bash
   git clone https://github.com/<your-org>/sushi-kitchen.git
   cd sushi-kitchen

3. **Install dependencies

npm i -g pnpm
pnpm -w install

4. **Copy the environment template

cp .env.example .env

Fill in real values for secrets, database, and API keys as needed.

5. **Start the stack

docker compose --profile core up -d

Use --profile full to enable observability, media, and extras.

6. **Run dev server

pnpm dev

7. **Run tests

pnpm test

## Adding a New Roll or Platter

1. **Create the file**  
   - Rolls → add a YAML file under `/rolls/`.  
   - Platters → add a YAML file under `/platters/`.

2. **Validate the schema**  
   - Run schema validation before committing:  
     ```bash
     pnpm -w validate:schema
     ```

3. **Update docs**  
   - Document the new roll/platter in [`/docs/agents.md`](docs/agents.md).  
   - If applicable, include an example in `/recipes`.

4. **Marketplace integration**  
   - Add an entry in [`/marketplace/catalog.yaml`](marketplace/catalog.yaml).  
   - Attach any dashboards, workflows, or other artifacts.

---

## Security Guidelines

- **No privileged containers**. Always run services as non-root and drop unnecessary capabilities.  
- **No raw internet tools** in agent shells. If internet access is required, use the approved SearxNG proxy (if enabled).  
- **Redact secrets & PII** in logs and traces.  
- Respect `.env.example` conventions — never commit real `.env` secrets.  

See also: [`/docs/security.md`](docs/security.md).

---

## CI Gates

All pull requests are validated automatically by GitHub Actions. These checks must pass before merging:

- **Prettier**: code formatting (`pnpm -w format:check`).  
- **ESLint / linting**: static analysis (`pnpm -w lint`).  
- **Markdown lint, Vale, spellcheck**: style and prose validation.  
- **Schema validation**: rolls and platters must pass JSON schema checks (`pnpm -w validate:schema`).  
- **Docker Compose config validation**: `docker compose config`.  
- **Link checker**: verifies internal and external links.  
- **Lighthouse (preview)**: accessibility and performance audit for the website.  
- **Trivy scan**: dependency and container security advisories.

These steps are defined in [`.github/workflows/ci.yml`](.github/workflows/ci.yml).

---

## License

By contributing, you agree that your contributions will be licensed under the terms of the [Apache-2.0 License](LICENSE).

