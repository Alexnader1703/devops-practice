yc iam key create --service-account-id aje7rsdh01tim89hf9fk --folder-name trainee-8 --output key.json - ключ
yc config profile create manager
yc config set service-account-key key.json
yc config set service-account-key key.json
yc config set cloud-id b1g5b020anchqspg6qul
yc config set folder-id b1gdpoivp1poeknjahoq
export YC_TOKEN=$(yc iam create-token)
export YC_FOLDER_ID=$(yc config get folder-id)