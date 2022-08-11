import graphlib
from django.shortcuts import render
from django.conf import settings
import requests
from rest_framework.decorators import api_view, permission_classes
import json
from rest_framework.response import Response


ms_identity_web = settings.MS_IDENTITY_WEB
'''
store the authorization token in auth_holder once we have a successful result
'''
auth_holder = ''


def index(request):
    return render(request, "auth/status.html")

@ms_identity_web.login_required
def token_details(request):
    return render(request, 'auth/token.html')

@ms_identity_web.login_required
def call_ms_graph(request):
    ms_identity_web.acquire_token_silently()
    graph = 'https://graph.microsoft.com/v1.0/users'
    authZ = f'Bearer {ms_identity_web.id_data._access_token}'
    print(authZ)
    auth_holder = authZ.copy()
    results = requests.get(graph, headers={'Authorization': authZ}).json()

    # trim the results down to 5 and format them.
    if 'value' in results:
        results ['num_results'] = len(results['value'])
        results['value'] = results['value'][:5]

    return render(request, 'auth/call-graph.html', context=dict(results=results))

@api_view(['GET'])
def get_plans(request):
    temp_group_id = '74402ac4-9af3-4da5-a54e-1244b4bc5dbd'
    graph = f'https://graph.microsoft.com/v1.0/groups/{temp_group_id}/planner/plans'
    results = requests.get(graph, headers={'Authorization': auth_holder}).json()
    print(results)
    return Response(results)
