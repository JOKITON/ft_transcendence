while [[ true ]]; do
  curl -X POST \
    http://localhost/api/v1/login \
    -H 'Content-Type: application/json' \
    -d '{ "username": "duvan", "password": "duvan"}'
done
