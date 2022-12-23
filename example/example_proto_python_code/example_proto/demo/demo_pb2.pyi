"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import example_proto.common.single_pb2
import google.protobuf.descriptor
import google.protobuf.empty_pb2
import google.protobuf.internal.containers
import google.protobuf.internal.enum_type_wrapper
import google.protobuf.message
import google.protobuf.timestamp_pb2
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


class UserMessage(google.protobuf.message.Message):
    """user info"""
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    UID_FIELD_NUMBER: builtins.int
    AGE_FIELD_NUMBER: builtins.int
    HEIGHT_FIELD_NUMBER: builtins.int
    SEX_FIELD_NUMBER: builtins.int
    DEMO_FIELD_NUMBER: builtins.int
    IS_ADULT_FIELD_NUMBER: builtins.int
    USER_NAME_FIELD_NUMBER: builtins.int
    DEMO_MESSAGE_FIELD_NUMBER: builtins.int
    uid: typing.Text
    """p2p: {"miss_default": true, "example": "10086", "title": "UID", "description": "user union id"}"""

    age: builtins.int
    """p2p: {"example": 18, "title": "use age", "ge": 0}"""

    height: builtins.float
    """p2p: {"ge": 0, "le": 2.5}"""

    sex: global___SexType.ValueType
    demo: example_proto.common.single_pb2.DemoEnum.ValueType
    is_adult: builtins.bool
    user_name: typing.Text
    """p2p: {"description": "user name"}
    p2p: {"default": "", "min_length": 1, "max_length": "10", "example": "so1n"}
    """

    @property
    def demo_message(self) -> example_proto.common.single_pb2.DemoMessage: ...
    def __init__(self,
        *,
        uid: typing.Text = ...,
        age: builtins.int = ...,
        height: builtins.float = ...,
        sex: global___SexType.ValueType = ...,
        demo: example_proto.common.single_pb2.DemoEnum.ValueType = ...,
        is_adult: builtins.bool = ...,
        user_name: typing.Text = ...,
        demo_message: typing.Optional[example_proto.common.single_pb2.DemoMessage] = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["demo_message",b"demo_message"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["age",b"age","demo",b"demo","demo_message",b"demo_message","height",b"height","is_adult",b"is_adult","sex",b"sex","uid",b"uid","user_name",b"user_name"]) -> None: ...
global___UserMessage = UserMessage

class MapMessage(google.protobuf.message.Message):
    """test map message and bad message"""
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    class UserMapEntry(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor
        KEY_FIELD_NUMBER: builtins.int
        VALUE_FIELD_NUMBER: builtins.int
        key: typing.Text
        @property
        def value(self) -> global___UserMessage: ...
        def __init__(self,
            *,
            key: typing.Text = ...,
            value: typing.Optional[global___UserMessage] = ...,
            ) -> None: ...
        def HasField(self, field_name: typing_extensions.Literal["value",b"value"]) -> builtins.bool: ...
        def ClearField(self, field_name: typing_extensions.Literal["key",b"key","value",b"value"]) -> None: ...

    class UserFlagEntry(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor
        KEY_FIELD_NUMBER: builtins.int
        VALUE_FIELD_NUMBER: builtins.int
        key: typing.Text
        value: builtins.bool
        def __init__(self,
            *,
            key: typing.Text = ...,
            value: builtins.bool = ...,
            ) -> None: ...
        def ClearField(self, field_name: typing_extensions.Literal["key",b"key","value",b"value"]) -> None: ...

    USER_MAP_FIELD_NUMBER: builtins.int
    USER_FLAG_FIELD_NUMBER: builtins.int
    @property
    def user_map(self) -> google.protobuf.internal.containers.MessageMap[typing.Text, global___UserMessage]: ...
    @property
    def user_flag(self) -> google.protobuf.internal.containers.ScalarMap[typing.Text, builtins.bool]: ...
    def __init__(self,
        *,
        user_map: typing.Optional[typing.Mapping[typing.Text, global___UserMessage]] = ...,
        user_flag: typing.Optional[typing.Mapping[typing.Text, builtins.bool]] = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["user_flag",b"user_flag","user_map",b"user_map"]) -> None: ...
global___MapMessage = MapMessage

class RepeatedMessage(google.protobuf.message.Message):
    """test repeated msg"""
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    STR_LIST_FIELD_NUMBER: builtins.int
    INT_LIST_FIELD_NUMBER: builtins.int
    USER_LIST_FIELD_NUMBER: builtins.int
    @property
    def str_list(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[typing.Text]:
        """p2p: {"min_items": 3, "max_items": 5}"""
        pass
    @property
    def int_list(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.int]:
        """p2p: {"min_items": 1, "max_items": 5, "unique_items": true}"""
        pass
    @property
    def user_list(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___UserMessage]: ...
    def __init__(self,
        *,
        str_list: typing.Optional[typing.Iterable[typing.Text]] = ...,
        int_list: typing.Optional[typing.Iterable[builtins.int]] = ...,
        user_list: typing.Optional[typing.Iterable[global___UserMessage]] = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["int_list",b"int_list","str_list",b"str_list","user_list",b"user_list"]) -> None: ...
global___RepeatedMessage = RepeatedMessage

class NestedMessage(google.protobuf.message.Message):
    """test nested message"""
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    class _IncludeEnum:
        ValueType = typing.NewType('ValueType', builtins.int)
        V: typing_extensions.TypeAlias = ValueType
    class _IncludeEnumEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[NestedMessage._IncludeEnum.ValueType], builtins.type):
        DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
        zero: NestedMessage._IncludeEnum.ValueType  # 0
        one: NestedMessage._IncludeEnum.ValueType  # 1
        two: NestedMessage._IncludeEnum.ValueType  # 2
    class IncludeEnum(_IncludeEnum, metaclass=_IncludeEnumEnumTypeWrapper):
        pass

    zero: NestedMessage.IncludeEnum.ValueType  # 0
    one: NestedMessage.IncludeEnum.ValueType  # 1
    two: NestedMessage.IncludeEnum.ValueType  # 2

    class UserPayMessage(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor
        BANK_NUMBER_FIELD_NUMBER: builtins.int
        EXP_FIELD_NUMBER: builtins.int
        UUID_FIELD_NUMBER: builtins.int
        bank_number: typing.Text
        """p2p: {"type": "p2p@import|pydantic.types|PaymentCardNumber"}"""

        @property
        def exp(self) -> google.protobuf.timestamp_pb2.Timestamp:
            """p2p: {"default_factory": "p2p@local|exp_time"}"""
            pass
        uuid: typing.Text
        """p2p: {"default_factory": "p2p@local|uuid4"}"""

        def __init__(self,
            *,
            bank_number: typing.Text = ...,
            exp: typing.Optional[google.protobuf.timestamp_pb2.Timestamp] = ...,
            uuid: typing.Text = ...,
            ) -> None: ...
        def HasField(self, field_name: typing_extensions.Literal["exp",b"exp"]) -> builtins.bool: ...
        def ClearField(self, field_name: typing_extensions.Literal["bank_number",b"bank_number","exp",b"exp","uuid",b"uuid"]) -> None: ...

    class UserListMapEntry(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor
        KEY_FIELD_NUMBER: builtins.int
        VALUE_FIELD_NUMBER: builtins.int
        key: typing.Text
        @property
        def value(self) -> global___RepeatedMessage: ...
        def __init__(self,
            *,
            key: typing.Text = ...,
            value: typing.Optional[global___RepeatedMessage] = ...,
            ) -> None: ...
        def HasField(self, field_name: typing_extensions.Literal["value",b"value"]) -> builtins.bool: ...
        def ClearField(self, field_name: typing_extensions.Literal["key",b"key","value",b"value"]) -> None: ...

    class UserMapEntry(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor
        KEY_FIELD_NUMBER: builtins.int
        VALUE_FIELD_NUMBER: builtins.int
        key: typing.Text
        @property
        def value(self) -> global___MapMessage: ...
        def __init__(self,
            *,
            key: typing.Text = ...,
            value: typing.Optional[global___MapMessage] = ...,
            ) -> None: ...
        def HasField(self, field_name: typing_extensions.Literal["value",b"value"]) -> builtins.bool: ...
        def ClearField(self, field_name: typing_extensions.Literal["key",b"key","value",b"value"]) -> None: ...

    USER_LIST_MAP_FIELD_NUMBER: builtins.int
    USER_MAP_FIELD_NUMBER: builtins.int
    USER_PAY_FIELD_NUMBER: builtins.int
    INCLUDE_ENUM_FIELD_NUMBER: builtins.int
    NOT_ENABLE_USER_PAY_FIELD_NUMBER: builtins.int
    EMPTY_FIELD_NUMBER: builtins.int
    @property
    def user_list_map(self) -> google.protobuf.internal.containers.MessageMap[typing.Text, global___RepeatedMessage]: ...
    @property
    def user_map(self) -> google.protobuf.internal.containers.MessageMap[typing.Text, global___MapMessage]: ...
    @property
    def user_pay(self) -> global___NestedMessage.UserPayMessage: ...
    include_enum: global___NestedMessage.IncludeEnum.ValueType
    @property
    def not_enable_user_pay(self) -> global___NestedMessage.UserPayMessage:
        """p2p: {"enable": false}"""
        pass
    @property
    def empty(self) -> google.protobuf.empty_pb2.Empty: ...
    def __init__(self,
        *,
        user_list_map: typing.Optional[typing.Mapping[typing.Text, global___RepeatedMessage]] = ...,
        user_map: typing.Optional[typing.Mapping[typing.Text, global___MapMessage]] = ...,
        user_pay: typing.Optional[global___NestedMessage.UserPayMessage] = ...,
        include_enum: global___NestedMessage.IncludeEnum.ValueType = ...,
        not_enable_user_pay: typing.Optional[global___NestedMessage.UserPayMessage] = ...,
        empty: typing.Optional[google.protobuf.empty_pb2.Empty] = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["empty",b"empty","not_enable_user_pay",b"not_enable_user_pay","user_pay",b"user_pay"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["empty",b"empty","include_enum",b"include_enum","not_enable_user_pay",b"not_enable_user_pay","user_list_map",b"user_list_map","user_map",b"user_map","user_pay",b"user_pay"]) -> None: ...
global___NestedMessage = NestedMessage