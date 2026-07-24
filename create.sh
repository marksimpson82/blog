#!/bin/bash

readonly title=$1

if [[ -z $title ]]; then
  echo >&2 "title must be provided"
  exit 1
fi

readonly file_date="$(date +%Y-%m-%d)"
readonly file_path="./_posts/${file_date}-${title}.md"

cat << EOF > "$file_path"
---
title: "${title}"
date: ${file_date}T00:00:00+00:00
author: Mark Simpson
layout: single
tags:
---
EOF

