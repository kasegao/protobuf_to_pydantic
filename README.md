# protobuf_to_pydantic
Generate the `pydantic.BaseModel` class (and the corresponding source code) with parameter verification function through the Protobuf file

> NOTE:
>  - Only supports proto3

[中文文档](https://github.com/so1n/protobuf_to_pydantic/blob/master/README_ZH.md)

> Current version 0.2.0 is under development, available version is [v0.1.7.4](https://github.com/so1n/protobuf_to_pydantic/tree/v0.1.7.4)

# 1.Installation
```bash
pip install protobuf_to_pydantic
```

# 2.Quick Start
`protobuf_to_pydantic` currently has two methods to generate `pydantic.BaseModel` objects through Protobuf files,
The first method is to generate the corresponding `Python` code file through the Protobuf file in the form of a plugin.
The second method is to generate the corresponding `pydantic.BaseModel` object based on the `Message` object at runtime.

## 2.1.Directly generate `pydantic.BaseModel` code files through plugins
> Note: The `protobuf-to-pydantic` plugin depends on `mypy-protobuf`, please install `mypy-protobuf` through the command `python -m pip install protobuf-to-pydantic[mypy-protobuf]`.
### 2.1.1.Use of plugin
The plugin method is the most recommended way to use `protobuf-to-pydantic`,
it supports the most complete functions, and it is also very simple to use, assuming that the code corresponding to the Protobuf file is usually generated by the following command:
```bash
python -m grpc_tools.protoc -I. example.proto
```
Then after installing `protobuf-to-pydantic`, can use the `--protobuf-to-pydantic out` option to use `protobuf-to-pydantic`, the command is as follows:
```bash
python -m grpc_tools.protoc -I. --protobuf-to-pydantic_out=. example.proto
```

Among them, `--protobuf-to-pydantic out=.` indicates the use of the `prorobuf-to-pydantic` plugin, and declares that the output location of the `protobuf-to-pydantic` plugin is `.` (indicating the use of `grpc tools.proto ` to use the output path),
In this way, the `protobuf-to-pydantic` plugin will write its own generated content in the corresponding file (the file name ends with `p2p.py`), such as `protobuf-to-pydantic` is `example.proto `The generated code file is named `example_p2p.py`

### 2.1.2.Plugin configuration
`protobuf-to-pydantic` supports configuration functions by reading a `Python` file.
Developers first need to create a configuration file in the current path of the running command, the file name is `plugin_config.py`, and write the following code:

```Python
import logging
from typing import List, Type

from google.protobuf.any_pb2 import Any  # type: ignore
from pydantic import confloat, conint
from pydantic.fields import FieldInfo

from protobuf_to_pydantic.desc_template import DescTemplate

# Configure the log output format and log level of the plugin, which is very useful when debugging
logging.basicConfig(format="[%(asctime)s %(levelname)s] %(message)s", datefmt="%y-%m-%d %H:%M:%S", level=logging.DEBUG)


class CustomerField(FieldInfo):
    pass


def customer_any() -> Any:
    return Any  # type: ignore


# For the configuration of the local template, see the use of the local template for details
local_dict = {
    "CustomerField": CustomerField,
    "confloat": confloat,
    "conint": conint,
    "customer_any": customer_any,
}
# Specifies the start of key comments
comment_prefix = "p2p"
# Specify the class of the template, you can extend the template by inheriting this class, see the chapter on custom templates for details
desc_template: Type[DescTemplate] = DescTemplate
# Specify the protobuf files of which packages to ignore, and the messages of the ignored packages will not be parsed
ignore_pkg_list: List[str] = ["validate", "p2p_validate"]
# Specifies the generated file name suffix (without .py)
file_name_suffix = "_p2p"
```
Next, change `--protobuf-to-pydantic out=.` in the command to `--protobuf-to-pydantic out=config path=plugin config.py:.`, as follows:
```bash
python -m grpc_tools.protoc -I. --protobuf-to-pydantic_out=config_path=plugin_config.py:. example.proto
```
Among them, `config path=plugin_config.py` on the left side of `:` indicates that the configuration file path to be read is `plugin_config.py`, and the right side of `:` still declares the output of the `protobuf-to-pydantic` plugin The position is `.`.
In this way, the `protobuf-to-pydantic` plugin can be loaded into the configuration file specified by the developer when it is running, and then run according to the configuration defined by the configuration file.

> Note: 更多配置内容见`protobuf_to_pydantic/plugin/config.py`文件
> Note: For more information on configuration, see the 'protobuf_to_pydantic/plugin/config.py'
## 2.2.Generate a `pydantic.BaseModel` object at runtime
`protobuf_to_pydantic` can generate the corresponding `pydantic.BaseModel` object based on the `Message` object at runtime。

For example, the `UserMessage` in the following Protobuf file named `demo.proto`:
```protobuf
// path: ./demo.proto
syntax = "proto3";
package user;

enum SexType {
  man = 0;
  women = 1;
}

message UserMessage {
  string uid=1;
  int32 age=2;
  float height=3;
  SexType sex=4;
  bool is_adult=5;
  string user_name=6;
}
```
Through `grpc_tools.protoc`, the corresponding `Python` code can be generated according to the Protobuf file (the file name at this time is `demo_pb2.py`),
and the `msg_to_pydantic_model` method of `protobuf_to_pydantic` can read the generated Proto file at runtime Message object data,
and generate the corresponding `pydantic.BaseModel` object:

```Python
from typing import Type
from protobuf_to_pydantic import msg_to_pydantic_model
from pydantic import BaseModel

# import protobuf gen python obj
from . import demo_pb2

UserModel: Type[BaseModel] = msg_to_pydantic_model(demo_pb2.UserMessage)
print(
    {
        k: v.field_info
        for k, v in UserModel.__fields__.items()
    }
)

# output
# {
#   'uid': FieldInfo(default='', extra={}),
#   'age': FieldInfo(default=0, extra={}),
#   'height': FieldInfo(default=0.0, extra={}),
#   'sex': FieldInfo(default=0, extra={}),
#   'is_adult': FieldInfo(default=False, extra={}),
#   'user_name': FieldInfo(default='', extra={})
#  }
```
Through the output results, it can be found that the generated `pydantic.BaseModel` object also contains `uid`, `age`, `height`, `sex`, `is adult` and `user name` fields, and their corresponding `default` The information is consistent with the `UserMessage` in the Protobuf file.

In addition to generating the corresponding `pydantic.BaseModel` object at runtime, `protobuf-to-pydantic` also supports converting the `pydantic.BaseModel` object to the corresponding `Python` code text at runtime (only compatible with `protobuf_to_pydantic `generated `pydantic.BaseModel` object).
Among them, the `pydantic_model_to_py_code` method of `protobuf_to_pydantic` is used to generate code text, and the `pydantic_model_to_py_file` method of `protobuf_to_pydantic` is used to generate code files,
the sample code of `pydantic_model_to_py_file` method of `protobuf_to_pydantic` is as follows:
```Python
from protobuf_to_pydantic import msg_to_pydantic_model, pydantic_model_to_py_file

# import protobuf gen python obj
from example.example_proto_python_code.example_proto.demo import demo_pb2

pydantic_model_to_py_file(
    "./demo_gen_code.py",
    msg_to_pydantic_model(demo_pb2.NestedMessage),
)
```
The code will first convert `demo_pb2.NestedMessage` into a `pydantic.BaseModel` object, and then the generated object will be converted into the corresponding code content by the `pydantic_model_to_py_file` method and written to `demo_gen_code.py` file.

## 2.3.Parameter verification
The `Message` object generated according to the Protobuf file will only carry a small amount of information. This is because the ordinary Protobuf file does not have enough parameter verification related information, which requires us to improve the parameter verification information of the `Message` object through some additional ways.
Currently `protobuf_to_pydantic` supports multiple ways to obtain other information of the Message, so that the generated `pydantic.BaseModel` object has the function of parameter verification.

> NOTE:
>  - 1.The text annotation function is not the focus of subsequent function development, and the P2P mode is recommended。
>  - 2.Plugin mode only supports PGV and P2P mode

### 2.3.1.Text annotation
Developers can write comments that meet the requirements of `protobuf_to_pydantic` for each field in the Protobuf file to provide parameter verification information for `protobuf_to_pydantic`, such as the following example:
```protobuf
syntax = "proto3";
package user;

enum SexType {
  man = 0;
  women = 1;
}

// user info
message UserMessage {
  // p2p: {"miss_default": true, "example": "10086"}
  // p2p: {"title": "UID"}
  string uid=1; // p2p: {"description": "user union id"}
  // p2p: {"example": 18, "title": "use age", "ge": 0}
  int32 age=2;
  // p2p: {"ge": 0, "le": 2.5}
  float height=3;
  SexType sex=4;
  bool is_adult=5;
  // p2p: {"description": "user name"}
  // p2p: {"default": "", "min_length": 1, "max_length": "10", "example": "so1n"}
  string user_name=6;
}
```
In this example, each annotation that can be used by `protobuf_to_pydantic` starts with `p2p:` (supports customization) and is followed by a complete Json string. If you are familiar with the usage of `pydantic`, you can find This Json string contains the verification information corresponding to `pydantic.Field`. For example, the `uid` field in `UserMessage` contains a total of 4 pieces of information as follows：

| Column       | Meaning                                                                               |
|--------------|---------------------------------------------------------------------------------------|
| miss_default | Indicates that the generated field does not have a default value                      |
| example      | An example value representing the generated field is 10086                            |
| title        | Indicates that the schema name of the field is UID                                    |
 | description  | The schema documentation for the representation field is described as `user_union_id` |

> Note:
>   - 1.Currently only single-line comments are supported and comments must be a complete Json data (no line breaks).
>   - 2.multi line comments are not supported。

When these annotations are written, `protobuf_to_pydantic` will bring the corresponding information for each field when converting the Message into the corresponding `Pydantic.BaseModel` object, as follows:

```python
from typing import Type
from protobuf_to_pydantic import msg_to_pydantic_model
from pydantic import BaseModel

# import protobuf gen python obj
from example.example_proto_python_code.example_proto.demo import demo_pb2

UserModel: Type[BaseModel] = msg_to_pydantic_model(demo_pb2.UserMessage, parse_msg_desc_method=demo_pb2)
print(
    {
        k: v.field_info
        for k, v in UserModel.__fields__.items()
    }
)
# output
# {
#   'uid': FieldInfo(default=PydanticUndefined, title='UID', description='user union id', extra={'example': '10086'}),
#   'age': FieldInfo(default=0, title='use age', ge=0, extra={'example': 18}),
#   'height': FieldInfo(default=0.0, ge=0, le=2, extra={}),
#   'sex': FieldInfo(default=0, extra={}),
#   'is_adult': FieldInfo(default=False, extra={}),
#   'user_name': FieldInfo(default='', description='user name', min_length=1, max_length=10, extra={'example': 'so1n'})
# }
```
It can be seen from the output results that the output fields carry the corresponding information. In addition, the difference between this code and the above is that the `msg_to_pydantic_model` function sets a keyword parameter named `parse_msg_desc_method` and its value is `demo_pb2`, which enables `protobuf_to_pydantic` to obtain additional information for each field in the Message object through comments in the `.pyi` file of the `demo_pb2` module.

> Note：This function requires the use of the [mypy-protobuf](https://github.com/nipunn1313/mypy-protobuf) plugin when generating the corresponding `Python` code from the Protobuf file, and the specified output path of the pyi file is the same as the generated `Python` code path to take effect at the same time.

In addition to obtaining comments through the `.pyi` file, `protobuf_to_pydantic` also supports setting the value of `parse_msg_desc_method` to the root directory path specified when the Message object is generated, so that `protobuf_to_pydantic` can parse the comments of the Protobuf file corresponding to the Message object. getting information。


For example, the project structure of the `protobuf_to_pydantic` sample code is as follows:
```bash
./protobuf_to_pydantic/
├── example/
│ ├── python_example_proto_code/
│ └── example_proto/
├── protobuf_to_pydantic/
└── /
```

The Protobuf file is stored in the `example/example_proto` folder, and then run the following command in the `example` directory to generate the `Python` code file corresponding to Protobuf:
```bash
cd example

python -m grpc_tools.protoc
  --python_out=./python_example_proto_code \
  --grpc_python_out=./python_example_proto_code \
  -I. \
```
Then the path to be filled in at this time is `./protobuf_to_pydantic/example`, the code is as follows：

```python
from typing import Type
from protobuf_to_pydantic import msg_to_pydantic_model
from pydantic import BaseModel

# import protobuf gen python obj
from example.example_proto_python_code.example_proto.demo import demo_pb2

UserModel: Type[BaseModel] = msg_to_pydantic_model(
    demo_pb2.UserMessage, parse_msg_desc_method="./protobuf_to_pydantic/example"
)
print(
    {
        k: v.field_info
        for k, v in UserModel.__fields__.items()
    }
)
# output
# {
#   'uid': FieldInfo(default=PydanticUndefined, title='UID', description='user union id', extra={'example': '10086'}),
#   'age': FieldInfo(default=0, title='use age', ge=0, extra={'example': 18}),
#   'height': FieldInfo(default=0.0, ge=0, le=2, extra={}),
#   'sex': FieldInfo(default=0, extra={}),
#   'is_adult': FieldInfo(default=False, extra={}),
#   'user_name': FieldInfo(default='', description='user name', min_length=1, max_length=10, extra={'example': 'so1n'})
# }
```
From the result, it can be seen that the information carried by the field is the same as the result obtained by the module
> NOTE: This method requires [lark](https://github.com/lark-parser/lark) to be installed in advance and the Protobuf file must exist in the running project.

### 2.3.2.PGV(protoc-gen-validate)
Currently, the commonly used object validation method in the Protobuf ecosystem is to directly use the [protoc-gen-validate](https://github.com/envoyproxy/protoc-gen-validate) project, while [protoc-gen-validate](https://github.com/envoyproxy/protoc-gen-validate) project also supports multiple languages, and most Protobuf developers will write `pgv` rules once so that different languages support the same validation rules.

And `protobuf-to-pydantic` also supports parsing the verification rules of `pgv` so that the generated `pydantic.BaseModel` class has corresponding verification logic,
It is very simple to use `Pgv` verification rules in `protobuf_to_pydantic`. First, you need to write the corresponding `Pgv` rules in the Protobuf file, and then fill in `parse_msg_desc_method` when converting through `msg_to_pydantic_model` method The value is `PGV`, the code is as follows:
```Python
from typing import Type
from protobuf_to_pydantic import msg_to_pydantic_model
from pydantic import BaseModel

# import protobuf gen python obj
from example.example_proto_python_code.example_proto.validate import demo_pb2

UserModel: Type[BaseModel] = msg_to_pydantic_model(
    demo_pb2.FloatTest, parse_msg_desc_method="PGV"
)
print(
    {
        k: v.field_info
        for k, v in UserModel.__fields__.items()
    }
)
# output
# {
#   'const_test': FieldInfo(default=1.0, const=True, extra={}),
#   'range_e_test': FieldInfo(default=0.0, ge=1, le=10, extra={}),
#   'range_test': FieldInfo(default=0.0, gt=1, lt=10, extra={}),
#   'in_test': FieldInfo(default=0.0, extra={'in': [1.0, 2.0, 3.0]}),
#   'not_in_test': FieldInfo(default=0.0, extra={'not_in': [1.0, 2.0, 3.0]}),
#   'ignore_test': FieldInfo(default=0.0, extra={})
# }
```

> Note:
>  - 1.For the usage of `Pgv`, see: [protoc-gen-validate doc](https://github.com/bufbuild/protoc-gen-validate/blob/main/README.md#constraint-rules)
>  - 2.Need to install `Pgv` through `pip install protoc_gen_validate` Or download [validate.proto](https://github.com/so1n/protobuf_to_pydantic/blob/master/example/example_proto/common/validate.proto) to the protobuf directory in the project to write pgv rules in the Protobuf file.


### 2.2.3.P2p
The verification rules of `Pgv` are written in the Option attribute of each field of `Message`, and there are better code specifications, so the readability of Protobuf files carrying `Pgv` verification rules is higher than that of Protobuf carrying comments At the same time, when writing `Pgv` rules, you can also experience the convenience brought by IDE auto-completion, but it only supports verification-related logic, and the feature richness is not as good as the file comment mode.

The `P2P` mode is an extension of the `PGV` mode, which incorporates some functions of text annotations. This mode satisfies the customization of the attributes of each `Field` in most `pydantic.BaseModel`, such as the following Protobuf file:
```protobuf
syntax = "proto3";
package p2p_validate_test;

import "example_proto/common/p2p_validate.proto";


message FloatTest {
  float const_test = 1 [(p2p_validate.rules).float.const = 1];
  float range_e_test = 2 [(p2p_validate.rules).float = {ge: 1, le: 10}];
  float range_test = 3[(p2p_validate.rules).float = {gt: 1, lt: 10}];
  float in_test = 4[(p2p_validate.rules).float = {in: [1,2,3]}];
  float not_in_test = 5[(p2p_validate.rules).float = {not_in: [1,2,3]}];
  float default_test = 6[(p2p_validate.rules).float.default = 1.0];
  float not_enable_test = 7[(p2p_validate.rules).float.enable = false];
  float default_factory_test = 8[(p2p_validate.rules).float.default_factory = "p2p@builtin|float"];
  float miss_default_test = 9[(p2p_validate.rules).float.miss_default = true];
  float alias_test = 10 [(p2p_validate.rules).float.alias = "alias"];
  float desc_test = 11 [(p2p_validate.rules).float.description = "test desc"];
  float multiple_of_test = 12 [(p2p_validate.rules).float.multiple_of = 3.0];
  float example_test = 13 [(p2p_validate.rules).float.example = 1.0];
  float example_factory = 14 [(p2p_validate.rules).float.example_factory = "p2p@builtin|float"];
  float field_test = 15[(p2p_validate.rules).float.field = "p2p@local|CustomerField"];
  float type_test = 16[(p2p_validate.rules).float.type = "p2p@local|confloat"];
  float title_test = 17 [(p2p_validate.rules).float.title = "title_test"];
}
```
`protobuf_to_pydantic` can read the generated Message object at runtime and generate a `pydantic.BaseModel` object with the corresponding information:

```python
from typing import Type
from protobuf_to_pydantic import msg_to_pydantic_model
from pydantic import BaseModel, confloat
from pydantic.fields import FieldInfo

# import protobuf gen python obj
from example.example_proto_python_code.example_proto.p2p_validate import demo_pb2


class CustomerField(FieldInfo):
    pass


DemoModel: Type[BaseModel] = msg_to_pydantic_model(
    demo_pb2.FloatTest,
    local_dict={"CustomerField": CustomerField, "confloat": confloat},
)
print(
    {
        k: v.field_info
        for k, v in DemoModel.__fields__.items()
    }
)
# output:
# {
#   'const_test': FieldInfo(default=1.0, const=True, extra={}),
#   'range_e_test': FieldInfo(default=0.0, ge=1, le=10, extra={}),
#   'range_test': FieldInfo(default=0.0, gt=1, lt=10, extra={}),
#   'in_test': FieldInfo(default=0.0, extra={'in': [1.0, 2.0, 3.0]}),
#   'not_in_test': FieldInfo(default=0.0, extra={'not_in': [1.0, 2.0, 3.0]}),
#   'default_test': FieldInfo(default=1.0, extra={}),
#   'default_factory_test': FieldInfo(default=PydanticUndefined, default_factory=<class 'float'>, extra={}),
#   'miss_default_test': FieldInfo(extra={}),
#   'alias_test': FieldInfo(default=0.0, alias='alias', alias_priority=2, extra={}),
#   'desc_test': FieldInfo(default=0.0, description='test desc', extra={}),
#   'multiple_of_test': FieldInfo(default=0.0, multiple_of=3, extra={}),
#   'example_test': FieldInfo(default=0.0, extra={'example': 1.0}),
#   'example_factory': FieldInfo(default=0.0, extra={'example': <class 'float'>}),
#   'field_test': CustomerField(default=0.0, extra={}),
#   'type_test': FieldInfo(default=0.0, extra={}),
#   'title_test': FieldInfo(default=0.0, title='title_test', extra={})
#   }
```
It is worth noting that this code does not explicitly specify that the value of `parse_msg_desc_method` is `p2p`, because `p2p` is already the default rule of `protobuf_to_pydantic`.

> Note: See the template chapter for the usage of `local_dict`

 > Note:
>  - 1.See the template chapter for the usage of `local_dict`
>  - 2.If the reference to the Proto file fails, you need to download [p2p_validate.proto](https://github.com/so1n/protobuf_to_pydantic/blob/master/protos/protobuf_to_pydantic/protos/p2p_validate.proto) in the project and use it in the Protobuf file。




### 2.3.3.Other parameter support
In addition to the parameters of `FieldInfo`, the file comment mode and `p2p` mode of `protobuf_to_pydantic` also support the following parameters:
- miss_default：By default, the default value of each field in the corresponding `pydantic.BaseModel` object is the same as the default value of each field in the Message, but when `miss default` is `true`, the setting of the default value will be canceled .
- enable: By default, `pydantic.BaseModel` will convert every field in the Message. If some fields do not want to be converted, you can set `enable` to `false`
- const: Specifies the value of the field's constant. Note: The const of `pydantic.BaseModel` only supports bool variables. When `const` is `True`, the accepted value can only be the value set by `default`, and the default value carried by the Message generated by protobuf corresponds to The null value of type does not match `pydantic.BaseModel`, so `protobuf_to_pydantic` makes some changes to the input of this value, but after `const` sets the value, the `cost` property in the generated field is `True` `, and `default` becomes the corresponding value of the setting.
- type: To expand the current type, for example, if you want to increase the verification of the bank card number through the `pydantic.types.Payment Card Number` type, you can specify the field type as `Payment Card Number` by the following method:
  ```protobuf
  // common example
  message UserPayMessage {
    string bank_number=1; // p2p: {"type": "p2p@import|pydantic.types|PaymentCardNumber"}
  }
  // p2p example
  message UserPayMessage {
    string bank_number=1[(p2p_validate.rules).string.type = "p2p@import|pydantic.types|PaymentCardNumber"];
  }
  ```

> Note:
>   If you don't know `pydantic`, you can use the following two URLs to learn what parameters Field supports:
>
>   - https://pydantic-docs.helpmanual.io/usage/types/#constrained-types
>
>   - https://pydantic-docs.helpmanual.io/usage/schema/#field-customization

### 2.3.4.Template
In some cases, the value we fill in is a method or function of a certain library in `Python` (such as the value of `type` parameter and `default_factory` parameter), which cannot be realized through Json syntax。
At this time, template parameters can be used to solve the corresponding problems. Currently `protobuf_to_pydantic` supports a variety of template parameters。

> Note:The `p2p` string at the beginning of the template can be defined by the comment prefix variable


#### 2.3.4.1.`p2p@import`
This template is used to indicate that the value is a variable under other modules. The specific usage method is as follows:
```protobuf
// comment example
message UserPayMessage {
  string bank_number=1; // p2p: {"type": "p2p@import|pydantic.types|PaymentCardNumber"}
}

// p2p example
message UserPayMessage {
  string bank_number=1[(p2p_validate.rules).string.type = "p2p@import|pydantic.types|PaymentCardNumber"];
}

// p2p other example
// Since the imported type happens to belong to the `pydantic.types` module, string.pydantic type can be used directly in `p2p` mode
message UserPayMessage {
  string bank_number=1[(p2p_validate.rules).string.pydantic_type = "PaymentCardNumber"];
}
```

The syntax in the format of `p2p{template method}|{module to be imported: A}|{variable in the module: B}` is used here, which means that `B` object needs to be imported and applied through `from A import B` ,
Through the definition of the template, `protobuf_to_pydantic` will convert the corresponding Message into the following `pydantic.BaseModel`:
```python
from pydantic import BaseModel
from pydantic.fields import FieldInfo
# p2p@import|pydantic.types|PaymentCardNumber
from pydantic.types import PaymentCardNumber

class UserPayMessage(BaseModel):
    bank_number: PaymentCardNumber = FieldInfo(default="", extra={})
```

#### 2.3.4.2.`p2p@import_instance`
The `p2p@import` template just imports and uses the variables of a certain library, while `p2p@import instance` imports the class of a certain library first,
and finally instantiates it with the specified parameters. The method of use is as follows:
```protobuf
message AnyTest {
  google.protobuf.Any default_test = 23 [
    (p2p_validate.rules).any.default = 'p2p@import_instance|google.protobuf.any_pb2|Any|{"type_url": "type.googleapis.com/google.protobuf.Duration"}'

  ];
}
```
Here is the `p2p{template method}|{module to be imported}|{corresponding class}|{corresponding parameter}` syntax, through the definition of the template, `protobuf_to_pydantic` will convert the corresponding Message is the following `pydantic.BaseModel` object:
```python
from google.protobuf.any_pb2 import Any as AnyMessage
from pydantic import BaseModel
from pydantic.fields import FieldInfo


class AnyTest(BaseModel):
    default_test: AnyMessage = FieldInfo(
        default=AnyMessage(type_url="type.googleapis.com/google.protobuf.Duration")
    )
```

#### 2.3.4.3.`p2p@local`
This template is used to introduce user-defined variables. The syntax in the format `{template method}|{local variable to be used}` is used here, as follows:
```protobuf
// comment example
message UserPayMessage {
  google.protobuf.Timestamp exp=1; // p2p: {"default_factory": "p2p@local|exp_time"}
}
// p2p example
message UserPayMessage {
  google.protobuf.Timestamp exp=1[(p2p_validate.rules).timestamp.default_factory= "p2p@local|exp_time"];
}
```
Then register the corresponding value through the parameter `local_dict` when calling the `msg_to_pydantic_model` method. The fake code is as follows:
```Python
import time


def exp_time() -> float:
  return time.time()

msg_to_pydantic_model(
    demo_pb2.NestedMessage,
    local_dict={"exp_time": exp_time},  # <----
)
```
In this way, `protobuf_to_pydantic` can generate a `pydantic.BaseModel` object that meets the requirements:
```python
from datetime import datetime
from pydantic import BaseModel
from pydantic.fields import FieldInfo

from . import exp_time

class UserPayMessage(BaseModel):
    exp: datetime = FieldInfo(default_factory=exp_time, extra={})
```

> Note: See the sample code for specific calling and generation methods.

#### 2.3.4.4.`p2p@builtin`
When the variable to be used comes from a built-in function, this template can be used directly (it can be considered as a simplified version of the `p2p@local` template), and the syntax is as follows:
```protobuf
// comment example
message UserPayMessage {
  google.protobuf.Timestamp exp=1; // p2p: {"type": "p2p@builtin|float"}
}

// p2p example
message UserPayMessage {
  google.protobuf.Timestamp exp=1[(p2p_validate.rules).timestamp.type= "p2p@builtin|float"];
}
```
In this way, `protobuf_to_pydantic` can generate a `pydantic.BaseModel` object that meets the requirements:
```python
from pydantic import BaseModel
from pydantic.fields import FieldInfo


class UserPayMessage(BaseModel):
    exp: float = FieldInfo()
```
#### 2.3.4.5.Custom template
Currently, `protobuf_to_pydantic` only supports several templates. If you have more template requirements, you can extend the template by inheriting the `DescTemplate` class.
For example, there is a strange requirement that the default value of the field is the timestamp when the Message object is generated as a `pydantic.BaseModel` object, but the timestamp has two versions, one version has a timestamp of length 10 and the other has a length of 13, so write the following Protobuf file:
```protobuf
message TimestampTest{
  int32 timestamp_10 = 1[(p2p_validate.rules).int32.default = "p2p@timestamp|10"];
  int32 timestamp_13 = 2[(p2p_validate.rules).int32.default = "p2p@timestamp|13"];
}
```
This file uses the custom `p2p@timestamp|{x}` syntax, where `x` only has two values of 10 and 13, and then you can write code according to this template behavior, the code is as follows:
```python
import time
from typing import Any, List
from protobuf_to_pydantic.gen_model import DescTemplate


class CustomDescTemplate(DescTemplate):
    def template_timestamp(self, template_var_list: List[str]) -> Any:
        timestamp: float = time.time()
        length: str = template_var_list[0]
        if length == "10":
            return int(timestamp)
        elif length == "13":
            return int(timestamp * 100)
        else:
            raise KeyError(f"timestamp template not support value:{length}")


from .demo_pb2 import TimestampTest # fake code
from protobuf_to_pydantic import msg_to_pydantic_model

msg_to_pydantic_model(
    TimestampTest,
    desc_template=CustomDescTemplate
)
```
This code first creates a `CustomDescTemplate` class inherited from `DescTemplate`, and this class adds a `template_timestamp` method to match the syntax of `p2p@timestamp`,
Then specify the template class as `CustomDescTemplate` through the `desc_template` key parameter in `msg_to_pydantic_model`, so that `msg_to_pydantic_model` will generate the following code (assuming the code generated when the timestamp is 1600000000 ):
```python
from pydantic import BaseModel
from pydantic.fields import FieldInfo

class TimestampTest(BaseModel):
    timestamp_10: int = FieldInfo(default=1600000000)
    timestamp_13: int = FieldInfo(default=1600000000000)
```

## 3.Code formatting
Code generated directly via `protobuf_to_pydantic` is not perfect, but `protobuf+type_pydantic` can rely on different formatting tools to generate code that conforms to the `Python` specification.
Currently supported formatting tools are `autoflake`, `black` and `isort`, but the prerequisite for using these tools is that the corresponding formatting tools are installed in the current running environment.

In addition, developers can decide how the formatter will execute through the `pyproject.toml` configuration file, an example of `pyproject.toml` as follows:
```toml
# Controls which formatters protobuf-to-pydantic can use, false means that the formatter is not used (default is true)
[tool.protobuf-to-pydantic.format]
black = true
isort = true
autoflake = true

# See the black configuration documentation:https://black.readthedocs.io/en/stable/usage_and_configuration/the_basics.html#configuration-format
[tool.black]
line-length = 120
target-version = ['py37']

# See the isort configuration documentation:https://pycqa.github.io/isort/docs/configuration/config_files.html#pyprojecttoml-preferred-format
[tool.isort]
profile = "black"
multi_line_output = 3
include_trailing_comma = true
force_grid_wrap = 0
use_parentheses = true
ensure_newline_before_comments = true
line_length = 120

# See the autoflake configuration documentation:https://github.com/PyCQA/autoflake#configuration
[tool.autoflake]
in-place = true
remove-all-unused-imports = true
remove-unused-variables = true
```

## 4.example
`protobuf_to_pydantic` provides some simple sample code, the following is the path of the sample code and protobuf file, just for reference:

| Implication                           | Example Protobuf                                                                            | Example code                                                                         |
|------------------------------|---------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------|
| Generate Model code with validation rules based on p2p schema | https://github.com/so1n/protobuf_to_pydantic/tree/master/example/example_proto/p2p_validate | https://github.com/so1n/protobuf_to_pydantic/tree/master/example/p2p_validate_example |
| Generate the basic Model code               | https://github.com/so1n/protobuf_to_pydantic/tree/master/example/example_proto/demo         | https://github.com/so1n/protobuf_to_pydantic/tree/master/example/simple_example      |
| Generate Model code with validation rules from .pyi files     | https://github.com/so1n/protobuf_to_pydantic/tree/master/example/example_proto/demo         | https://github.com/so1n/protobuf_to_pydantic/tree/master/example/text_comment_example |
| Generate Model code with validation rules from protobuf files | https://github.com/so1n/protobuf_to_pydantic/tree/master/example/example_proto/validate     | https://github.com/so1n/protobuf_to_pydantic/tree/master/example/validate_example    |
