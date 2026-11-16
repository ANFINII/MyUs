resource "aws_sns_topic" "alarm" {
  name = "${local.name}-alarm"
}

resource "aws_sns_topic_subscription" "alarm" {
  count = nonsensitive(length(var.emails_for_alarm))

  topic_arn = aws_sns_topic.alarm.arn
  protocol  = "email"
  endpoint  = var.emails_for_alarm[count.index]
}

resource "aws_sns_topic" "alarm_us_east_1" {
  provider = aws.us_east_1

  name = "${local.name}-alarm"
}

resource "aws_sns_topic_subscription" "alarm_us_east_1" {
  provider = aws.us_east_1
  count    = nonsensitive(length(var.emails_for_alarm))

  topic_arn = aws_sns_topic.alarm_us_east_1.arn
  protocol  = "email"
  endpoint  = var.emails_for_alarm[count.index]
}
