from pprint import pprint
from typing import List, Any, AnyStr, Union

from waapi import WaapiClient, CannotConnectToWaapiException


class WaClient(WaapiClient):
    FUNC_GET_INFO = 'ak.wwise.core.getInfo'
    FUNC_GET_SELECTED = 'ak.wwise.ui.getSelectedObjects'
    FUNC_GET = 'ak.wwise.core.object.get'
    FUNC_CREATE = 'ak.wwise.core.object.create'

    GET_SELECTED_OPTIONS = {
        'return': [
            'id',  # 对象的 ID
            'name',  # 对象的名称
            'notes',  # 备注
            'type',  # 对象类型
            'path',  # 对象路径
            'parent',  # 父对象，{'id':'xx', 'name':'xx'}
            'owner',  # 对象的所有者，这适用于被其他对象本地拥有的对象，如自定义效果、自定义衰减等。
            'shortId',  # 短 ID，int
            'category',  # 分类
            'filePath',  # 文件路径
            'workunit',  # 对象所属 workunit，{'id':'xx', 'name':'xx'}
            'workunit:isDefault',  # workunit 是否是默认，bool
            'workunit:type',  # workunit 类型，可以是："folder", "rootFile", "nestedFile"
            'workunit:isDirty',  # 如果返回 True，表示这个 workunit 为修改过，未保存状态
            'childrenCount',  # 子对象数量，只找一层，int
            'sound:originalWavFilePath',  # sound 对应的 wav文件路径
            'sound:convertedWemFilePath',  # sound 对应的 wem文件路径
            'soundbank:bnkFilePath',  # sound 对应的 bank文件路径
            '@Volume',
            '@IsVoice',
            '@OutputBus'
        ]
    }

    def __init__(self):
        super().__init__()

    def get_info(self):
        result = self.call(self.FUNC_GET_INFO)
        version = result['version']['displayName']
        print(f'Wwise版本：{version}')
        return version

    def get_selected(self) -> List:
        """获取选中的对象列表，可多选"""
        result = self.call(self.FUNC_GET_SELECTED, options=self.GET_SELECTED_OPTIONS)
        return result['objects']

    def get_selected_id(self) -> List:
        """获取选中对象的 ID列表，可多选"""
        lis = []
        for i in self.get_selected():
            lis.append(i['id'])
        return lis

    def get_obj_by_id(self, id_list: List):
        """通过 ID列表，获取对象列表，适用于已知 ID，其他未知的情况"""
        args = {'from': {'id': id_list}}
        result = self.call(self.FUNC_GET, args, options=self.GET_SELECTED_OPTIONS)
        return result['return']

    def get_parent_matches(self, id_list: List, name_pattern='.+') -> List:
        """
        通过 ID列表，获取名称符合正则表达式的，父级级对象，返回一个列表
        :param id_list: ID列表，如：['{906E2637-B380-439E-A1A6-CE0118406ED2}']
        :param name_pattern: 名称，正则表达式，默认匹配任意字符
        :return: 对象列表
        """
        args = {
            'from': {'id': id_list},
            'transform': [
                {'select': ['parent']},
                {'where': ['name:matches', name_pattern]}
            ]
        }
        result = self.call(self.FUNC_GET, args, options=self.GET_SELECTED_OPTIONS)
        return result['return']

    def get_ancestors_matches(self, id_list: List, name_pattern='.+') -> List:
        """
        通过 ID列表，获取名称符合正则表达式的，所有父级对象，返回一个列表
        :param id_list: ID列表，如：['{906E2637-B380-439E-A1A6-CE0118406ED2}']
        :param name_pattern: 名称，正则表达式，默认匹配任意字符
        :return: 对象列表
        """
        args = {
            'from': {'id': id_list},
            'transform': [
                {'select': ['ancestors']},
                {'where': ['name:matches', name_pattern]}
            ]
        }
        result = self.call(self.FUNC_GET, args, options=self.GET_SELECTED_OPTIONS)
        return result['return']

    def get_children_matches(self, id_list: List, name_pattern='.+') -> List:
        """
        通过 ID列表，获取名称符合正则表达式的，子级对象，返回一个列表
        :param id_list: ID列表，如：['{906E2637-B380-439E-A1A6-CE0118406ED2}']
        :param name_pattern: 名称，正则表达式，默认匹配任意字符
        :return: 对象列表
        """
        args = {
            'from': {'id': id_list},
            'transform': [
                {'select': ['children']},
                {'where': ['name:matches', name_pattern]}
            ]
        }
        result = self.call(self.FUNC_GET, args, options=self.GET_SELECTED_OPTIONS)
        return result['return']

    def get_descendants_matches(self, id_list: List, name_pattern='.+') -> List:
        """
        通过 ID列表，获取名称符合正则表达式的，所有子对象，返回一个列表
        :param id_list: ID列表，如：['{906E2637-B380-439E-A1A6-CE0118406ED2}']
        :param name_pattern: 名称，正则表达式，默认匹配任意字符
        :return: 对象列表
        """
        args = {
            'from': {'id': id_list},
            'transform': [
                {'select': ['descendants']},
                {'where': ['name:matches', name_pattern]}
            ]
        }
        result = self.call(self.FUNC_GET, args, options=self.GET_SELECTED_OPTIONS)
        return result['return']

    def get_parent_contains(self, id_list: List, name_pattern='') -> List:
        """
        通过 ID列表，获取名称符包含子串的，父级级对象，返回一个列表
        :param id_list: ID列表，如：['{906E2637-B380-439E-A1A6-CE0118406ED2}']
        :param name_pattern: 名称子串，默认匹配任意字符
        :return: 对象列表
        """
        args = {
            'from': {'id': id_list},
            'transform': [
                {'select': ['parent']},
                {'where': ['name:contains', name_pattern]}
            ]
        }
        result = self.call(self.FUNC_GET, args, options=self.GET_SELECTED_OPTIONS)
        return result['return']

    def get_ancestors_contains(self, id_list: List, name_pattern='') -> List:
        """
        通过 ID列表，获取名称符包含子串的，所有父级对象，返回一个列表
        :param id_list: ID列表，如：['{906E2637-B380-439E-A1A6-CE0118406ED2}']
        :param name_pattern: 名称子串，默认匹配任意字符
        :return: 对象列表
        """
        args = {
            'from': {'id': id_list},
            'transform': [
                {'select': ['ancestors']},
                {'where': ['name:contains', name_pattern]}
            ]
        }
        result = self.call(self.FUNC_GET, args, options=self.GET_SELECTED_OPTIONS)
        return result['return']

    def get_children_contains(self, id_list: List, name_pattern='') -> List:
        """
        通过 ID列表，获取名称符包含子串的，子级对象，返回一个列表
        :param id_list: ID列表，如：['{906E2637-B380-439E-A1A6-CE0118406ED2}']
        :param name_pattern: 名称子串，默认匹配任意字符
        :return: 对象列表
        """
        args = {
            'from': {'id': id_list},
            'transform': [
                {'select': ['children']},
                {'where': ['name:contains', name_pattern]}
            ]
        }
        result = self.call(self.FUNC_GET, args, options=self.GET_SELECTED_OPTIONS)
        return result['return']

    def get_descendants_contains(self, id_list: List, name_pattern='') -> List:
        """
        通过 ID列表，获取名称符包含子串的，所有子对象，返回一个列表
        :param id_list: ID列表，如：['{906E2637-B380-439E-A1A6-CE0118406ED2}']
        :param name_pattern: 名称子串，默认匹配任意字符
        :return: 对象列表
        """
        args = {
            'from': {'id': id_list},
            'transform': [
                {'select': ['descendants']},
                {'where': ['name:contains', name_pattern]}
            ]
        }
        result = self.call(self.FUNC_GET, args, options=self.GET_SELECTED_OPTIONS)
        return result['return']

    def get_type_matches(self, _type: AnyStr, name_pattern='.+') -> List:
        """
        通过类型，获取名称符合正则表达式的对象，返回一个列表
        :param _type: 对象类型，字符串
        :param name_pattern: 名称，正则表达式，默认匹配任意字符
        :return: 对象列表
        """
        args = {
            'from': {'ofType': [_type]},
            'transform': [
                {'where': ['name:matches', name_pattern]}
            ]
        }
        result = self.call(self.FUNC_GET, args, options=self.GET_SELECTED_OPTIONS)
        return result['return']

    def get_type_contains(self, _type: AnyStr, name_pattern='') -> List:
        """
        通过类型，获取名称包含子串的对象，返回一个列表
        :param _type: 对象类型，字符串
        :param name_pattern: 名称子串，默认匹配任意字符
        :return: 对象列表
        """
        args = {
            'from': {'ofType': [_type]},
            'transform': [
                {'where': ['name:contains', name_pattern]}
            ]
        }
        result = self.call(self.FUNC_GET, args, options=self.GET_SELECTED_OPTIONS)
        return result['return']

    def create_from_path(self, path: str):
        pass


if __name__ == '__main__':
    try:
        with WaClient() as client:
            client.get_info()
    except CannotConnectToWaapiException:
        print('waapi连接失败！')
    except Exception as e:
        print(f'出错啦！{e}')