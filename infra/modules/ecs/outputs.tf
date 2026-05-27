output "ecr_repository_url" {
  value = aws_ecr_repository.app.repository_url
}

output "app_security_group_id" {
  value = aws_security_group.app.id
}

output "alb_dns_name" {
  value = aws_lb.this.dns_name
}

output "alb_listener_arn" {
  value = aws_lb_listener.https.arn
}
