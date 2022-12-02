from kubernetes import client, config
import os, time
from flask import Flask, render_template
#from apscheduler.schedulers.background import BackgroundScheduler


#config.load_kube_config("./config")   # I'm using file named "config" in the "/root" directory
config.load_incluster_config()

app = Flask(__name__)

# #function to get pod from all namespaces and save to pod.txt
# def get_pod_all_namespace():
#     v1 = kubernetes.client.CoreV1Api()
#     f = open('pod.txt', 'a+')
#     os.remove('pod.txt')
#     # f = open('pod.txt', 'w+')
#     print("Listing pods with their IPs:")
#     ret = v1.list_pod_for_all_namespaces(watch=False)
#     for i in ret.items:
#         f = open('pod.txt', 'a')
#         file_contents = f.write("%s\t%s\t%s\n" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))
#         f.close()
        
        
#Display pods status to /pods        
@app.route("/pods")
def display_pod():
    v1 = client.CoreV1Api()
    all_pods = v1.list_pod_for_all_namespaces()
    print("Listing pods with their IPs:"  )
    for i in all_pods.items:
        return render_template('pods.html', data=all_pods.items)


#Display containers utilization to /cont        
@app.route("/cont")
def display_cont():
    api = client.CustomObjectsApi()
    resource = api.list_namespaced_custom_object(group="metrics.k8s.io",version="v1beta1", namespace="", plural="pods")
    for pod in resource["items"]:
        containers = pod['containers']
        for container in containers:
            return render_template('cont.html', resource=resource["items"])       
@app.route("/")
def homepage():
    return render_template("home.html") 
# #monitoring container utilization 
# def resource_metrics():
#     api = client.CustomObjectsApi()
#     resource = api.list_namespaced_custom_object(group="metrics.k8s.io",version="v1beta1", namespace="default", plural="pods")
#     for pod in resource["items"]:
#         containers = pod['containers']
#         for container in containers:
#             print(container['name'], container['usage']['cpu'], container['usage']['memory'],  "\n")


# # flask app    
# def apps():
#     #resource_metrics()
#     display_pods()
#     display_cont()
#     homepage()
#     # get_pod_all_namespace()
#     #scheduler = BackgroundScheduler()
#     #scheduler.add_job(func=get_pod_all_namespace, trigger="interval", seconds=30)
#     #schedule.every(5).seconds.do(get_pod_all_namespace)
#     # scheduler.start()

        
    # return Flask(__name__)


if __name__ == "__main__":
    # from waitress import serve
    # serve(app, host="0.0.0.0", port=5000)
    app.run()