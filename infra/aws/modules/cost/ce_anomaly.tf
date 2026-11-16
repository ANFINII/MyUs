###
# Cost Explorer (コスト異常検知)
###
resource "aws_ce_anomaly_monitor" "service" {
  name              = var.name
  monitor_type      = "DIMENSIONAL"
  monitor_dimension = "SERVICE"

  tags = {
    Name = var.name
  }
}

resource "aws_ce_anomaly_subscription" "daily" {
  name      = "daily-${var.name}-detected-anomaly-cost-exceeded-${var.cost_anomaly_threshold_dollar}-dollar"
  frequency = "DAILY"

  monitor_arn_list = [
    aws_ce_anomaly_monitor.service.arn,
  ]

  dynamic "subscriber" {
    for_each = var.emails

    content {
      type    = "EMAIL"
      address = subscriber.value
    }
  }

  threshold_expression {
    dimension {
      key           = "ANOMALY_TOTAL_IMPACT_ABSOLUTE"
      match_options = ["GREATER_THAN_OR_EQUAL"]
      values        = [var.cost_anomaly_threshold_dollar]
    }
  }

  tags = {
    Name = "daily-${var.name}-detected-anomaly-cost-exceeded-${var.cost_anomaly_threshold_dollar}-dollar"
  }
}
