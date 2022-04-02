# pylint: disable=unused-argument
# pylint: disable=invalid-name
# pylint: disable=consider-iterating-dictionary
import inspect
from typing import Any, Dict

import nonebot.matcher as matcher
from nonebot import on_command
from nonebot.plugin import plugin as plugin

"""
module_doc
"""

## just a function to test

sendyou = on_command("hh")

sendyou.handle()
async def you():
    """
    matcher docs
    """
    await matcher.send("you")


##


def get_doc(matcher_):
    """
    Render a docs of a matcher
    """
    return "\n".join([inspect.cleandoc(handler_.call.__doc__) for handler_ in matcher_.handlers
                      if handler_.call.__doc__])


class Reg:
    """
    reg:存储了各moudle的哈希表
    mkey:moudle的键，__plugin_name__
    reg[mkey]：返回一个Matcher的集合
    plugin > moudle > matcher
    """
    def __init__(self) -> None:
        mathcers = matcher.matchers.copy().values()
        matchers_list = []
        for group in mathcers:
            for matcher_ in group:
                matchers_list.append(matcher_)
        reg = {}
        plugins = plugin.plugins.copy()
        
        # for i in matchers_list:
        print(plugins["test"].module.__dict__)
        self.extrat(plugins)


        # print(*[(i.plugin,i.module) for i in matchers_list])
        for i in matchers_list:

            if reg.get((i.plugin_name, i.module_name)):
                reg[(i.plugin_name, i.module_name)] += "\n\n" + get_doc(i)
            else:
                reg[(i.plugin_name, i.module_name)] = get_doc(i) or ""
        self.reg = reg

    def extrat(self,pl:Dict[str,Any]):
        ma = [ [ j.__name__ for j in i.matcher] for i in pl.values()]
        print(ma)

        oo = [ [ j.module_name for j in i.matcher] for i in pl.values()]
        print([inspect.cleandoc(i.module.__doc__) if i.module.__doc__ else "" for i in pl.values()])
        print(list(zip(pl.keys(),oo)))

    def get_keys(self, key=None, value=None) -> str:
        """
        get_keys Get the key of the reg

        :return: the docs of the module
        :rtype: str
        """
        if all((key, value)):
            res = self.reg.get((key, value))
            if res:
                return f"{key}用法: " + res
            return "无结果"
        if not key and not value:
            res = set()
            for i, _ in self.reg.keys():
                res.add(i)
            return "已安装插件:\n" + "  ".join(list(res))
        if any((key, value)):
            kv_list = []
            for kk, vv in self.reg.keys():
                set_kv = {kk, vv, None} - {key, value}
                c1 = kk == vv and len(set_kv) < 1
                c2 = kk != vv and len(set_kv) < 2
                if c1 or c2:
                    kv_list.append((kk, vv))
            if not kv_list:
                return "无结果"
            if len(kv_list) == 1:
                return f"{key}用法: \n" + self.reg[kv_list[0]]
            else:
                res = {}
                for k_, v_ in kv_list:
                    if res.get(k_):
                        res[k_].append(v_)
                    else:
                        res[k_] = [v_]
                result = ""
                if len(res) > 1:
                    result = "查询到多种结果:\n"
                for k, v in res.items():
                    result += f"{k}的模块:\n\t"
                    result += "\n\t".join(v)
                    result += "\n"
                return result


help = on_command('help')

@help.handle()
async def _help(event):
    """
    help 命令名称
    help 什么都不填 -> 获取所有命令
    """
    reg = Reg()
    args = str(event.message).strip().split(maxsplit=1)

    await help.send(reg.get_keys(*args))

