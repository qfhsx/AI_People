<span id="#Md1eFOlC"></span>
## 接口简介
使用克隆数字人形象id，生成数字人视频，返回视频url
<span id="#dVqXfrFI"></span>
## 限制条件

|名称 |内容 |
|---|---|
|音频要求 |1. 音频格式：支持mp3、wav格式，推荐为wav格式 |

<span id="#nunaQrKy"></span>
## 请求说明

|名称 |内容 |
|---|---|
|接口地址 |[https://visual.volcengineapi.com](https://visual.volcengineapi.com/) |
|请求方式 |POST |
|Content\-Type |application/json |

<span id="#dPxfxAqk"></span>
## 提交任务
<span id="#iats95yk"></span>
### **提交任务请求参数**
<span id="#x0H8Mc5h"></span>
#### **Header参数**
完整公共参数列表见 [公共参数](https://www.volcengine.com/docs/6369/67268)
本服务**Region为cn\-north\-1，Service为cv**
<span id="#0SpKzYp2"></span>
#### **Query参数**
:::tip 拼接到url后的参数，示例：[https://visual.volcengineapi.com?Action=CVSubmitTask&Version=2022-08-31](https://visual.volcengineapi.com?Action=CVSubmitTask&Version=2022-08-31)

:::
|参数 |可选/必选 |类型 |说明 |
|---|---|---|---|
|Action |必选 |String |接口名，取值：CVSubmitTask |
|Version |必选 |String |版本号，取值：2022\-08\-31 |

<span id="#krM1cWF9"></span>
#### **Body参数**
:::warning
业务请求参数，放到request.body中，MIME\-Type为**application/json**

:::
|名称 |类型 |必选 |描述 |备注 |
|---|---|---|---|---|
|req_key |string |是 |服务标识| |\
| | | |取固定值: realman_avatar_creation_task | |
|resource_id |string |是 |克隆数字人id| |\
| | | |如尚未购买和创建克隆数字人形象，可使用官方提供的 **250623\-zhibo\-linyunzhi** 进行试用 | |
|audio_url |string |是 |音频url | |
|templ_start_strategy |string |否 |指定模板开始策略| |\
| | | || |\
| | | |* start_from_given_seconds：指定模板开始时间| |\
| | | || |\
| | | |&nbsp;| |\
| | | |在某些场景下，需要省略模板视频开头段落，能生成效果更好的数字人视频| |\
| | | |&nbsp;| |\
| | | |**例如： ** 我在 [创建克隆数字人形象](https://www.volcengine.com/docs/85128/1773809) 时，上传了一个20秒模板视频，我现在想省略头5秒，用后面的15秒作为模板来生成本次的数字人视频，就可以在body中添加下面参数来达成这个效果| |\
| | | |```JSON| |\
| | | |"templ_start_strategy":"start_from_given_seconds",| |\
| | | |"templ_start_seconds":5| |\
| | | |```| |\
| | | | | |
|templ_start_seconds |double |否 |指定渲染模版开始时间点，默认为0| |\
| | | |自动对模板时长取余（假设模版视频一共30s，如果设置了40s，那么就相当于设置成10s，对30s取余）| |\
| | | |可传入小数 | |

<span id="#A25ib5qe"></span>
### 提交任务返回参数
<span id="#fIqDKFOO"></span>
#### **通用返回参数**
请参考[通用返回字段及错误码](https://www.volcengine.com/docs/6444/69728)
<span id="#20otoM38"></span>
#### **业务返回参数**
:::tip 重点关注data中以下字段，其他字段为公共返回(可忽略或不做解析)

:::
|字段 |类型 |说明 |
|---|---|---|
|task_id |string |任务ID，用于查询结果 |

<span id="#uAai0lIu"></span>
### 提交任务请求&返回完整示例
**请求示例：** 
```JSON
{
    "req_key":"realman_avatar_creation_task",
    "resource_id":"b782c6c2-6ad9-4c8e-8e2a-659eaae7e6e0",
    "audio_url": "http://XXXX.wav"
}
```

**返回示例：** 
```JSON
{
    "code": 10000,
    "data": {
        "task_id": "14411597596416601128"
    },
    "message": "Success",
    "request_id": "20250804222334727A1B3CE05362A5E78A",
    "status": 10000,
    "time_elapsed": "49.115688ms"
}
```

<span id="#Ue1eQBE0"></span>
## 查询任务
<span id="#A77xsLeN"></span>
### **查询任务请求参数**
<span id="#m2QXTchw"></span>
#### **Header参数**
完整公共参数列表见 [公共参数](https://www.volcengine.com/docs/6369/67268)
本服务**Region为cn\-north\-1，Service为cv**
<span id="#W4wWSOUr"></span>
#### **Query参数**
:::tip 拼接到url后的参数，示例：[https://visual.volcengineapi.com](https://visual.volcengineapi.com/)[?Action=CVGetResult&Version=2022-08-31](https://visual.volcengineapi.com?Action=CVGetResult&Version=2022-08-31)

:::
|参数 |可选/必选 |类型 |说明 |
|---|---|---|---|
|Action |必选 |String |接口名，固定值：CVGetResult |
|Version |必选 |String |版本号，固定值：**2022\-08\-31** |

<span id="#J8rqHQJM"></span>
#### **Body参数**
:::warning
业务请求参数，放到request.body中，MIME\-Type为**application/json**

:::
|参数 |可选/必选 |类型 |说明 |示例 |
|---|---|---|---|---|
|req_key |必选 |String |服务标识，取固定值: realman_avatar_creation_task | |
|task_id |必选 |String |任务ID，此字段的取值为**提交任务接口**的返回 | |

<span id="#b0kqLtUe"></span>
### 查询任务返回参数
<span id="#kRJXEMxW"></span>
#### **通用返回参数**
请参考[通用返回字段及错误码](https://www.volcengine.com/docs/6444/69728)
<span id="#NkKs5Myo"></span>
#### **业务返回参数**
:::tip
重点关注data中以下字段，其他字段为公共返回(可忽略或不做解析)

:::
|参数名 |参数说明 |参数示例 |
|---|---|---|
|url |结果视频url | |

<span id="#lBB7zDPI"></span>
### 查询任务请求&返回完整示例
**请求示例：** 
```JSON
{
    "req_key": "realman_avatar_creation_task",
    "task_id": "<任务提交接口返回task_id>"
}
```

**返回示例：** 
```JSON
{
    "code": 10000,
    "data": {
        "binary_data_base64": [],
        "image_urls": null,
        "resp_data": "{\"progress\":100,\"received_at\":1754317414,\"finished_at\":1754317434,\"inferred_at\":1754317414,\"creation_duration\":20,\"inferred_rtf\":5.154639175257732,\"process_rtf\":5.154639175257732,\"submit_log_id\":\"20250804222334727A1B3CE05362A5E78A\",\"vid\":{\"Vid\":\"v020adg10005d28c4tfog65rs0t5blag\",\"VideoMeta\":{\"Uri\":\"tos-cn-v-242bcc/oME47KfDhSEAVwaCF6QpEViiCUA1A0QnBEAGAi\",\"Height\":1282,\"Width\":720,\"OriginHeight\":1282,\"OriginWidth\":720,\"Duration\":3.88,\"Bitrate\":3822272,\"Md5\":\"65dad5936f4ce903c5fe0e76f8531a9e\",\"Format\":\"MP4\",\"Size\":1853802,\"FileType\":\"video\"},\"url\":\"https://v26-vvecloud.yangyi08.com/1e822419cc129cc17c4d0303f1bd01e3/689181d1/video/tos/cn/tos-cn-v-242bcc/oME47KfDhSEAVwaCF6QpEViiCUA1A0QnBEAGAi/?a=7073&ch=0&cr=0&dr=0&er=0&lr=default&cd=0%7C0%7C0%7C0&br=3732&bt=3732&cs=0&ds=3&ft=xztlUQhhe6BMyq5mVOkJD12Nzj&mime_type=video_mp4&qs=13&rc=am84M3U5cndmNTgzNGczM0Bpam84M3U5cndmNTgzNGczM0BeX3FwMmRjMTVhLS1kXi9zYSNeX3FwMmRjMTVhLS1kXi9zcw%3D%3D&btag=80000e00008000&dy_q=1754362814&l=20250805110014E1FCC673C0BFEA535F18\"},\"code\":0,\"msg\":\"success\"}",
        "status": "done"
    },
    "message": "Success",
    "request_id": "20250805110014E1FCC673C0BFEA535F18",
    "status": 10000,
    "time_elapsed": "172.502303ms"
}
```

<span id="#QjhcvrCE"></span>
## 错误码
<span id="#osKGbBPW"></span>
### **通用错误码**
请参考[通用返回字段及错误码](https://www.volcengine.com/docs/6444/69728)
<span id="#ZJyTWZaP"></span>
### **业务错误码**

|HttpCode |错误码 |错误消息 |描述 |是否需要重试 |
|---|---|---|---|---|
|200 |10000 |无 |请求成功 |不需要 |
|400 |50411 |Pre Img Risk Not Pass |输入图片前审核未通过 |不需要 |
|400 |50511 |Post Img Risk Not Pass |输出图片后审核未通过 |可重试 |
|400 |50412 |Text Risk Not Pass |输入文本前审核未通过 |不需要 |
|400 |50512 |Post Text Risk Not Pass |输出文本后审核未通过 |不需要 |
|400 |50413 |Post Text Risk Not Pass |输入文本含敏感词、版权词等审核不通过 |不需要 |
|429 |50429 |Request Has Reached API Limit, Please Try Later |QPS超限 |可重试 |
|429 |50430 |Request Has Reached API Concurrent Limit, Please Try Later |并发超限 |可重试 |
|500 |50500 |Internal Error |内部错误 |可重试 |
|500 |50501 |Internal RPC Error |内部算法错误 |可重试 |

<span id="#ZJQe9RpM"></span>
## 接入说明
<span id="#c9HnMnHk"></span>
### HTTP方式接入说明
请参考[HTTP请求示例](https://www.volcengine.com/docs/6444/1390583)


