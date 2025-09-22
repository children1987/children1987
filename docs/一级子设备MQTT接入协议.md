# 一级子设备MQTT接入协议

> **⚠️ 注意**
> 
> **不推荐**新接入设备采用。本协议仅为兼容老设备而保留，未来可能会被停用。
> 
> [子设备MQTT接入协议](子设备MQTT接入协议.md)完全兼容本协议，前者支持本平台的全新特性“支持多级子设备”，建议优先采用该协议。

对于仅有一级子设备的父设备与平台通信的场景，可使用以下MQTT主题：

## 主题概览

以下主题用于子设备通过网关与云端通讯：

| ***消息类型*** | ***主题*** | ***发布/订阅*** |
| --- | --- | --- |
| [子设备上报上线通知](#子设备上报上线通知) | gateway_connect/{username} | 网关发布 |
| [子设备上报下线通知](#子设备上报下线通知) | gateway_disconnect/{username} | 网关发布 |
| [子设备上报属性](#子设备上报属性) | gateway_attributes/{username} | 网关发布 |
| [子设备上报属性的响应](#子设备上报属性的响应) | gateway_attributes_response/{username} | 网关订阅 |
| [子设备获取云端属性](#子设备获取云端属性) | gateway_attributes_get/{username} | 网关发布 |
| [子设备获取云端属性的响应](#子设备获取云端属性的响应) | gateway_attributes_get_response/{username} | 网关订阅 |
| [云端下发属性至子设备](#云端下发属性至子设备) | gateway_attributes_push/{username} | 网关订阅 |
| [子设备上报事件](#子设备上报事件) | gateway_event_report/{username} | 网关发布 |
| [子设备上报事件的响应](#子设备上报事件的响应) | gateway_event_response/{username} | 网关订阅 |
| [云端下发命令至子设备](#云端下发命令至子设备) | gateway_command_send/{username} | 网关订阅 |
| [云端下发命令至子设备的响应](#云端下发命令至子设备的响应) | gateway_command_reply/{username} | 网关发布 |

## 各主题的使用方法

下面我们逐个介绍各个主题的使用方法。

### 子设备上报上线通知

当网关确定子设备已连接时，可上报消息通知平台，网关发布主题如下：

***gateway_connect/{username}***

网关 MQTT 的所有消息都必须是 JSON 格式，如果发布的不是 JSON 格式，网关会被平台主动断开 MQTT 连接。

```json
{
  "device": "SUB_DEVICE_ADDR",
  "product": "ProductKey OR ProductCode"
}
```

device：子设备地址。

product：非必含。`EZtCloud 公共产品库` 中，产品的 `产品Key` 或 `产品识别码` 。当包含此参数时，EZtCloud 将检查该设备是否已被创建，若否，则自动创建该设备。

### 子设备上报下线通知

当网关确定子设备已断开时，可上报消息通知平台，网关发布主题如下：

***gateway_disconnect/{username}***

发布消息格式如下：

```json
{
  "device": "SUB_DEVICE_ADDR"
}
```

device：子设备地址。

### 子设备上报属性

当网关接收子设备的属性变化时，向平台上报子设备属性主题如下：

***gateway_attributes/{username}***

消息格式：

```json
{
  "SUB_DEVICE_ADDR1": {
    "ATTRIBUTES1": "VALUE1",
    "ATTRIBUTES2": "VALUE2"
  },
  "SUB_DEVICE_ADDR2": {
    "ATTRIBUTES1": "VALUE1",
    "ATTRIBUTES2": "VALUE2"
  }
}
```

网关支持一次上报多个子设备的属性。

SUB_DEVICE_ADDR1、SUB_DEVICE_ADDR2：子设备地址。

举个例子，网关上报多个子设备的属性，如下：

```json
{
  "1": {
    "battery": 100,
    "occupancy": false
  },
  "2": {
    "battery": 98,
    "occupancy": true
  }
}
```

这时，在控制台的子设备详情页，会实时更新显示设备属性的最新值。

### 子设备上报属性的响应

网关订阅这个主题，可以实时接收平台下发给子设备的属性消息。

***gateway_attributes_response/{username}***

接收到的消息格式如下：

```json
{
  "error_code": 0,
  "error_msg": "OK",
  "ts": 12312314212
}
```

device：子设备地址。

网关通过自身的运行机制，将消息转发给子设备地址 为 SUB_DEVICE_ADDR1 的子设备，或者在转发前对数据包进行必要的处理。

> **⚠️ 注意**
>
>此响应消息默认`不开启`，需要时可在此处开启：设备类型详情页 > `设置` > `云端响应`。

### 子设备获取云端属性

网关可以获取子设备在平台的属性，例如用来初始化子设备的运行状态。

发布主题如下：

***gateway_attributes_get/{username}***

发布的消息格式

```json
{
  "device": "SUB_DEVICE_ADDR1",
  "get": {
    "keys": ["KEY1", "KEY2"]
  }
}
```

device：子设备地址。

keys：要读取的属性标识符数组，空数组 [] 标识读取所有属性。

### 子设备获取云端属性的响应

网关订阅以下主题，用来接收平台回复的子设备属性。

***gateway_attributes_get_response/{username}***

回复的消息格式

```json
{
  "device": "SUB_DEVICE_ADDR1",
  "error_code": 0,
  "error_msg": "",
  "ts": 12312314212,
  "attributes": {
    "KEY1": "VALUE1",
    "KEY1": "VALUE2"
  }
}
```

device：子设备地址。

response：读取子设备属性的回复内容。

### 云端下发属性至子设备

除了子设备主动获取属性以外，我们也需要让子设备可以实时接收云平台下发的属性。

确保网关已订阅如下主题：

***gateway_attributes_push/{username}***

当云平台下发属性给子设备时，网关会通过以上订阅主题，收到 JSON 结构的消息，例如：

```json
{
  "device": "SUB_DEVICE_ADDR1",
  "attributes": {
    "switch": false
  }
}
```

这个示例消息显然是通知字设备关闭某个开关，子设备通过自身的程序实现该功能后，可以接着向云平台上报属性或上报事件，让云平台得到确认。

### 子设备上报事件

在前边的介绍中，我们已经知道，事件通常用于设备向平台发送一些通知或请求，但不希望将相关参数记录到设备属性中。

网关同样可以上报子设备的事件，并触发平台对子设备设置的事件规则。

例如，网关上报子设备请求 OTA 固件版本检查的事件。

发布主题如下：

***gateway_event_report/{username}***

上报的消息格式

```json
{
  "device": "SUB_DEVICE_ADDR1",
  "event": {
    "method": "EVENT_IDENTIFIER",
    "params": {
      "PARAM1": "VALUE1",
      "PARAM2": "VALUE2"
    },
    "id": 1000
  }
}
```

device：子设备地址。

event：事件消息体，与直连设备事件上报的格式相同。

### 子设备上报事件的响应

如果我们想知道事件上报是否被云平台成功接收，可以订阅如下主题：

***gateway_event_response/{username}***

当网关上报子设备事件后，便会通过该主题收到来自云端的响应消息，如果云端接收成功，响应消息如下：

```json
{
  "error_code": 0,
  "error_msg": "OK",
  "ts": 12312314212,
  "device": "SUB_DEVICE_ADDR1"
}
```
> **💡 提示**
>
> 响应消息中的成功，只代表云平台成功收到了事件上报，并不代表对事件进行业务处理的结果。

云平台收到子设备的事件上报后，如何处理事件呢？***规则引擎***便派上用场了，通过规则引擎，您可以将事件实时推送到第三方，或通过规则引擎的云函数实现告警策略，当然还可以实现对其它设备的联动控制。

> **⚠️ 注意**
>
> 此响应消息默认`不开启`，需要时可在此处开启：设备类型详情页 > `设置` > `云端响应`。

### 云端下发命令至子设备

订阅主题如下：

***gateway_command_send/{username}***

接收到的消息格式如下：

```json
{
  "device": "SUB_DEVICE_ADDR1",
  "command": {
    "method": "COMMAND_IDENTIFIER",
    "params": {
      "PARAM1": "VALUE1",
      "PARAM2": "VALUE2"
    },
    "id": 1000
  }
}
```

device：子设备地址。

command：命令消息体，与直连设备下发命令消息的格式相同。

### 云端下发命令至子设备的响应

子设备收到命令消息后，在设备端实现特定的功能前，可以回复命令，也可以不回复命令。

云端会自动接收回复命令，并和下发命令进行匹配，在控制台的设备命令历史中，您可以看到一组包含下发和回复的命令日志。一次下发命令只能接收一次回复命令，它们的匹配是通过使用一致的 `<id>` 来保证。

发布主题如下：

***gateway_command_reply/{username}***

消息格式如下：

```json
{
  "device": "SUB_DEVICE_ADDR1",

  "command": {
    "method": "EVENT_IDENTIFIER",
    "params": {
      "PARAM1": "VALUE1",
      "PARAM2": "VALUE2"
    },
    "id": 1000
  }
}
```

它和命令下发的消息内容完全一样。