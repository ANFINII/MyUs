resource "aws_cloudwatch_metric_alarm" "ec2_status_check" {
  alarm_name          = "${local.name}-ec2-status-check"
  alarm_description   = "EC2 のステータスチェックが失敗している"
  namespace           = "AWS/EC2"
  metric_name         = "StatusCheckFailed"
  statistic           = "Maximum"
  period              = 60
  evaluation_periods  = 5
  comparison_operator = "GreaterThanOrEqualToThreshold"
  threshold           = 1
  treat_missing_data  = "breaching"
  alarm_actions       = [aws_sns_topic.alarm.arn]
  ok_actions          = [aws_sns_topic.alarm.arn]

  dimensions = {
    InstanceId = local.api.instance_id
  }
}

resource "aws_cloudwatch_metric_alarm" "ec2_cpu_credit" {
  alarm_name          = "${local.name}-ec2-cpu-credit"
  alarm_description   = "EC2 の CPU クレジットが減っている。0 になると CPU がベースライン（20%）までに抑えられる"
  namespace           = "AWS/EC2"
  metric_name         = "CPUCreditBalance"
  statistic           = "Minimum"
  period              = 300
  evaluation_periods  = 2
  comparison_operator = "LessThanOrEqualToThreshold"
  threshold           = 50
  treat_missing_data  = "notBreaching"
  alarm_actions       = [aws_sns_topic.alarm.arn]
  ok_actions          = [aws_sns_topic.alarm.arn]

  dimensions = {
    InstanceId = local.api.instance_id
  }
}

resource "aws_cloudwatch_metric_alarm" "ec2_memory" {
  alarm_name          = "${local.name}-ec2-memory"
  alarm_description   = "EC2 のメモリの使用率が高い。足りなくなると OS ごと固まる"
  namespace           = "CWAgent"
  metric_name         = "mem_used_percent"
  statistic           = "Maximum"
  period              = 60
  evaluation_periods  = 3
  comparison_operator = "GreaterThanOrEqualToThreshold"
  threshold           = 90
  treat_missing_data  = "notBreaching"
  alarm_actions       = [aws_sns_topic.alarm.arn]
  ok_actions          = [aws_sns_topic.alarm.arn]

  dimensions = {
    InstanceId = local.api.instance_id
  }
}

resource "aws_cloudwatch_metric_alarm" "ec2_disk" {
  alarm_name          = "${local.name}-ec2-disk"
  alarm_description   = "EC2 のルートボリュームの使用率が高い。値が届かないときも鳴らす（CloudWatch Agent が止まっているかもしれない）"
  namespace           = "CWAgent"
  metric_name         = "disk_used_percent"
  statistic           = "Maximum"
  period              = 300
  evaluation_periods  = 2
  comparison_operator = "GreaterThanOrEqualToThreshold"
  threshold           = 80
  treat_missing_data  = "breaching"
  alarm_actions       = [aws_sns_topic.alarm.arn]
  ok_actions          = [aws_sns_topic.alarm.arn]

  dimensions = {
    InstanceId = local.api.instance_id
    path       = "/"
    fstype     = "xfs"
  }
}
