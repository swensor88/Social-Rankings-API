# Social-Rankings-API

FastAPI service and AWS infrastructure for collecting and organizing social media rankings for politicians.

## Architecture

- API framework: FastAPI with OpenAPI/Swagger UI at `/docs`.
- Data layer: SQLAlchemy ORM and Alembic migrations.
- Database: PostgreSQL (local via Docker, cloud via Amazon RDS).
- Runtime auth: API key using `X-API-Key` header for CRUD endpoints.
- Cloud hosting: ECS Fargate behind ALB, fronted by API Gateway.
- Secrets: AWS Secrets Manager for API key and DB connection values.
- Environment model: Terramate stack layout for `stage` and `prod`.

## Project Layout

- `app/`: FastAPI app, routes, models, schemas, repositories, config.
- `migrations/`: Alembic environment and initial migration.
- `tests/`: health/auth/CRUD integration tests.
- `infra/`: Terramate root, Terraform modules, environment stacks.
- `.github/workflows/ci-cd.yml`: CI/CD pipeline for test/build/deploy.

## API Endpoints

Public:
- `GET /health-check`

Protected with `X-API-Key`:
- `POST/GET/GET{id}/PUT{id}/DELETE{id}` for:
	- `/political-bodies`
	- `/politicians`
	- `/social-channels`
	- `/accounts`

## Data Model

- `political_body`: `id`, `name`, `description`
- `politicians`: `id`, `political_body_id`, `name`, `current_position`, `start_date`, `end_date`
- `social_channel`: `id`, `name`, `audience_type`, `download_type`, `download_frequency`
- `accounts`: `id`, `politician_id`, `social_channel_id`, `total_audience`

Enums:
- `download_type`: `api`, `web`, `s3`
- `download_frequency`: `hourly`, `daily`, `weekly`

## Local Development

### Prerequisites

- Python 3.11+
- Docker + Docker Compose

### Setup

1. Install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Create `.env` from `.env.example` and set values as needed.

3. Start local Postgres and API:

```bash
docker compose up --build
```

4. Apply migrations:

```bash
alembic upgrade head
```

5. Open Swagger UI:

- http://localhost:8000/docs

### Run Tests

```bash
pytest -q
```

## Migrations

- Create migration:

```bash
alembic revision -m "message"
```

- Apply migration:

```bash
alembic upgrade head
```

- Roll back one version:

```bash
alembic downgrade -1
```

## Infrastructure (Terramate + Terraform)

Region: `us-east-1`

Stacks:
- `infra/stacks/stage`
- `infra/stacks/prod`

Modules:
- `vpc`, `rds`, `secrets`, `iam`, `ecs`, `apigateway`

### Stage Deploy

1. Copy variables template:

```bash
cp infra/stacks/stage/terraform.tfvars.example infra/stacks/stage/terraform.tfvars
```

2. Edit values (`alb_certificate_arn`, `db_password`, `api_key`).

3. Deploy:

```bash
cd infra/stacks/stage
terraform init
terraform apply
```

### Production Deploy

1. Copy variables template:

```bash
cp infra/stacks/prod/terraform.tfvars.example infra/stacks/prod/terraform.tfvars
```

2. Edit values and deploy:

```bash
cd infra/stacks/prod
terraform init
terraform apply
```

## CI/CD

Workflow: `.github/workflows/ci-cd.yml`

Pipeline:
1. Trigger on push to `stage` (and manually via `workflow_dispatch`).
2. Run tests.
3. Build and push multi-arch Docker image to ECR (`latest` and commit SHA tags).
4. Force ECS rolling deployment on the stage service and wait for stability.

No additional GitHub Actions secrets/variables are required for role assumption.
The stage deploy role ARN is defined directly in `.github/workflows/ci-cd.yml`.

## Security Baseline for New AWS Account

1. Enable MFA for root account and avoid root daily usage.
2. Configure AWS IAM Identity Center for human access.
3. Use role-based access with least privilege for CI and runtime.
4. Enable CloudTrail in all regions.
5. Enable GuardDuty and AWS Config.
6. Add AWS Budgets and CloudWatch billing alarms.
7. Keep RDS private-only and restrict inbound traffic by security groups.

## Rollback and Recovery

- App rollback: redeploy ECS service with previous image tag.
- DB rollback: apply Alembic downgrade only for compatible changes.
- Infra rollback: use Terraform plan and targeted rollbacks carefully.

## Notes

- Current deployment uses AWS default endpoints.
- Custom domain and ACM automation can be added later.
- Production is currently single-AZ for cost control; upgrade path to multi-AZ is straightforward via RDS and subnet strategy.
