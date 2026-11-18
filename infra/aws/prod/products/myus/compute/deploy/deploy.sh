#!/bin/bash
set -euo pipefail

: "${AWS_REGION:?}" "${PARAMETER_PATH:?}" "${IMAGE:?}"

cd /opt/myus
umask 077

aws ssm get-parameters-by-path \
  --region "$AWS_REGION" \
  --path "$PARAMETER_PATH" \
  --with-decryption \
  --query 'Parameters[].[Name,Value]' \
  --output text \
  | sed "s|^${PARAMETER_PATH}||; s|\t|=|" > django.env.new

if grep -q '=FIXME$' django.env.new; then
  echo "FIXME のままのパラメータがある:" >&2
  grep '=FIXME$' django.env.new | cut -d= -f1 >&2
  rm -f django.env.new
  exit 1
fi
mv django.env.new django.env

aws ecr get-login-password --region "$AWS_REGION" | docker login --username AWS --password-stdin "${IMAGE%%/*}"

export IMAGE
docker compose pull
docker compose run --rm backend python manage.py migrate --noinput
docker compose up -d --remove-orphans
docker image prune -f
