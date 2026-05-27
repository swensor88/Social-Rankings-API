# GitHub Copilot Prompt: Build Social-Rankings-API + AWS Infrastructure

Use this prompt with GitHub Copilot Chat in Agent mode to implement the app and infrastructure end-to-end.
## Prompt

You are GPT-5.3-Codex acting as a Principal Software Architect and Senior Full-Stack Engineer. Build a production-structured FastAPI service and Terramate-managed AWS infrastructure for a new project named Social-Rankings-API.

### Objective
Create:
1. A FastAPI web API with SQLAlchemy and Alembic, including CRUD for all required entities.
2. A Terramate solution for AWS hosting in us-east-1 using ECS Fargate, API Gateway, ALB, and RDS PostgreSQL.
3. Stage and production environments, low-cost defaults, and a secure baseline suitable for a new AWS account.
4. CI/CD via GitHub Actions.

### Known Inputs
- AWS Account ID: 716525549892
- AWS Region: us-east-1
- Endpoint strategy now: AWS default endpoints (no custom domain yet)
- DB sizing preference: free-tier-equivalent where available, otherwise lowest practical cost
- Production availability (initial): single-AZ
- Include API key auth now
- Include CI/CD now
- Scope excludes EventBridge for now

### Functional API Requirements
Build FastAPI with standard Swagger UI/OpenAPI configuration and these entities:

1. political_body
- id (PK int)
- name (text)
- description (text)

2. politicians
- id (PK int)
- political_body_id (FK int -> political_body.id)
- name (text)
- current_position (text)
- start_date (date)
- end_date (date, nullable)

3. social_channel
- id (PK int)
- name (text)
- audience_type (text)
- download_type (enum: api, web, s3)
- download_frequency (enum: hourly, daily, weekly)

4. accounts
- id (PK int)
- politician_id (FK int -> politicians.id)
- social_channel_id (FK int -> social_channel.id)
- total_audience (int)

Also include:
- Initial Alembic migration for the full schema
- CRUD endpoints for each entity
- /health-check endpoint returning 200 only when runtime and DB checks are healthy
- API key authentication for protected endpoints

### Infrastructure Requirements (Terramate + AWS)
Implement Terramate stacks/modules with stage and production environments and best-practice dependencies.

Core components:
- VPC and networking best practices
- ECS Fargate for app hosting
- RDS PostgreSQL in private subnets
- ALB in front of ECS
- API Gateway in front of ALB/ECS (to support future multi-service expansion)
- Secrets Manager for DB and API secrets
- IAM least-privilege roles/policies

Security/networking specifics:
- Public ingress only on 80 and 443
- Redirect 80 to 443
- Restrict backend traffic with security groups
- Keep DB private-only

Cost posture:
- Choose low-cost defaults for dev/stage
- Keep production initially single-AZ with documented path to multi-AZ

### Required Repository Outputs
Create and wire these areas (adapt naming as needed, but keep structure clear):
- app (FastAPI app, routes, schemas, models, config, db session/dependencies)
- migrations (Alembic)
- tests (API and integration tests)
- infra (Terramate root, stacks, modules, environment variables)
- .github/workflows (CI/CD)
- Dockerfile, docker-compose for local development
- README with setup, run, migration, deploy, rollback, and troubleshooting steps

### Implementation Expectations
- Use Python with FastAPI + SQLAlchemy + Alembic
- Use clear layering (models, schemas, services/repositories, routes)
- Use environment-driven config for local and AWS
- Add concise comments only where logic is non-obvious
- Keep code style consistent and lint-friendly
- Ensure OpenAPI docs accurately match implemented endpoints

### Suggested Execution Order
1. Scaffold app, dependencies, and local container workflow
2. Implement SQLAlchemy models and Alembic initial migration
3. Implement schemas/services/routes with full CRUD + health-check
4. Add API key auth and tests
5. Scaffold Terramate stacks/modules and AWS resource dependency order
6. Add GitHub Actions for test/build/deploy
7. Update documentation and run verification steps

### Verification Criteria
Local:
- Migrations apply successfully
- CRUD integration tests pass for all entities
- /health-check works for healthy and broken DB scenarios
- API key auth behavior is validated

Cloud (stage):
- Terramate stack plans/applies in dependency order
- ECS service is reachable through API Gateway endpoint
- ALB redirects 80 -> 443
- RDS accessible only from allowed private sources
- Secrets retrieval works from ECS task role
- Logs available in CloudWatch

Security and ops:
- IAM role separation and least privilege documented and applied
- New account baseline recommendations included (MFA, root lock-down, CloudTrail/Config/GuardDuty, Identity Center)
- Budget/cost alarm baseline configured and documented

### Final Delivery Format
When done, provide:
1. Architecture summary
2. File-by-file change list
3. Commands to run locally
4. Commands/workflow to deploy stage then production
5. Any assumptions and follow-up hardening recommendations

If any requirement is ambiguous during implementation, ask targeted questions before proceeding in that area.