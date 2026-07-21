# Phicomm DC1 ESPHome reborn

## 固件编译及刷固件方法
### 0、前置条件
请确认已经按照[本方法](https://github.com/duchenpaul/phicomm_dc1-esphome/tree/main/cookbook)连接好TTL工具，并且TTL工具驱动已经正确安装。

### 1、下载固件配置文件（下方右键另存为）
> ####   固件版本定义：
> - [dc1_homeassistant_api](https://github.com/duchenpaul/phicomm_dc1-esphome/raw/main/yaml/dc1_homeassistant_api.yaml)：用于通过API接入Home Assistant
> - [dc1_homeassistant_mqtt](https://github.com/duchenpaul/phicomm_dc1-esphome/raw/main/yaml/dc1_homeassistant_mqtt.yaml)：用于通过MQTT接入Home Assistant
> - [dc1_mqtt](https://github.com/duchenpaul/phicomm_dc1-esphome/raw/main/yaml/dc1_mqtt.yaml)：用于接入其他mqtt平台


```
配置文件对应版本更新历史

dc1_homeassistant_api:

v2019.12.02.001：
迁移到1.14版本ESPHome

v2019.03.28.002：
编译固件前请更新esphome及esphome-core到最新版本！
1、优化按钮，解决重启问题


dc1_homeassistant_mqtt:

v2019.12.02.001：
迁移到1.14版本ESPHome

v2019.08.26.001：
感谢[yaming116](https://github.com/yaming116) QQ昵称：花开堪折枝的mqtt版本修改及测试，使用mqtt时禁止使用api！


```

### 2、修改固件配置文件

1. 参考`dc1_homeassistant_test.yaml`, 重命名设备

2. 在你的设备配置文件中使用如下 `external_components`（注意：如果通过 `packages` 引入了 `library/dc1.yaml`，需要先移除/替换其中的 `external_components`，否则列表会合并并保留 local source）:

    ```yaml
    external_components:
      - source:
          type: git
          url: https://github.com/duchenpaul/phicomm_dc1-esphome
          ref: master
        components: [cat9554]
        refresh: 1d
    ```

### 3、搭建编译环境及刷固件

- Windows

[点此查看](https://github.com/Samuel-0-0/esphome-tools-dc1/tree/master)

- MacOS
打开终端，执行如下命令：（如需python虚拟环境，请自行配置virtualenv）

```
# 安装 esphome
pip install esphome
# 进入配置文件所在目录
cd xxxxx
# 编译固件(xxxxx.yaml为你的配置文件名字)
esphome compile xxxxx.yaml
# 刷固件（线刷或者OTA皆可）
esphome upload xxxxx.yaml
```

- Linux
> 与MacOS类似，参考MacOS的方法
