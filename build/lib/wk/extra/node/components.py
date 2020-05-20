from wk.extra.node import *

def html(args):
    default_args=dict(
        title='Html Demo',
        contents=''
    )
    smart_update_dict(default_args,args)
    args = default_args
    return Html()([
        Head()([
            Meta(charset='utf-8'),
            Title()(args['title']),
        ]),
        Body()(args['contents'])
    ])

def form_demo(args={}):
    default_args=dict(
        action='',method='post',style='background-color:#1D93EC;color:white',
        username=dict(type='text',name='username',placeholder='username'),
        password=dict(type='password',name='password',placeholder='password'),
        submit_btn=dict(type='submit',style="background-color:#1D93EC;color:white")
    )
    smart_update_dict(default_args,args)
    args=default_args
    username=args.pop('username')
    password=args.pop('password')
    submit_btn=args.pop('submit_btn')

    return Form(**args)([
        Label()(Input(**username)),
        Label()(Input(**password)),
        Button(**submit_btn)("Submit")
    ])


if __name__ == '__main__':
    x = Node()('hi')
    # x = html("hi")
    # x = form_demo()
    x = html(dict(
        contents=[
            Div(style='background-color:#1D93EC;color:white;min-height:50px')([
                form_demo(dict(
                    username=dict(placeholder="input your username...")
                ))
            ])
        ]
    ))
    x.to_file(r'D:\work\wk\data/test.html')
    print(x)



