from wk import gen_sms_code
import json
class AliyunSmsService:
    def __init__(self,access_key_id=None,access_secret=None,debug=True):
        self.access_key_id=access_key_id
        self.access_secret=access_secret
        self.debug=debug

        pass
    def send_to(self, phone_number):
        ''''send'''
        if self.debug :
            return '123456'
        code = gen_sms_code(6)
        from aliyunsdkcore.client import AcsClient
        from aliyunsdkcore.request import CommonRequest
        client = AcsClient(self.access_key_id, self.access_secret, 'cn-hangzhou')
        request = CommonRequest()
        request.set_accept_format('json')
        request.set_domain('dysmsapi.aliyuncs.com')
        request.set_method('POST')
        request.set_protocol_type('https')  # https | http
        request.set_version('2017-05-25')
        request.set_action_name('SendSms')

        request.add_query_param('RegionId', "cn-hangzhou")
        request.add_query_param('PhoneNumbers', phone_number)
        request.add_query_param('SignName', '知识树')
        request.add_query_param('TemplateCode', 'SMS_194635024')
        request.add_query_param('TemplateParam', json.dumps({'code':code}))

        response = client.do_action_with_exception(request)
        # python2:  print(response)
        # print(str(response, encoding='utf-8'))
        return code
