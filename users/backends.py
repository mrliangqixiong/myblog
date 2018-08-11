from .models import User


class EmailBackend(object):
    def authenticate(self, request, **credentials):
        # 要注意登录表单中用户输入的用户名或者邮箱的field 名均为 username
        # 先获取email,
        email = credentials.get('email', credentials.get('username', ''))
        # 再根据email去取对象,如果能取到,则校验密码,如果取不到则报DoesNotExist的异常
        if email:
            # email存在则去取对象
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                pass
            else:
                # 取到了对象
                # 校验密码
                if user.check_password(credentials['password']):
                    # 校验密码通过,则返回user对象
                    return user

    def get_user(self, user_id):
        # 该方法必须的
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
