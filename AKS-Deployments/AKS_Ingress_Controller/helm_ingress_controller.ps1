# Set variable for ACR location to use for pulling images
$ACR_URL="resenseacr.azurecr.io"
$STATIC_IP="20.198.75.177"
$RESOURCE_GROUP="Resense-PoC"
$DNS_LABEL="resense.tech"
$REGISTRY_NAME="resenseacr"
$SOURCE_REGISTRY="k8s.gcr.io"
$CONTROLLER_IMAGE="ingress-nginx/controller"
$CONTROLLER_TAG="v1.0.4"
$PATCH_IMAGE="ingress-nginx/kube-webhook-certgen"
$PATCH_TAG="v1.1.1"
$DEFAULTBACKEND_IMAGE="defaultbackend-amd64"
$DEFAULTBACKEND_TAG="1.5"
$CERT_MANAGER_REGISTRY="quay.io"
$CERT_MANAGER_TAG="v1.5.4"
$CERT_MANAGER_IMAGE_CONTROLLER="jetstack/cert-manager-controller"
$CERT_MANAGER_IMAGE_WEBHOOK="jetstack/cert-manager-webhook"
$CERT_MANAGER_IMAGE_CAINJECTOR="jetstack/cert-manager-cainjector"

# Use Helm to deploy an NGINX ingress controller
helm install nginx-ingress ingress-nginx/ingress-nginx `
    --namespace resense --create-namespace `
    --set controller.replicaCount=2 `
    --set controller.nodeSelector."kubernetes\.io/os"=linux `
    --set controller.image.registry=$ACR_URL `
    --set controller.image.image=$CONTROLLER_IMAGE `
    --set controller.image.tag=$CONTROLLER_TAG `
    --set controller.image.digest="" `
    --set controller.admissionWebhooks.patch.nodeSelector."kubernetes\.io/os"=linux `
    --set controller.admissionWebhooks.patch.image.registry=$ACR_URL `
    --set controller.admissionWebhooks.patch.image.image=$PATCH_IMAGE `
    --set controller.admissionWebhooks.patch.image.tag=$PATCH_TAG `
    --set controller.admissionWebhooks.patch.image.digest="" `
    --set defaultBackend.nodeSelector."kubernetes\.io/os"=linux `
    --set defaultBackend.image.registry=$ACR_URL `
    --set defaultBackend.image.image=$DEFAULTBACKEND_IMAGE `
    --set defaultBackend.image.tag=$DEFAULTBACKEND_TAG `
    --set defaultBackend.image.digest="" `
    --set controller.service.type=LoadBalancer `
    --set controller.service.loadBalancerIP=$STATIC_IP `
    --set controller.service.annotations."service\.beta\.kubernetes\.io/azure-load-balancer-resource-group"=$RESOURCE_GROUP `
    --set controller.service.externalTrafficPolicy=Local
    