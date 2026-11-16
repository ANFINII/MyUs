resource "aws_cloudwatch_metric_alarm" "rds_free_storage" {
  alarm_name          = "${local.name}-rds-free-storage"
  alarm_description   = "RDS の空き容量が 2GiB を切った"
  namespace           = "AWS/RDS"
  metric_name         = "FreeStorageSpace"
  statistic           = "Minimum"
  period              = 300
  evaluation_periods  = 1
  comparison_operator = "LessThanOrEqualToThreshold"
  threshold           = 2 * 1024 * 1024 * 1024
  treat_missing_data  = "breaching"
  alarm_actions       = [aws_sns_topic.alarm.arn]
  ok_actions          = [aws_sns_topic.alarm.arn]

  dimensions = {
    DBInstanceIdentifier = local.mysql.identifier
  }
}

resource "aws_cloudwatch_metric_alarm" "rds_cpu" {
  alarm_name          = "${local.name}-rds-cpu"
  alarm_description   = "RDS の CPU 使用率が 15 分続けて 80% を超えた。t4g の RDS は Unlimited モードなので、続くと追加の料金がかかる"
  namespace           = "AWS/RDS"
  metric_name         = "CPUUtilization"
  statistic           = "Average"
  period              = 300
  evaluation_periods  = 3
  comparison_operator = "GreaterThanOrEqualToThreshold"
  threshold           = 80
  treat_missing_data  = "notBreaching"
  alarm_actions       = [aws_sns_topic.alarm.arn]
  ok_actions          = [aws_sns_topic.alarm.arn]

  dimensions = {
    DBInstanceIdentifier = local.mysql.identifier
  }
}
