# /bin/bash

# (1) Front-end
kubectl run front-end-app \
  --image=nginx \
  --labels="role=front-end" \
  --expose --port=80 \
  --namespace development

# (2) Back-end API
kubectl run back-end-api-app \
  --image=nginx \
  --labels="role=back-end-api" \
  --expose --port=80 \
  --namespace development

# (3) Admin front-end
kubectl run admin-front-end-app \
  --image=nginx \
  --labels="role=admin-front-end" \
  --expose --port=80 \
  --namespace development

# (4) Admin back-end API
kubectl run admin-back-end-api-app \
  --image=nginx \
  --labels="role=admin-back-end-api" \
  --expose --port=80 \
  --namespace development