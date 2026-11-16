resource "aws_cloudwatch_metric_alarm" "api_5xx" {
  provider = aws.us_east_1

  alarm_name          = "${local.name}-api-5xx"
  alarm_description   = "API の CloudFront の 5xx の割合が 10 分続けて 5% を超えた"
  namespace           = "AWS/CloudFront"
  metric_name         = "5xxErrorRate"
  statistic           = "Average"
  period              = 300
  evaluation_periods  = 2
  comparison_operator = "GreaterThanOrEqualToThreshold"
  threshold           = 5
  treat_missing_data  = "notBreaching"
  alarm_actions       = [aws_sns_topic.alarm_us_east_1.arn]
  ok_actions          = [aws_sns_topic.alarm_us_east_1.arn]

  dimensions = {
    DistributionId = local.api.distribution_id
    Region         = "Global"
  }
}
