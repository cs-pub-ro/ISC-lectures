#!/bin/bash
for lecture_dir in lectures/*; do
  if [ -f "$lecture_dir/slides.md" ]; then
    lecture_name=$(basename $lecture_dir)
    echo "Building HTML for $lecture_name..."
    npx @slidev/cli build "$lecture_dir/slides.md" --out slides
    
    echo "Building PDF for $lecture_name..."
    npx @slidev/cli export "$lecture_dir/slides.md" --output "$lecture_dir/slides/slides.pdf"
  fi
done

echo "Starting NGINX..."
nginx -g "daemon off;"
