#!/bin/bash

# Find all public.pem files and store them in an array
files=($(find . -type f -name "public.pem"))

# Compare each file with every other file
for ((i=0; i<${#files[@]}; i++)); do
  for ((j=i+1; j<${#files[@]}; j++)); do
    diff "${files[i]}" "${files[j]}" > /dev/null
    if [ $? -ne 0 ]; then
      echo "Difference found between ${files[i]} and ${files[j]}"
    fi
  done
done