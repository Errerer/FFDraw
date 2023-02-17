# FFDraw: 一个针对FFxiv的悬浮窗图形显示框架

> 此处应有介绍

## 运行

### python 版本

* 需求 `python3.10` 或以上的`x64版本`作为运行环境
* 下载专案后在专案目录运行 `python -m pip install -r requirements.txt` 安装依赖
* 如果遇到安装依赖问题请自行搜索 `pip换源` 相关
* 执行 `main.py`

### exe 版本

* 去 [release](https://github.com/nyaoouo/FFDraw/releases/latest) 下载带exe的发布
* 双击 `FFDraw.exe` 运行
* 注：exe版本未必属于最新版本，也未必适应你的运行环境，请尽量使用python版本或从其他人获取最新版本的build (安装 `pyinstaller` 并运行 `pack.py`)
* 注2：cn版本与正常版本差异为默认值适配国内网络、国服默认路径编码，无需手动设置，两个版本均能适用与国服与国际服

### 注

* 如果遇到编码问题 `utf8 cant decode` 之类，请修改 `config.json` 中的 `path_encoding` 为 `gbk` 并重启程序
* 关于跨域：设置 `web_server/enable_cors`，另外如果你不打算给链接设置ssl， chrome 请在 [chrome://flags/](chrome://flags/) 中设置 `Block insecure private network requests`
  为 `disable` [(ref)](https://developer.chrome.com/articles/cors-rfc1918-feedback/#chrome%27s-plans-to-enable-cors-rfc1918)

## 使用

本程序基础的使用基于 http rpc api, 运行后将json指令传送到 `http://127.0.0.1:8001/rpc` 即可  
一个基础的 json payload 例子：

```json
{
    "cmd": "add_omen",
    "color": "enemy",
    "shape_scale": {
        "key": "circle",
        "range": 5
    },
    "pos": {
        "key": "actor_pos",
        "id": 269567252
    },
    "duration": 10
}
```

在本接口中，关键字和其他参数在同一层，请注意  
更多例子参阅 [这里](./test.py)

## 指令：关键字`cmd`

#### 指令：add_omen

* 描述：添加一个图形并且返回 omen_id

|      参数       |                类型                |                                   描述                                    |
|:-------------:|:--------------------------------:|:-----------------------------------------------------------------------:|
|    `shape`    |             `number`             |                        图形的形状，高十六位为类型，低十六位为参数（后详）                        |
|    `scale`    |           `number[3]`            |                       图形的比例，对应`[东西刻度，上下刻度，南北刻度]`                        |
| `shape_scale` |      `(number, number[3])`       |          一般用于使用特殊值（后详），为形状、比例的二元组，当存在时忽略 `shape` 和 `scale` 参数           |
|   `surface`   |     `number[3]`/`number[4]`      |                      填充颜色的rgba值，如果输入长度为3，默认alpha为1                      |
|    `line`     |     `number[3]`/`number[4]`      |                      线条颜色的rgba值，如果输入长度为3，默认alpha为1                      |
|    `color`    | `string`/`number[3]`/`number[4]` | 输入为 `string` 时会套用预设配色（后详），否则等同于`surface`参数，当存在时忽略 `surface` 和 `line` 参数 |
|     `pos`     |           `number[3]`            |                  图像在游戏3d空间里面的位置，对应 `[东西刻度，上下刻度，南北刻度]`                   |
|   `facing`    |             `number`             |                           图像沿着y轴的旋转量，以rad为单位                            |
|  `duration`   |             `number`             |                          图像的存活时间，空则一直存在需要手动清除                           |
|    `label`    |             `string`             |                               在指定位置显示的文字                                |
| `label_color` |           `number[3]`            |                                 显示文字的颜色                                 |
| `label_scale` |             `number`             |                                 显示文字的比例                                 |
|  `label_at`   |             `number`             |             显示文字的相对坐标的位置（[参见这里](./ff_draw/gui/text.py#L41)）             |

---
#### 指令：add_line

* 描述：添加一个线条 omen_id

|      参数       |                类型                |             描述             |
|:-------------:|:--------------------------------:|:--------------------------:|
|     `src`     |           `number[3]`            |           线条的来源            |
|     `dst`     |           `number[3]`            |           线条的目标            |
|    `width`    |             `number`             |          线条粗幼，默认3          |
|    `color`    | `string`/`number[3]`/`number[4]` | 线条颜色，输入为 `string` 时会套用预设配色 |
|    `label`    |             `string`             |         在指定位置显示的文字         |
| `label_color` |           `number[3]`            |          显示文字的颜色           |
| `label_scale` |             `number`             |          显示文字的比例           |
|  `label_at`   |             `number`             |        显示文字的相对坐标的位置        |

---

#### 指令：destroy_omen

* 描述：删除指定图形

|  参数  |    类型    |          描述           |
|:----:|:--------:|:---------------------:|
| `id` | `number` | 图形的omen_id,如果为-1则全部删除 |

---

#### 指令：foreach

* 描述：foreach(`values` as `name`)`func`()

|    参数    |    类型    |   描述    |
|:--------:|:--------:|:-------:|
| `values` | `any[]`  |  变量的列表  |
|  `name`  | `string` | 变量赋值的名字 |
|  `func`  |   `指令`   |  执行的指令  |

---

#### 指令：with_args

* 描述：设定变量列表并且运行 `func`

|   参数   |       类型       |   描述    |
|:------:|:--------------:|:-------:|
| `args` | `map[str,any]` |  变量的列表  |
| `func` |      `指令`      |  执行的指令  |

## 预设配色

|   关键字    |  描述  |
|:--------:|:----:|
|  enemy   | 珊瑚色  |
| g_enemy  |  橘色  |
|  friend  | 海水蓝 |
| g_friend | 天蓝色  |

## 图形：数值类型

* 高十六位为类型，低十六位为参数

| 图形类型 |      参数       |                                                描述                                                |
|:----:|:-------------:|:------------------------------------------------------------------------------------------------:|
| 0x1  | 内圈比例 * 0xffff | 参数为空是普通圆形，否则月环，如果需要描述外圈 20 内圈 10 的月环，图形值为 `0x10000&#124;int((10/20)*0xffff)`（scale为 `[20,1,20]`） |
| 0x2  |      特殊值      |                           矩形，参数为1时前后镜像，参数为2时，在1的基础上另外绘画一个90度旋转的矩形（交叉）                            |
| 0x5  |   角度（单位deg）   |                              扇形，如果需要角度为20的扇形，图形值为 `0x50000&#124;20`                              |

* 另有点线三角等图形参阅 [这里](./ff_draw/gui/__init__.py)

## 特殊值：关键字`key`

#### 关键字：now

* 类型： `any`
* 描述：设为创建时的数值，而不是即时数值

|  参数   |  类型   |  描述   |
|:-----:|:-----:|:-----:|
| value | `any` | 变量表达式 |

---

#### 关键字：arg

* 类型： `any`
* 描述：获取`foreach`赋值的变量

|  参数  |    类型    |   描述    |
|:----:|:--------:|:-------:|
| name | `string` | 获取变量的名字 |

---

#### 关键字：remain

* 类型： `number`
* 描述：当前图形的剩余时间

| 参数  | 类型  | 描述  |
|:---:|:---:|:---:|
|  -  |  -  |  -  |

---

#### 关键字：progress

* 类型： `number`
* 描述：当前图形的进度，为 0-1 之间的值

| 参数 | 类型  | 描述  |
|:---:|:---:|:---:|
|  -  |  -  |  -  |

---

#### 关键字：is_hit

* 类型： `1/0`
* 描述：当前图形是否在xz轴上覆盖某个坐标

| 参数  |     类型      |  描述   |
|:---:|:-----------:|:-----:|
| pos | `number[3]` | 查询坐标 |

---

#### 关键字：count_hit_actor

* 类型： `number`
* 描述：当前图形覆盖了多少个actor

| 参数  |     类型     |     描述      |
|:---:|:----------:|:-----------:|
| ids | `number[]` | actor id 列表 |

---

#### 关键字：eval

* 类型： `any`
* 描述：输入python表达式并获取返回 （本特殊值未来可能因为安全原因弃用，请避免使用）

|  参数  |       类型       |    描述    |
|:----:|:--------------:|:--------:|
| code |    `string`    | python表达式 |
| args | `map[str,any]` | 表达式用到的变量 |

---

#### 关键字：actor_pos

* 类型： `number[3]`
* 描述：返回对应实体的位置

|  参数  |      类型       |    描述    |
|:----:|:-------------:|:--------:|
|  id  |    number     |   实体id   |

---

#### 关键字：actor_facing

* 类型： `number`
* 描述：返回对应实体的面向

|  参数  |      类型       |    描述    |
|:----:|:-------------:|:--------:|
|  id  |    number     |   实体id   |

---

#### 关键字：actor_has_status

* 类型： `1/0`
* 描述：返回角色是否拥有某状态

|    参数     |   类型   |   描述    |
|:---------:|:------:|:-------:|
|    id     | number |  实体id   |
| status_id | number |  状态id   |
| source_id | number | 来源id，可选 |

---

#### 关键字：actor_status_remain

* 类型： `number`
* 描述：返回角色某状态的剩余时间，无则为0

|    参数     |   类型   |   描述    |
|:---------:|:------:|:-------:|
|    id     | number |  实体id   |
| status_id | number |  状态id   |
| source_id | number | 来源id，可选 |

---

#### 关键字：actor_status_param

* 类型： `number`
* 描述：返回角色某状态的参数，无则为0

|    参数     |   类型   |   描述    |
|:---------:|:------:|:-------:|
|    id     | number |  实体id   |
| status_id | number |  状态id   |
| source_id | number | 来源id，可选 |

---

#### 关键字：actor_status_source

* 类型： `number`
* 描述：返回角色某状态的来源id，无则为0

|    参数     |   类型   |   描述    |
|:---------:|:------:|:-------:|
|    id     | number |  实体id   |
| status_id | number |  状态id   |

---

#### 关键字：actor_exists

* 类型： `1/0`
* 描述：该id对应的实体是否存在

|  参数  |      类型       |    描述    |
|:----:|:-------------:|:--------:|
|  id  |    number     |   实体id   |

---

#### 关键字：actor_can_select

* 类型： `1/0`
* 描述：该id对应的实体是否能被选中

|  参数  |      类型       |    描述    |
|:----:|:-------------:|:--------:|
|  id  |    number     |   实体id   |

---

#### 关键字：actor_is_visible

* 类型： `1/0`
* 描述：该id对应的实体是否可见

|  参数  |      类型       |    描述    |
|:----:|:-------------:|:--------:|
|  id  |    number     |   实体id   |

---

#### 关键字：actor_distance

* 类型： number
* 描述：两个实体之间的距离

| 参数  |      类型       |   描述   |
|:---:|:-------------:|:------:|
| a1  |    number     | 实体a的id |
| a2  |    number     | 实体b的id |

---

#### 关键字：player_by_distance_idx

* 类型： number
* 描述：根据与某实体的距离排序所有玩家并返回指定index的角色id（可能造成性能负担，谨慎使用）

| 参数  |      类型       |   描述    |
|:---:|:-------------:|:-------:|
| src  |    number     | 指定实体的id |
| idx  |    number     | 查询index |

---

#### 关键字：actor_relative_facing

* 类型： number
* 描述：src实体看向dst实体时的面向

| 参数  |      类型       |   描述    |
|:---:|:-------------:|:-------:|
| src |    number     | 来源实体的id |
| dst |    number     | 目标实体的id |

---

#### 关键字：me

* 类型： number
* 描述：当前操作角色的id

| 参数  |   类型   |   描述    |
|:---:|:------:|:-------:|
|  -  |   -    |    -    |

---

#### 关键字：target

* 类型： number
* 描述：指定实体的目标id

|  参数  |      类型       |    描述    |
|:----:|:-------------:|:--------:|
|  id  |    number     |   实体id   |

---

#### 关键字：fallback

* 类型： any
* 描述：尝试返回 `expr`值，如果出现任意错误则返回 `default`值

|  参数  | 类型  | 描述  |
|:----:|:---:|:---:|
| expr | any | 表达式 |
|  default  | any | 默认值 |

---

#### 关键字：if

* 类型： any
* 描述：如果 `cond!=0`，返回`true`，否则返回`false`

|  参数  | 类型  | 描述  |
|:----:|:---:|:---:|
| cond | any | 判断式 |
|  true  | any | 真值  |
|  false  | any |  假值  |

---

#### 关键字：gt

* 类型： `1/0`
* 描述：等价 `v1 > v2`

|  参数  | 类型  | 描述  |
|:----:|:---:|:---:|
| v1 | any | 数值1 |
|  v2  | any | 数值2 |

---

#### 关键字：lt

* 类型： `1/0`
* 描述：等价 `v1 < v2`

|  参数  | 类型  | 描述  |
|:----:|:---:|:---:|
| v1 | any | 数值1 |
|  v2  | any | 数值2 |

---

#### 关键字：gte

* 类型： `1/0`
* 描述：等价 `v1 >= v2`

|  参数  | 类型  | 描述  |
|:----:|:---:|:---:|
| v1 | any | 数值1 |
|  v2  | any | 数值2 |

---

#### 关键字：lte

* 类型： `1/0`
* 描述：等价 `v1 <= v2`

|  参数  | 类型  | 描述  |
|:----:|:---:|:---:|
| v1 | any | 数值1 |
|  v2  | any | 数值2 |

---

#### 关键字：add

* 类型： `number`
* 描述：返回 `values` 的总和（可以用于相加2/3/4元组）

|  参数  |    类型    | 描述  |
|:----:|:--------:|:---:|
| values | number[] | 数值 |

---

#### 关键字：mul

* 类型： `number`
* 描述：返回 `values` 的总乘

|  参数  |    类型    | 描述  |
|:----:|:--------:|:---:|
| values | number[] | 数值 |

---

#### 关键字：div

* 类型： `number`
* 描述：返回 `values` 的总除

|  参数  |    类型    | 描述  |
|:----:|:--------:|:---:|
| values | number[] | 数值 |

---

#### 关键字：min

* 类型： `number`
* 描述：返回 `values` 的最小值

|  参数  |    类型    | 描述  |
|:----:|:--------:|:---:|
| values | number[] | 数值 |

---

#### 关键字：max

* 类型： `number`
* 描述：返回 `values` 的最大值

|  参数  |    类型    | 描述  |
|:----:|:--------:|:---:|
| values | number[] | 数值 |

---

#### 关键字：string_format

* 类型： `string`
* 描述：`format`.format(*`args`)

|   参数   |   类型   | 描述  |
|:------:|:------:|:---:|
| format | string | 格式  |
|  args  | any[]  | 数值  |

---

#### 关键字：circle

* 类型： `(number, number[3])`
* 描述：用于 `shape_scale` 的特殊值，表述圆形

| 参数  |    类型    | 描述  |
|:---:|:--------:|:---:|
| range | number | 半径  |

---

#### 关键字：fan

* 类型： `(number, number[3])`
* 描述：用于 `shape_scale` 的特殊值，表述扇形

| 参数  |    类型    |  描述  |
|:---:|:--------:|:----:|
| deg | number | 扇形角度 |
| range | number |  半径  |

---

#### 关键字：donut

* 类型： `(number, number[3])`
* 描述：用于 `shape_scale` 的特殊值，表述环形

| 参数  |    类型    |  描述  |
|:---:|:--------:|:----:|
| inner | number | 内圈半径 |
| range | number | 外圈半径 |

---

#### 关键字：rect

* 类型： `(number, number[3])`
* 描述：用于 `shape_scale` 的特殊值，表述矩形

|  参数   |    类型    | 描述  |
|:-----:|:--------:|:---:|
| width | number | 宽度  |
| range | number | 长度  |

---

#### 关键字：cross

* 类型： `(number, number[3])`
* 描述：用于 `shape_scale` 的特殊值，表述十字

|  参数   |    类型    | 描述  |
|:-----:|:--------:|:---:|
| width | number | 宽度  |
| range | number | 长度  |

---

#### 关键字：action_shape

* 类型： `(number, number[3])`
* 描述：用于 `shape_scale` 的特殊值，表述某技能的形状（本接口无法判断扇形角度及月环内圈，统一输出90度扇形和50%月环）

|  参数   |    类型    |  描述  |
|:-----:|:--------:|:----:|
|  id   | number | 技能id |

---

#### 关键字：destroy_omen

* 类型： `None`
* 描述：用于 `shape_scale` 或 `shape` 的特殊值，会返回0并将omen销毁

| 参数 | 类型  | 描述  |
|:---:|:---:|:---:|
|  -  |  -  |  -  |

---

#### 关键字：actors_by_type

* 类型： `number[]`
* 描述：返回符合 actor_type 的 id 列表

| 参数 |   类型   |          描述          |
|:---:|:------:|:--------------------:|
|  type  | number | 1：玩家，2：战斗npc，3：事件npc |

---

#### 关键字：actors_by_base_id

* 类型： `number[]`
* 描述：返回符合 base_id 的 id 列表

| 参数  |   类型   |   描述    |
|:---:|:------:|:-------:|
| id  | number | base_id |

---

#### 关键字：actors_in_party

* 类型： `number[]`
* 描述：返回队伍中所有人的id

| 参数  | 类型  | 描述  |
|:---:|:---:|:---:|
|  -  |  -  |  -  |

---

#### 关键字：pi

* 类型： `number`
* 描述：返回pi的倍数

| 参数  |   类型   |  描述   |
|:---:|:------:|:-----:|
|  val  | number | 返回的倍数 |

---

#### 关键字：rad_deg

* 类型： `number`
* 描述：在rad和deg间转换

| 参数  | 类型 |         描述         |
|:---:|:------:|:------------------:|
| rad | number |  优先判断，将rad转换为deg   |
| deg | number | 如果rad为空，将deg转换为rad |

## 插件开发

* 编写python模块置于plugins文件夹中，会自动导入
* `update(main:FFDraw)->any` 每帧调用，一般用于直接调用gui进行绘制
* `process_command(command:dict)->bool` httpapi在找不到指令cmd时调用，返回true为已处理
