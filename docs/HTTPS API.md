# HTTPS API

## 准备工作

### 获得项目 API 接入参数

可在 **控制台 > 项目设置 > 应用层API** 中获取 **HTTPS API 接入点**。

全局的，请使用 `https` 加密访问，为确保数据安全性，全局不支持 `http` 协议访问。

不同项目的 API 接入点可能不同，请您以控制台获取的地址为准。

此外，您还需要妥善保存此页面的 **ProjectKey** 和 **ProjectToken**（或**ProjectSecret**），用于请求 API 时的身份验证。

## 认证

应用层应用可通过如下两种方式之一认证：

- 通过**ProjectToken**认证
- 通过**ProjectSecret**认证（不推荐，即将废弃）

|  | ***通过ProjectToken认证*** | ***通过ProjectSecret认证*** |
| --- | --- | --- |
| 是否推荐 | 推荐 | 不推荐，即将废弃 |
| 安全性 | 高 | 低 |
| 易用性 | 一般 | 高 |
| 特点 | 请求时不直接发送ProjectToken，故**安全性较高** | 简单易用，但**安全性较低** |

### 通过ProjectToken认证

基于`timestamp`(时间戳)和`ProjectToken`，通过下文给出的算法计算出`signature`后，访问其它API时，在请求头中携带前述`timestamp`、`signature`和`ProjectKey`即可。

```
user {ProjectKey}
timestamp {timestamp}
signature {signature}
// 其它 header key
```

`signature` 的有效期为**2小时**，过期后需重新计算。

**ProjectToken**应仅保存在应用层服务器，严防泄密。

如下是一段由python语言实现的`signature`计算代码。其包含详细注释，亦可将其视为签名计算算法的伪代码：

```python
import hashlib
import time
# 自 Unix 纪元（January 1 1970 00:00:00 GMT）起的当前时间的秒数。
time_time = time.time()
# 转为字符串，直接忽略小数部分取整。（获取字符串长度为10，例如"1626969655"。）
timestamp = str(time_time)[:10]
# 字符串后拼接token，获取ori_str。假设此处token为"123456"，则ori_str为"1626969655123456"。
ori_str = timestamp + token
# ori_str以utf-8编码，获取encoded_str，接上文例，encoded_str为"1626969655123456"。
encoded_str = ori_str.encode(encoding='utf-8')
# 获取encoded_str的md5码，即为所需签名，接上文例，signature 为"8771d774599c38b15adba116ed82ca8d"。
signature = hashlib.md5(encoded_str).hexdigest()
```

> **⚠️ 注意**
>
> 实现上述算法后，请务必以上文中的例子验证签名算法的正确性。

### 通过ProjectSecret认证（不推荐，即将废弃）

通过API获取 `AccessToken`，用于其它所有 API 请求的身份标识。

`AccessToken` 获取后的有效期为**24小时**，过期后需重新获取。

在调用其它接口时，将获取到的 `token` 字符串作为 Bearer Token加入请求头即可。如：

```bash
Authorization Bearer string_xxx
// 其它 header key
```

服务器发起请求，获取 `AccessToken`。ProjectSecret应仅保存在应用层服务器，严防泄密。

**Request Syntax**

```bash
POST <HTTPS API 接入点>/api_login/ HTTP/1.1
Content-Type: application/json
```

**Request Body**

```json
{
	"username": "project_key",
	"password": "project_secret"
}
```

**Body Parameters**

- `project_key`：在控制台项目应用中获取。例如：PR_SrtQtf9dEx
- `project_secret`：在控制台项目应用中获取。

**Response Syntax**

```bash
HTTP/1.1 200 OK
Content-type: application/json

{
    "result": 0,
    "token": "string_xxx"
}
```

**HTTP Status Code**

- 200：请求成功。
- 其它：请求失败。

## API 请求代码示例

以获取 API AccessToken 为例，以下是python语言请求 API 的示例代码，仅供参考：

```python
import requests
import json

url = '<HTTPS API 接入点>/api/devices/<device_username>/down_attr/'
data = {
    "attrs": "{\"attr1\": \"off\", \"attr2\": 26}"
}
headers = {
    'Content-Type': 'application/json'
}
response = requests.post(url, data=json.dumps(data), headers=headers)

print(response.text)
```

> **💡 提示**
>
> 本系统API不限制调用者使用的编程语言，其它编程语言一般也都支持http(s)的调用，这里不再逐一给出样例。

## 项目资源API

项目下几乎所有资源都可通过API访问。

想快速尝试？我们提供了[在线测试工具](https://api.eztcloud.com/swagger-ui/)。

如下为详细描述：

### 项目

详见[接口文档](https://api.eztcloud.com/swagger-ui/)。

### 设备类型

详见[接口文档](https://api.eztcloud.com/swagger-ui/)。

### 设备组

详见[接口文档](https://api.eztcloud.com/swagger-ui/)。

### 设备

#### 设备属性下发

**Request Syntax**

```bash
POST <HTTPS API 接入点>/api/devices/<device_username>/down_attr/ HTTP/1.1
Content-Type: application/json
```

**Path Parameters**

- `device_username`：设备的username. 例如：DU_dMcDPsiBlk

**Request Body**

```json
{
    "attrs": "{\"attr1\": \"off\", \"attr2\": 26}"
}
```

**Body Parameters**

- `attrs`：一个json字符串。将其load为对象后，其键为设备的属性名称，其值为相应属性的值。支持一次下发多个属性。

**Response Syntax**

```bash
HTTP/1.1 200 OK
Content-type: application/json
```

**HTTP Status Code**

- 200：请求成功。
- 其它：请求失败。

#### 其它接口

详见[接口文档](https://api.eztcloud.com/swagger-ui/)。
