import grpc
import UserManager_pb2, UserManager_pb2_grpc

from flask import Flask, request, jsonify

app = Flask(__name__)

grpc_channel = grpc.insecure_channel('userservice:50051') 
stub = UserManager_pb2_grpc.UserManagerStub(grpc_channel)

@app.post("/users")
def Adduser():

    data_in = request.get_json()
    email = data_in.get("email", "")
    user_name = data_in.get("name" , "")

    post_request = UserManager_pb2.AddUserRequest()
    post_request.email = email
    post_request.name = user_name

    try:
        post_response = stub.AddUser(post_request)
        resume = f"""{post_response.name}| {post_response.email}
        created an account with ID {post_response.id}
        at {post_response.created_at}\n"""

        return jsonify({
            "message" : f"{resume}",
            "id" : post_response.id
        }),201

    except grpc.RpcError as e:
        return jsonify({
            "error" : "microservice error\n",
            "details" : f"{e.details()}"
        }), 400


@app.delete("/users/<id>")
def Deleteuserid(id):

    delete_request = UserManager_pb2.DeleteUserRequest()
    delete_request.id = id

    try:
        delete_response = stub.DeleteUser(delete_request)

        return jsonify({
            "message" : f"{delete_response.delete_ack}\n"
        }), 200

    except grpc.RpcError as e:
        return jsonify({
            "error" : "microservice error \n",
            "details" : f"{e.details()}"
        }), 400

@app.get("/users/<id>")
def GetUser(id):

    get_user_request = UserManager_pb2.GetUserRequest()
    get_user_request.id = id

    try:
        get_user_response = stub.GetUser(get_user_request)
        resume = f"""USER: {get_user_response.name} | {get_user_response.email} | 
                     ID:{get_user_response.id}|
                     CREATED: {get_user_response.created_at}\n"""
        return jsonify({
            "message" : f"{resume}"
        }), 200

    except grpc.RpcError as e:
        return jsonify({
            "error" : "microservice error \n",
            "details" : f"{e.details()}"
        }), 400

@app.get("/users")
def GetList():

    get_request = UserManager_pb2.EmptyRequest()

    try:
        user_list = []
        get_response = stub.GetList(get_request)
        for user in get_response:
            user_dic = {
                "name" : user.name,
                "email" : user.email,
                "id" : user.id,
                "created_at" : user.created_at
            }
            user_list.append(user_dic)
        
        return jsonify(user_list), 200

    except grpc.RpcError as e:
        return jsonify({
            "error" : "microservice error \n",
            "details" : f"{e.details()}"
        }), 400





if __name__ == "__main__":
    print("Api running\n")
    app.run(host= "0.0.0.0", port = 5000, debug= True)
