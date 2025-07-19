from rest_framework.decorators import api_view
from rest_framework.response import Response

USERS = {
    1: {'id': 1, 'name': 'Ali', 'email': 'ali132@gmail.com'},
    2: {'id': 2, 'name': 'Vali', 'email': 'aysel446@gmail.com'},
    3: {'id': 3, 'name': 'Elvin', 'email': 'elvin21@gmail.com'},
    4: {'id': 4, 'name': 'Selcan', 'email': 'selcan55@gmail.com'},
    5: {'id': 5, 'name': 'Nigar', 'email': 'nigar2001@gmail.com'},
    6: {'id': 6, 'name': 'Anar', 'email': 'anar2890@gmail.com'},
}

@api_view(['GET'])
def debug_view(request, id, word):
    my_param = request.query_params.get('my_param')
    return Response({"message": f"This is a debug view with the id {id} and word {word}.\nQuery parameters: {my_param}"}) 

@api_view(['GET'])
def user_list(request):
    name = request.query_params.get('name')
    users = USERS.values()
    if name:
        users = [user for user in users if user['name'] == name]
    return Response(users)

@api_view(['GET'])
def user_detail(request, id):
    user = USERS.get(id)
    if not user:
        return Response({"error": "User not found"}, status=404)
    return Response(user)
