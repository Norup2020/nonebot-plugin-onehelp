# nonebot-plugin-onehelp

这是一个旨在让开发者更流畅为编写的插件添加文档的插件,然而因为当年的骚操作原因, 弄出了两条风格完全不同的开发路线dev和dev2

## dev

dev路线是相对正常的一个开发路线,其风格类似于常见的[nonebot-plugin-help](https://github.com/XZhouQD/nonebot-plugin-help))插件

通过`nonebot.matcher.matchers`的`Matcher`列表读取全部的`Matcher`, 从其中读取其层级, 再通过读取被 *`handler`函数* 装饰的函数的`__doc__`以完成读取

以下是例子

```python3
some_cmd = on_command("some_cmd") #定义一个Matcher

@some_cmd.handle() # handler函数之一
async _(): #这是被装饰的函数
    """这一行的东西就叫做__doc__了"""
    await some_cmd.send("some_reply")
```

注: 本文所称的 *`handler`函数* ,除非另有说明,均表示`Matcher`可以添加入`Matcher.handlers`的`Matcher`自带装饰器函数(如`Matcher.handle`,`Matcher.got`,`Matcher.recive`)

但是, 仍然需要使用`__plugin_name__`这样的变量以作为插件名称,这使得这条路线仍然难以摆脱添加变量这样的不流畅操作, 尽管在`nonebot1`时代这种变量还是可以容忍的

### dev:TODO

+ 摆脱`__plugin_name__`这样的变量
+ 更高程度的自定义

## dev2 

dev2路线是相对奇怪的一个开发路线,其风格极度*诡异*且 ***黑魔法***

通过`inspect.getmembers`获取所有的`module`, 然后再通过`MatcherMeta`过滤, 获取所有的`Matcher`, 最后归档

`module`的判断极度容易出错,尤其是真的引入模块的时候

例子

```python3
import nonebot
### 这将会读取nonebot模块的文档
```

现存的bug主要就是模块误读以及层级读取失误

### dev2:TODO

+ 修好bug
+ 修好bug