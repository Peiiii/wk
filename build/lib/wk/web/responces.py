import json
from flask import current_app
class JsonResponse(dict):
    def __init__(self, success=None,code=None,message=None,data=None,action=None,params=None):
        super().__init__(success=success,code=code,message=message,data=data,action=action,params=params)
    def jsonify(self):
        response = current_app.response_class(
            response=json.dumps(self,ensure_ascii=False,indent=2),
            status=200,
            mimetype='application/json'
        )
        return response
class ActionResponse(JsonResponse):
    def __init__(self,action,params={},data=None,message=None,success=None,code=None):
        super().__init__(action=action,params=params,data=data,message=message,success=success,code=code)

class ActionRedirect(ActionResponse):
    def __init__(self,location=None,success=True,message=None,target=None):
        target=location or target
        assert target
        params=dict(location=target)
        super().__init__(action='redirect',params=params,success=success,message=message)
class ActionRefresh(ActionResponse):
    def __init__(self,success=True,message=None):
        super().__init__(action='refresh',success=success,message=message)
class StatusResponse(JsonResponse):
    def __init__(self,success=True,message="success",code=0,data=None,*args,**kwargs):
        super().__init__(success=success,message=message,code=code,data=data,*args,**kwargs)
class StatusSuccessResponce(StatusResponse):
    def __init__(self,success=True,message="success",code=0,data=None,*args,**kwargs):
        super().__init__(success=success,message=message,code=code,data=data,*args,**kwargs)
class StatusErrorResponse(StatusResponse):
    def __init__(self,success=False,message="failure",code=-1,data=None,*args,**kwargs):
        super().__init__(success=success,message=message,code=code,data=data,*args,**kwargs)
