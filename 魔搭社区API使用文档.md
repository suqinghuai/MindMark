## 概要#

魔搭通过API-Inference，将开源模型服务化并通过API接口进行标准化，让开发者能以更轻量和迅捷的方式体验开源模型，并集成到不同的AI应用中，从而展开富有创造力的尝试，包括与工具结合调用，来构建多种多样的AI应用原型。

## 前提条件：创建账号并获取Token#

API-Inference面向ModelScope注册用户免费提供，请在登陆后获取您专属的访问令牌（Access Token）。具体可以参见[账号注册和登陆](https://modelscope.cn/docs/accounts/registration)以及[Token的管理](https://modelscope.cn/docs/accounts/token)等相关文档。 ![img.png](https://resouces.modelscope.cn/document/docdata/2026-3-10_16-8-CN/dist/model-service/API-Inference/intro/_resources/token.png) 注意: 账号注册后需[绑定阿里云账号](https://modelscope.cn/docs/accounts/aliyun-binding-and-authorization)，并且通过[**实名认证**](https://help.aliyun.com/zh/account/real-name-authentication)后才可使用API-Inference。

## 使用方法#

### 大语言模型 LLM#

当前魔搭平台的API-Inference，针对大语言模型提供OpenAI API兼容的接口。 对于LLM模型的API，使用前，请先安装OpenAI SDK:

```
pip install openai
```

NOTE

其他流行的接口也陆续支持中，例如[Anthropic API](https://docs.anthropic.com/en/api)，可参见下面的 “大语言模型 LLM（Anthropic API兼容接口）” 部分。

安装后就可以通过标准的OpenAI调用方式使用。具体调用方式，在每个模型页面右侧的API-Inference范例中以提供，**请以模型页面的 API-Inference 示范代码为准**，尤其例如对于reasoning模型，调用的方式与标准LLM会有一些细微区别。以下范例仅供参考。

NOTE

请注意，本文档中的模型名字，都仅作示范作用。在不同时间，随着新模型上线，旧模型可能下线不再支持。为确保API调用能正常工作，请配置一个当前支持的模型 ID。

```
from openai import OpenAI

client = OpenAI(
    api_key="MODELSCOPE_ACCESS_TOKEN", # 请替换成您的ModelScope Access Token
    base_url="https://api-inference.modelscope.cn/v1/"
)


response = client.chat.completions.create(
    model="Qwen/Qwen3.5-35B-A3B", # ModelScope Model-Id
    messages=[
        {
            'role': 'system',
            'content': 'You are a helpful assistant.'
        },
        {
            'role': 'user',
            'content': '用python写一下快排'
        }
    ],
    stream=True
)

for chunk in response:
    print(chunk.choices[0].delta.content, end='', flush=True)
```

在这个范例里，使用魔搭的API-Inference，有几个需要适配的有几个地方：

-   base url: 指向魔搭API-Inference服务 `https://api-inference.modelscope.cn/v1/`。
-   api\_key: 使用魔搭的访问令牌(Access Token), 可以从您的魔搭账号中获取：[https://modelscope.cn/my/myaccesstoken](https://modelscope.cn/my/myaccesstoken) 。
-   模型名字(model):使用魔搭上开源模型的Model Id，例如`Qwen/Qwen2.5-Coder-32B-Instruct` 。

### 大语言模型 LLM（Anthropic API兼容接口）#

针对LLM模型，API-Inference也支持与Anthropic API兼容的调用方式。要使用Anthropic模式，请在使用前，安装Anthropic SDK:

```
pip install anthropic
```

IMPORTANT

Anthropic API兼容调用方式当前整处于beta测试阶段。如果您在使用过程中遇到任何问题，请联系我们[提供反馈](https://modelscope.cn/docs/community/contact-us)。

安装Anthropic SDK后，即可调用，以下为使用范例。

#### 流式调用#

```
import anthropic

client = anthropic.Anthropic(
    api_key="MODELSCOPE_ACCESS_TOKEN", # 请替换成您的ModelScope Access Token
    base_url="https://api-inference.modelscope.cn")

with client.messages.stream(
    model="Qwen/Qwen3.5-35B-A3B", # ModelScope Model-Id
    messages=[
        {"role": "user", "content": "write a python quicksort"}
    ],
    max_tokens = 1024
) as stream:
  for text in stream.text_stream:
      print(text, end="", flush=True)
```

#### 非流式调用#

```
import anthropic

client = anthropic.Anthropic(
    api_key="MODELSCOPE_ACCESS_TOKEN", # 请替换成您的ModelScope Access Token
    base_url="https://api-inference.modelscope.cn")

message = client.messages.create(
    model="Qwen/Qwen3.5-35B-A3B", # ModelScope Model-Id
    messages=[
        {"role": "user", "content": "write a python quicksort"}
    ],
    max_tokens = 1024
)
print(message.content[0].text)
```

在这个范例里，使用魔搭的API-Inference，有几个需要适配的有几个地方：

-   base url: 指向魔搭API-Inference服务 `https://api-inference.modelscope.cn` 。
-   api\_key: 使用魔搭的访问令牌(Access Token), 可以从您的魔搭账号中获取：[https://modelscope.cn/my/myaccesstoken](https://modelscope.cn/my/myaccesstoken) 。
-   模型名字(model):使用魔搭上开源模型的Model Id，例如`Qwen/Qwen2.5-Coder-32B-Instruct` 。

更多Anthropic API的接口用法以及参数，可以参考 [Anthropic API官方文档](https://docs.anthropic.com/en/api)。

### Base64 本地图片编码工具函数#

对于具备视觉理解能力的模型（如Qwen2.5-VL等专门的VL模型，以及Qwen3.5等支持视觉的一体化模型）和图像编辑模型，如果需要使用本地图片而非线上URL，可以通过以下工具函数将本地图片转为Base64编码：

```
import os
import mimetypes
import base64

def image_to_data_url(image_path):
    if not os.path.isfile(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")

    with open(image_path, "rb") as f:
        image_data = f.read()

    mime_type, _ = mimetypes.guess_type(image_path)

    if mime_type is None or not mime_type.startswith('image/'):
        mime_type = 'image/png'

    base64_encoded = base64.b64encode(image_data).decode('utf-8')
    return f"data:{mime_type};base64,{base64_encoded}"
```

下方的**视觉模型**和**AIGC模型**部分均会使用该函数。

### 视觉模型#

对于视觉理解场景，同样可以通过OpenAI API调用，例如：

```
from openai import OpenAI

client = OpenAI(
    base_url='https://api-inference.modelscope.cn/v1',
    api_key='MODELSCOPE_ACCESS_TOKEN', # 请替换成您的ModelScope Access Token
)

response = client.chat.completions.create(
    model='Qwen/Qwen3.5-35B-A3B', # ModelScope Model-Id, required
    messages=[{
        'role':
            'user',
        'content': [{
            'type': 'text',
            'text': '描述这幅图',
        }, {
            'type': 'image_url',
            'image_url': {
                'url':
                    'https://modelscope.oss-cn-beijing.aliyuncs.com/demo/images/audrey_hepburn.jpg',
            },
        }],
    }],
    stream=True
)

for chunk in response:
    if chunk.choices:
        print(chunk.choices[0].delta.content, end='', flush=True)
```

具备视觉理解能力的模型（如Qwen2.5-VL等专门的VL模型，以及Qwen3.5等支持视觉的一体化模型）均支持通过Base64编码传入本地图片，只需使用上方的[`image_to_data_url`](https://modelscope.cn/docs/model-service/API-Inference/intro#base64-%E6%9C%AC%E5%9C%B0%E5%9B%BE%E7%89%87%E7%BC%96%E7%A0%81%E5%B7%A5%E5%85%B7%E5%87%BD%E6%95%B0)函数，将`image_url`中的URL替换为该函数的返回值即可：

```
        'content': [{
            'type': 'text',
            'text': '描述这幅图',
        }, {
            'type': 'image_url',
            'image_url': {
                'url': image_to_data_url('path/to/local/image.jpg'),
            },
        }],
```

### AIGC模型#

支持API调用的模型列表，可以通过[AIGC模型](https://www.modelscope.cn/aigc/models)页面进行搜索。 API的调用示例如下:

```
import requests
import time
import json
from PIL import Image
from io import BytesIO

base_url = 'https://api-inference.modelscope.cn/'
api_key = "<MODELSCOPE_SDK_TOKEN>"

common_headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
}

response = requests.post(
    f"{base_url}v1/images/generations",
    headers={**common_headers, "X-ModelScope-Async-Mode": "true"},
    data=json.dumps({
        "model": "Qwen/Qwen-Image",
        # "loras": "<lora-repo-id>", # optional lora(s)
        """
        LoRA(s) Configuration:
        - for Single LoRA: 
        "loras": "<lora-repo-id>"
        - for Multiple LoRAs: 
        "loras": {"<lora-repo-id1>": 0.6, "<lora-repo-id2>": 0.4}
        - Upto 6 LoRAs, all weight-coeffients must sum to 1.0
        """
        "prompt": "A golden cat"
    }, ensure_ascii=False).encode('utf-8')
)


response.raise_for_status()
task_id = response.json()["task_id"]

while True:
    result = requests.get(
        f"{base_url}v1/tasks/{task_id}",
        headers={**common_headers, "X-ModelScope-Task-Type": "image_generation"},
    )
    result.raise_for_status()
    data = result.json()

    if data["task_status"] == "SUCCEED":
        image = Image.open(BytesIO(requests.get(data["output_images"][0]).content))
        image.save("result_image.jpg")
        break
    elif data["task_status"] == "FAILED":
        print("Image Generation Failed.")
        break

    time.sleep(5)
```

#### Base64 图片输入支持#

对于图像编辑模型，输入的图片建议使用线上托管的图像URL地址。如果需要使用本地文件，可以使用上方的[`image_to_data_url`](https://modelscope.cn/docs/model-service/API-Inference/intro#base64-%E6%9C%AC%E5%9C%B0%E5%9B%BE%E7%89%87%E7%BC%96%E7%A0%81%E5%B7%A5%E5%85%B7%E5%87%BD%E6%95%B0)函数对本地图片进行Base64编码，并将编码后的数据作为`image_url`传递给模型。一个典型的调用方式是：

```
        # input as base64
        "image_url": [
           image_to_data_url("path/to/local/image.jpg")
        ]
```

更多参数说明

|参数名|参数说明|是否必须|参数类型|示例|取值范围|
|---|---|---|---|---|---|
|model|模型id|是|string|MAILAND/majicflus\_v1|ModelScope上的AIGC 模型ID|
|prompt|正向提示词，大部分模型建议使用英文提示词效果较好。|是|string|A mysterious girl walking down the corridor.|长度小于2000|
|negative\_prompt|负向提示词|否|string|lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry|长度小于2000|
|size|生成图像分辨率大小|否|string|1024x1024|分辨率范围:
SD系列:\[64x64,2048x2048\]，FLUX:\[64x64,1024x1024\]，Qwen-Image:\[64x64,1664x1664\], Z-Image-Turbo: \[512x512, 2048x2048\]|
|seed|随机种子|否|int|12345|\[0,2^31-1\]|
|steps|采样步数|否|int|30|\[1,100\]|
|guidance|提示词引导系数|否|float|3.5|\[1.5,20\]|
|image\_url|待编辑图片的url地址（或者编码过的base64数据），该参数只适用于支持图片编辑的模型|否|string|https://resources.modelscope.cn/aigc/image\_edit.png|确保公网可访问（或者编码过的base64数据）|
|loras|LoRA模型，用于风格迁移或细节增强。请在ModelScope [AIGC专区模型库](https://modelscope.cn/aigc/models)查找与基础模型兼容的LoRA模型|否|string|dict|单个LoRA: "<lora-repo-id>"
多个LoRA: {"<lora-repo-id1>": 0.6, "<lora-repo-id2>": 0.4}|