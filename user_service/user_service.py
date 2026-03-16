import grpc 
import UserManager_pb2, UserManager_pb2_grpc
from concurrent import futures
from bson import ObjectId
from bson.errors import InvalidId
from datetime import datetime
from pymongo import MongoClient
import stomp


client = MongoClient("mongodb://mongodb:27017")
db = client["UsermanagerDB"]
users_collection = db["UsermanagerCollection"]



class UserManagerServicer(UserManager_pb2_grpc.UserManagerServicer):

    def __init__(self, conn, dest_send):
        self.conn = conn
        self.dest_send = dest_send

    def AddUser(self, request, context):
        print("AddUser called\n")
        email_in = request.email
        name_in = request.name

        research_filter = {
            "email" : email_in
        }

        result_research = users_collection.find_one(research_filter)
        add_response = UserManager_pb2.User()

        if(result_research is None):
            created_at = datetime.now().isoformat()
            user_to_add = {
                "name" : name_in,
                "email" : email_in,
                "created_at" : created_at
            }
            result = users_collection.insert_one(user_to_add)

            added_user_id = str(result.inserted_id)

            add_response.id = added_user_id
            add_response.name = name_in
            add_response.email = email_in
            add_response.created_at = created_at

            try:
                message_stomp = f"\nADDED USER: {name_in}/{email_in}/{added_user_id}/{created_at}\n"
                self.conn.send(destination = self.dest_send, body = message_stomp)
            except Exception as e:
                print(f"STOMP ERROR {e}")


            return add_response
        
        else:
            context.abort(grpc.StatusCode.ALREADY_EXISTS, "Email already used")



    def GetUser(self, request, context):
        print("GetUser called\n")

        try:
            id_research = ObjectId(request.id)
        except InvalidId:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "Id format not valid")

        research_filter = {
            "_id" : id_research
        }

        result_research = users_collection.find_one(research_filter)
        get_response = UserManager_pb2.User()
        if(result_research is None):
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "User not found")
        else:
            get_response.name = result_research.get("name", "")
            get_response.email = result_research.get("email", "")
            get_response.id = str(result_research["_id"])
            get_response.created_at = result_research.get("created_at", "")
            return get_response
            



    def GetList(self, request, context):
        print("GetList called\n")

        get_list_response = UserManager_pb2.User()

        users = users_collection.find()

        for user in users:
            get_list_response.name = user.get("name", "")
            get_list_response.email = user.get("email", "")
            get_list_response.id = str(user["_id"])
            get_list_response.created_at = user.get("created_at", "")
            yield get_list_response

    def DeleteUser(self, request, context):
        print("DeleteUser called\n")

        try:
            id_research = ObjectId(request.id)
        except InvalidId:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "Id format not valid")        
        
        research_filter = {
            "_id" : id_research
        }
        user_delete = users_collection.find_one_and_delete(research_filter)
        if(user_delete is None):
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "User not found")
        else:
            delete_response = UserManager_pb2.DeleteAck()
            delete_response.delete_ack = f"DELETED USER: {request.id}\n"
            try:
                message_stomp = f"\nDELETED USER: {request.id}\n"
                self.conn.send(destination = self.dest_send, body = message_stomp)
            except Exception as e:
                print(f"STOMP ERROR: {e}")

            return delete_response
    


# funzione serve per il running del server
def serve(conn, dest_send):
    conn.connect(wait= True)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers= 50))
    UserManager_pb2_grpc.add_UserManagerServicer_to_server(UserManagerServicer(conn, dest_send), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("Grpc Server Running\n")
    server.wait_for_termination()




if __name__ == "__main__":
    conn = stomp.Connection([("activemq", 61613)], auto_content_length= False)
    dest_send = "/queue/notifyservice"
    serve(conn, dest_send)
   