# _For the assignment_
### Task 1
1. This deployment is currently not working properly, can you figure out why.
we have no env for prefix, so we only have one prefix / for default and it call for "de" at the time
And the svc name is now hello-world-en but the deployment and env are hello-world-de
  targetPort should be 8000 because container pod is listening on 8000


2. When querying different endpoints it should show each of the different services you created on the previous step:
http://<address>/de should show "Hello Freund"
http://<address>/es should show "Hello Amigo"
http://<address>/fr should show "Hello Ami"

Write api to get "de", "es", "fr" in nodejs and use env "REGION" for helm deployment 
```sh
app.get(`/${region}`, function(request, response) {
  response.send(`Hello ${world}`);
});
```


1. Deploy this applications to the istio service mesh

Expose this service to outside of the cluster by istio gateway ingress controller.
When query http://<address>/eu should load balancing round robind shows belows output
"Hello Freund"
"Hello Amigo"
"Hello Ami"

Using gateway and virtualservice to route /de; /es; /fr to the right region (deployment)
```sh
Example for de region:
  - name: "de"
    match:
    - uri:
        exact: "/de"
    route:
    - destination:
        host: hello-world
        subset: de
```


and using destination rule trafficPolicy: Loadbalancer type (ROUND_ROBIN) for /eu (route around de/es/fr )

```sh
apiVersion: networking.istio.io/v1alpha3
kind: DestinationRule
metadata:
  name: hello-world-destination
spec:
  host: hello-world.default.svc.cluster.local
  trafficPolicy:
    loadBalancer:
      simple: ROUND_ROBIN
  subsets:
  - name: de
    labels:
      region: de
  - name: es
    labels:
      region: es
  - name: fr
    labels:
      region: fr
```


helm upgrade --install kubernetes-task . --values values.yaml
kubectl apply -f test-destination.yaml
kubectl apply -f test-gateway.yaml



### Task 2

> Implement a Python or Golang app /script to perform a periodically health-check for the cluster/apps i.e usage of the pods (CPU/MEM), status of pod/node,...etc without using kubectl if possible.

![Home Page](https://github.com/ngdtrunguit/Python-for-K8s/blob/main/task2/homepage.png)

![Pod Status](https://github.com/ngdtrunguit/Python-for-K8s/blob/main/task2/pods-on-LB.png)

![Containers Utilization](https://github.com/ngdtrunguit/Python-for-K8s/blob/main/task2/cont-on-LB.png)






