"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import google.protobuf.descriptor
import google.protobuf.internal.enum_type_wrapper
import google.protobuf.message
import typing
import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

class _SexType:
    ValueType = typing.NewType('ValueType', builtins.int)
    V: typing_extensions.TypeAlias = ValueType
class _SexTypeEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[_SexType.ValueType], builtins.type):
    DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
    man: _SexType.ValueType  # 0
    women: _SexType.ValueType  # 1
class SexType(_SexType, metaclass=_SexTypeEnumTypeWrapper):
    pass

man: SexType.ValueType  # 0
women: SexType.ValueType  # 1
global___SexType = SexType


class CreateUserRequest(google.protobuf.message.Message):
    """create user"""
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    UID_FIELD_NUMBER: builtins.int
    USER_NAME_FIELD_NUMBER: builtins.int
    PASSWORD_FIELD_NUMBER: builtins.int
    SEX_FIELD_NUMBER: builtins.int
    uid: typing.Text
    """p2p: {"miss_default": true, "example": "10086", "title": "UID", "description": "user union id"}"""

    user_name: typing.Text
    """p2p: {"description": "user name"}
    p2p: {"default": "", "min_length": 1, "max_length": "10", "example": "so1n"}
    """

    password: typing.Text
    """p2p: {"description": "user password"}
    p2p: {"alias": "pw", "min_length": 6, "max_length": 18, "example": "123456"}
    """

    sex: global___SexType.ValueType
    def __init__(self,
        *,
        uid: typing.Text = ...,
        user_name: typing.Text = ...,
        password: typing.Text = ...,
        sex: global___SexType.ValueType = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["password",b"password","sex",b"sex","uid",b"uid","user_name",b"user_name"]) -> None: ...
global___CreateUserRequest = CreateUserRequest

class DeleteUserRequest(google.protobuf.message.Message):
    """delete user"""
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    UID_FIELD_NUMBER: builtins.int
    uid: typing.Text
    def __init__(self,
        *,
        uid: typing.Text = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["uid",b"uid"]) -> None: ...
global___DeleteUserRequest = DeleteUserRequest

class LoginUserRequest(google.protobuf.message.Message):
    """login user"""
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    UID_FIELD_NUMBER: builtins.int
    PASSWORD_FIELD_NUMBER: builtins.int
    uid: typing.Text
    password: typing.Text
    def __init__(self,
        *,
        uid: typing.Text = ...,
        password: typing.Text = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["password",b"password","uid",b"uid"]) -> None: ...
global___LoginUserRequest = LoginUserRequest

class LoginUserResult(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    UID_FIELD_NUMBER: builtins.int
    USER_NAME_FIELD_NUMBER: builtins.int
    TOKEN_FIELD_NUMBER: builtins.int
    uid: typing.Text
    """p2p: {"example": "10086", "title": "UID", "description": "user union id"}"""

    user_name: typing.Text
    """p2p: {"description": "user name"}
    p2p: {"default": "", "min_length": 1, "max_length": "10", "example": "so1n"}
    """

    token: typing.Text
    """p2p: {"description": "user token"}"""

    def __init__(self,
        *,
        uid: typing.Text = ...,
        user_name: typing.Text = ...,
        token: typing.Text = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["token",b"token","uid",b"uid","user_name",b"user_name"]) -> None: ...
global___LoginUserResult = LoginUserResult

class LogoutUserRequest(google.protobuf.message.Message):
    """logout user"""
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    UID_FIELD_NUMBER: builtins.int
    TOKEN_FIELD_NUMBER: builtins.int
    uid: typing.Text
    token: typing.Text
    """p2p: {"enable": false}"""

    def __init__(self,
        *,
        uid: typing.Text = ...,
        token: typing.Text = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["token",b"token","uid",b"uid"]) -> None: ...
global___LogoutUserRequest = LogoutUserRequest

class GetUidByTokenRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    TOKEN_FIELD_NUMBER: builtins.int
    token: typing.Text
    def __init__(self,
        *,
        token: typing.Text = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["token",b"token"]) -> None: ...
global___GetUidByTokenRequest = GetUidByTokenRequest

class GetUidByTokenResult(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    UID_FIELD_NUMBER: builtins.int
    uid: typing.Text
    def __init__(self,
        *,
        uid: typing.Text = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["uid",b"uid"]) -> None: ...
global___GetUidByTokenResult = GetUidByTokenResult
