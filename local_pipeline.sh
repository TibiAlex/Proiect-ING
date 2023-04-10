#!/bin/bash

# $1 - parameter for the operation that we want the script to make
# $(echo $2 | cut -d'=' -f1) - f1 gives me what is before = and f2 what is after

if [ "$1" = "build" ]
then
    # $2 - image_name; $3 - docker file location
    if [[ $(echo $2 | cut -d'=' -f1) != "image_name" || $(echo $3 | cut -d'=' -f1) != "location" ]]
    then
        echo "The parameters for the build are:"
        echo "image_name=<image_name>"
        echo "location=<location>"
    else
        echo "Building the docker image!"
        IMAGE_NAME=$(echo $2 | cut -d'=' -f2)
        LOCATION=$(echo $3 | cut -d'=' -f2)
        docker build -t $IMAGE_NAME $LOCATION
        echo "Finished building the docker image!"
    fi
elif [ "$1" = "push" ]
then
    # $2 - username; $3 - password; $4 - image_name; $5 - image_tag
    if [[ $(echo $2 | cut -d'=' -f1) != "username" || $(echo $3 | cut -d'=' -f1) != "password" || $(echo $4 | cut -d'=' -f1) != "image_name" || $(echo $5 | cut -d'=' -f1) != "image_tag" ]]
    then
        echo "The parameters for the push are:"
        echo "username=<username>"
        echo "password=<password>"
        echo "image_name=<image_name>"
        echo "image_tag=<image_tag>"
    else
        echo "Pushing the image to dockerhub!"
        USERNAME=$(echo $2 | cut -d'=' -f2)
        PASSWORD=$(echo $3 | cut -d'=' -f2)
        IMAGE_NAME=$(echo $4 | cut -d'=' -f2)
        IMAGE_TAG=$(echo $5 | cut -d'=' -f2)
        docker tag $IMAGE_NAME $USERNAME/$IMAGE_NAME:$IMAGE_TAG
        docker login -u $USERNAME -p $PASSWORD
        docker push $USERNAME/$IMAGE_NAME:$IMAGE_TAG
        echo "Finished pushing the docker image!"
    fi
elif [ "$1" = "deploy" ]
then
    # $2 - image_name; $3 - image_tag
    if [[ $(echo $2 | cut -d'=' -f1) != "image_name" || $(echo $3 | cut -d'=' -f1) != "image_tag" ]]
    then
        echo "The parameters for the deploy are:"
        echo "image_name=<image_name>"
        echo "image_tag=<image_tag>"
    else
        echo "Deploying the image locally!"
        IMAGE_NAME=$(echo $2 | cut -d'=' -f2)
        IMAGE_TAG=$(echo $3 | cut -d'=' -f2)
        # here i check if there already is a container running so i can stop it
        container_name=$(docker ps -a --format '{{.Names}}' | grep one_flask_like_no_other)
        if [ "$container_name" = "one_flask_like_no_other" ]; then
            docker stop one_flask_like_no_other
            docker rm one_flask_like_no_other
        fi
        docker run -d -p 5000:5000 --name one_flask_like_no_other $IMAGE_NAME:$IMAGE_TAG
        echo "The container has been created!"
    fi
elif [ "$1" = "test" ]
then
    # $2 - endpoint
    if [[ $(echo $2 | cut -d'=' -f1) != "endpoint" ]]
    then
        echo "The parameters for the test are:"
        echo "endpoint=<endpoint>"
    else
        echo "Sending a request with curl!"
        ENDPOINT=$(echo $2 | cut -d'=' -f2)
        curl -v $ENDPOINT
    fi
elif [ "$1" = "kube_deploy" ]
then
    echo "Preparing to deploy to minikube"
    kubectl apply -f k8s_manifest.yaml
    echo "The application has been deployed!"
else
    echo "Wrong first parameter, the options are: build, push, deploy, test, kube_deploy!"
fi
