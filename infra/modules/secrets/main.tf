resource "aws_secretsmanager_secret" "db" {
  name = "${var.name_prefix}/db"
}

resource "aws_secretsmanager_secret_version" "db" {
  secret_id = aws_secretsmanager_secret.db.id
  secret_string = jsonencode({
    username          = var.db_username
    password          = var.db_password
    host              = var.db_host
    port              = var.db_port
    dbname            = var.db_name
    connection_string = "postgresql+psycopg://${var.db_username}:${var.db_password}@${var.db_host}:${var.db_port}/${var.db_name}"
  })
}

resource "aws_secretsmanager_secret" "api_key" {
  name = "${var.name_prefix}/api-key"
}

resource "aws_secretsmanager_secret_version" "api_key" {
  secret_id = aws_secretsmanager_secret.api_key.id
  secret_string = jsonencode({
    api_key = var.api_key
  })
}
