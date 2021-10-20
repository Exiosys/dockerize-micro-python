# from flask import Flask

# app = Flask(__name__)

# @app.route('/')
# def hello():
#     return "Demo Flask & Docker application is up and running!"

# if __name__ == '__main__':
#     app.run(host="0.0.0.0", port=80)


from flask import Flask, jsonify, request
import docker
app = Flask(__name__)
client = docker.DockerClient(base_url='unix://var/run/docker.sock')


def check_id_name(x, id):
    if x['Id'] == id or x['Names'][0] == '/'+id:
        return True
    return False


def get_container_info(id):
    container_info = {}
    for container in client.containers.list():
        if(container.id == id or container.name == id):
            api = container.client.api.containers()
            api = filter(lambda x: check_id_name(x, id), api)
            api = list(api)[0]
            if container.id == id or container.name == id:
                container_info['name'] = container.name
                container_info['short_hash'] = container.short_id
                container_info['image'] = container.image.tags[0]
                container_info['uptime'] = api["Status"]
                container_info['published_ports'] = container.ports
                container_info['volumes'] = api["Mounts"]
                return container_info
    return {"message": "Container not found"}


def get_all_running_containers():
    containers_info = []
    for container in client.containers.list():
        containers_info.append(get_container_info(container.id))
    return containers_info


def get_all_containers():
    return {"message" : "A faire"}


@app.route('/containers/')
def containers():
    isAll = request.args.get('all')
    if isAll == 'True' or isAll == '1':
        return  jsonify(get_all_containers())
    return jsonify(get_all_running_containers())


@app.route('/containers/<id>')
def containersID(id):
    client = docker.DockerClient(base_url='unix://var/run/docker.sock')
    container_info = {}
    for container in client.containers.list():
        if container.id == id or container.name == id:
            container_info = get_container_info(id)
            return jsonify(container_info)
    return {"message": "Container not found"}


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)


# if __name__ == "__main__":
