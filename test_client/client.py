import requests
import random
import json
from time import sleep

base_url = "http://localhost:5000"


if __name__ == "__main__":
    print("testing running...\n")



    sleep(1)

#-------------------------------------------------
    print("creating new tester user...\n")
    sleep(1)
    random_user = random.randint(1,999)
    add_testing_dic = {
        "email" : f"TesterUser{random_user}@mail.it",
        "name" : f"Tester Guy {random_user}"
    }

    post_response = requests.post(url= f"{base_url}/users", json= add_testing_dic)
    if(post_response.status_code == 201):
        
        post_msg = post_response.json()
        print(post_msg.get("message", ""))
        sleep(1)
        extracted_id = post_msg.get("id")
    else:
        print(f"post went wrong!\n{post_response.json()}")
        exit()


#------------------------------------------------
    print("Getting Users list")
    sleep(2)
    get_response = requests.get(url= f"{base_url}/users")
    if(get_response.status_code == 200):
        get_msg = get_response.json()
 
        print(json.dumps(get_msg, indent= 4))
        sleep(1)
    else:
        print(f"get went wrong!\n{get_response.json()}")


#---------------------------------------------------
    print("\nGetting selected User info\n")
    sleep(2)
    get_user_response = requests.get(url= f"{base_url}/users/{extracted_id}")
    if(get_user_response.status_code == 200):
        get_user_msg = get_user_response.json()

        print(get_user_msg.get("message", ""))
        sleep(1)
    else:
        print(f"get user went wrong!\n{get_user_response.json()}")


#-----------------------------------------------------

    print("Deleting selected User\n")
    sleep(2)
    delete_response = requests.delete(url= f"{base_url}/users/{extracted_id}")
    if(delete_response.status_code == 200):
        delete_msg = delete_response.json()

        print(delete_msg.get("message", ""))
        sleep(1)
    else:
        print(f"delete went wrong!\n{delete_response.json()}")

