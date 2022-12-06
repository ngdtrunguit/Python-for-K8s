# _For the assignment_

### Task 1 - helm debug
1. This deployment is currently not working properly, can you figure out why?
   
> We have no env for prefix, so we only have one prefix / for default and it call for "de" at the time
And the svc name is now hello-world-en but the deployment and env are hello-world-de
  targetPort should be 8000 because container pod is listening on 8000


2. When querying different endpoints it should show each of the different services you created on the previous step:
   
- `http://<address>/de` should show "Hello Freund"
- `http://<address>/es` should show "Hello Amigo"
- `http://<address>/fr` should show "Hello Ami"

> Write api to get "de", "es", "fr" in nodejs and use env "REGION" for helm deployment 
```sh
app.get(`/${region}`, function(request, response) {
  response.send(`Hello ${world}`);
});
```


3. Deploy this applications to the istio service mesh

- 3.1 Expose this service to outside of the cluster by istio gateway ingress controller.
> Using gateway and virtualservice to route /de; /es; /fr to the right region (deployment)
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
- 3.2 When query `http://<address>/eu` should load balancing round robind shows belows output
"Hello Freund"
"Hello Amigo"
"Hello Ami"

>Using destination rule trafficPolicy: Loadbalancer type (ROUND_ROBIN) for /eu (route around de/es/fr )

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



### Task 2

- Implement a Python or Golang app /script to perform a periodically health-check for the cluster/apps i.e usage of the pods (CPU/MEM), status of pod/node,...etc without using kubectl if possible.

> Using kubernetes client to grab the API, visual the output to python flask
```sh

*.py
#Get all pods from all namespace 
@app.route("/pods")
def display_pod():
    v1 = client.CoreV1Api()
    all_pods = v1.list_pod_for_all_namespaces()

#Get all containers information from all namespace
@app.route("/cont")
def display_cont():
    api = client.CustomObjectsApi()
    resource = api.list_namespaced_custom_object(group="metrics.k8s.io",version="v1beta1", namespace="", plural="pods")

*.html

#Showing pods information and status
    <tbody>
        {% for item in data %}
            <tr>
                <td>{{ item.status.pod_ip }}</td>
                <td>{{ item.metadata.namespace }}</td>
                <td>{{ item.metadata.name }}</td>
                <td>{{ item.status.phase }}</td>
            </tr>
    </tbody>

#Showing containers cpu/memory utilization
    <tbody>
        {% for pod in resource %}
        {% set containers = pod['containers'] %}
        {%for container in containers %}
            <tr>
                <td>{{ pod.metadata.name }}</td>
                <td>{{ container['usage']['cpu'] }}</td>
                <td>{{ container['usage']['memory'] }}</td>
            </tr>
        {% endfor %}
    </tbody>
```

![Home Page](https://github.com/ngdtrunguit/Python-for-K8s/blob/main/task2/homepage.png)

![Pod Status](https://github.com/ngdtrunguit/Python-for-K8s/blob/main/task2/pods-on-LB.png)

![Containers Utilization](https://github.com/ngdtrunguit/Python-for-K8s/blob/main/task2/cont-on-LB.png)






