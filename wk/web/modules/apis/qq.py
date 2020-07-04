import requests,json
def get_openid(data):
    url = 'https://graph.qq.com/oauth2.0/me'
    body = {'access_token': data.get('access_token')}
    response = requests.get(url, params=body)
    open_id = json.loads(response.text[10:-4])
    open_id = open_id.get('openid')
    requests.session().close()
    return open_id


def get_user_info(data, open_id,appid):
    url = 'https://graph.qq.com/user/get_user_info'
    body = {'access_token': data.get('access_token'), 'oauth_consumer_key': appid, 'openid': open_id}
    response = requests.get(url, params=body)
    user_info = response.json()
    requests.session().close()
    return user_info
