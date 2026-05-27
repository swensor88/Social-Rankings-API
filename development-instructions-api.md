Act as a Principal Software Architect and Senior Full-Stack Engineer. Your task is to create a Web API using python's Fast API, and build out a terramate infrastructure solution for hosting it in AWS. The hosting should be a containerized solution using ECS, API Gateway, Load Balancers, RDS (postgres)

The FastAPI should include Swagger UI with standard configuration.

The API will have a data layer publishing to an RDS Postgres instance. The data domain will have the following entities/schema:

-political_body
--id, pk int
--name (text)
--description (text)

-politicians
--id, primary key (int)
--political_body_id, fk int
--name (text)
--current_position (text)
--start_date (date)
--end_date (date), nullable

-social_channel
--id, pk int
--name (text)
--audience_type (text)
--download_type (enum, value can be api, web, s3)
--download_frequency (enum, hourly, daily, weekly)

-accounts
--id, primary key (int)
--politician_id, foreign key to politicians table (int)
--social_channel_id, foreign key to social_channel table (int)
--total_audience, int, 

Use SQLAlchemy for the data layer, and create an initial migration for the above schema. 

Create CRUD endpoints for each of the above data types.

Also create a /health-check endpoint, returning a 200 if the service is running and no errors are found during execution


--Host items in region us-east-1
--Select low-cost options for all services, as this will be a dev environment initially.
--Prompt me for all information needed regarding AWS, such as account id

Terramate solution should include:

--environment management, with stage and production environments for the app
--Use ECS Fargate for application hosting
--Use RDS for database
--Put an API Gateway in front of everything, the plan will be to add additional services behind the API Gateway later.
--Use Secret Manager or similar technology for managing connection strings, API Keys, etc.
--Best practices for VPC setup and security
--Best practices for networking, firewalling. Only allow traffic on Port 443, and redirect port 80 to port 443
--this is a new AWS account, so please make a recommendation for basic security practices regarding IAM, roles. 