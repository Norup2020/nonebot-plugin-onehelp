"""
Help docs
"""
import inspect

import nonebot.matcher as matcher
from nonebot import on_command
from nonebot.adapters.cqhttp import Bot, Event

try:
    from nonebot.plugin import plugins # pylint: disable=no-name-in-module
except:
    plugins = {}
__plugin_name__ = 'help'

# pylint: disable=unused-argument
# pylint: disable=invalid-name
# pylint: disable=consider-iterating-dictionary

def get_doc(matcher_):
    """
    Render a docs of a matcher
    """
    if hasattr(matcher_,"module_name"):
        return "\n".join([inspect.cleandoc(handler_.func.__doc__) for handler_ in matcher_.handlers
                      if handler_.func.__doc__])
    
    return None

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
        for i in matchers_list:
            if reg.get((i.plugin_name, i.module_name)):
                reg[(i.plugin_name, i.module_name)] += get_doc(i)
            else:
                reg[(i.plugin_name, i.module_name)] = get_doc(i) or ""
        self.reg = reg

    def get_keys(self, key=None, value=None) -> str:
        """
        get_keys Get the key of the reg

        :return: the docs of the module
        :rtype: str
        """
        if all((key, value)):
            res = self.reg.get((key, value))
            if res:
                return "用法: " + res
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
                return "用法: \n" + self.reg[kv_list[0]]
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







class InspectReg:
    def __init__(self) -> None:
        regs = {}


        def generate_docs(module,dic,name):
            self_matchers = inspect.getmembers(module,
                lambda member:issubclass(
                    type(member),matcher.MatcherMeta))
            plugin_dict = dict([
                (matcher_name,get_doc(matcher_)) \
                for matcher_name,matcher_ in self_matchers \
                if get_doc(matcher_) != None])
            if plugin_dict:
                dic.setdefault(name,plugin_dict)

            doc_string = module.__doc__
            if doc_string:
                dic.get(name,dic).setdefault("__doc__",doc_string.strip())

        for pluginkey,pluginv in plugins.items():
            subreg = {}
            generate_docs(pluginv.module,subreg,"__init__")

            subplugin_ = inspect.getmembers(pluginv.module,inspect.ismodule)

            for subname,items in subplugin_:
                generate_docs(items,subreg,subname)
            if subreg:
                regs.setdefault(pluginkey,subreg)

        self.dict = regs

    def get_plugins(self):
        res = ""
        for i,j in self.dict.items():
            res += f"{i}"
            if j.get("__init__",{}).get("__doc__") or j.get("__doc__"):
                print(i)
                print(j,flush=True)
                res += "\t"
                res += (j.get("__init__",{}).get("__doc__") or j.get("__doc__")).splitlines()[0]
            res += "\n"
        return "已安装插件:\n-----\n" + res

    def get_plugin(self,plugin_name):
        
        plugin = self.dict.get(plugin_name)
        print(plugin)
        res = plugin_name  
        if plugin.get("__init__",{}).get("__doc__") or plugin.get("__doc__"):
            res += "\n"
            res += plugin.get("__init__",{}).get("__doc__","") or plugin.get("__doc__","")
        res += "\n-----\n"
        for subpln,subplv in plugin.items():
            if subpln != "__doc__":
                res += subpln + "\n"
            if  isinstance(subplv,dict):
                res += subplv.get("__doc__","")
                mmm = ""
                for matcher_name in subplv.keys():
                    if matcher_name == "__doc__":
                        continue
                    mmm += f"\t{matcher_name}\n"
                if mmm:
                    res += "\n" + mmm
        print(res)
        return res


## main and test matcher

help_ = on_command('help')


@help_.handle()
async def _help(bot: Bot, event: Event, state: dict):
    """
    help 命令名称
    help 什么都不填 -> 获取所有命令
    """
    args = str(event.message).strip().split(maxsplit=1)

    reg = Reg()

    await help_.send(reg.get_keys(*args))


testinghelp = on_command('testinghelp')


@testinghelp.handle()
async def _testinghelp(bot: Bot, event: Event, state: dict):
    """
    hee
    """

    arg = str(event.message).strip()
    print(arg)
    inspect_reg = InspectReg()
    print(inspect_reg.dict)
    if not arg:
        await heee.send(inspect_reg.get_plugins())
    else:
        await heee.send(inspect_reg.get_plugin(arg))