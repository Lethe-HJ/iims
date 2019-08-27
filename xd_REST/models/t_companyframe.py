# coding: utf-8

from sqlalchemy import Integer, Date, Unicode, Numeric, exc, Table
from sqlalchemy import Column, DateTime, String, desc
from . import Base, metadata
from xd_REST import session
from xd_REST.models.t_staff import TStaff
import copy

t_T_CompanyFrame = Table(
    'T_CompanyFrame', metadata,
    Column('ID', Integer),
    Column('Level', Integer),
    Column('Name', String(30, 'Chinese_PRC_CI_AS')),
    Column('ParentId', Integer),
    Column('AllParentId', String(1024, 'Chinese_PRC_CI_AS')),
    Column('IsLeaf', Integer),
    Column('ChildId', String(1024, 'Chinese_PRC_CI_AS')),
    Column('AllChildId', String(1024, 'Chinese_PRC_CI_AS')),
    Column('TreeNodeName', String(30, 'Chinese_PRC_CI_AS')),
    Column('IsShow', Integer),
    Column('Reserve', String(200, 'Chinese_PRC_CI_AS')),
    Column('staff', String(1024, 'Chinese_PRC_CI_AS'))
)


class FrameTree:
    def __init__(self, pattern):
        self.t_frame = t_T_CompanyFrame
        self.node = {
            "ID": -1,
            "Name": "",
            # "parents": [],
            "children": [],
            "children_li": [],
            "staff_li": [],
            "level": -1,
        }
        self.staff = {
            "ID": -1,
            "Name": "",
        }
        self.node_li = self.get_node_li()
        self.root = None
        self.pattern = pattern

    def get_node_li(self):
        """
        获取结点列表
        :return:
        """
        node_li = []
        frams = session.query(self.t_frame).all()
        for fram in frams:
            new_code = copy.deepcopy(self.node)
            new_code["ID"] = fram.ID
            new_code["Name"] = fram.Name
            new_code["children_li"] = fram.ChildId.strip(',').split(',') if fram.ChildId else []
            new_code["staff_li"] = fram.staff.strip(',').split(',') if fram.staff else []
            print(new_code["staff_li"])
            new_code["level"] = fram.Level
            node_li.append(new_code)
        print("-----------------------------------------------")
        return node_li

    def build_tree(self):
        """
        构造树
        :return:
        """
        self.root = self.node_li[0]
        self.build_sub_tree(self.root)
        return self.root

    def build_sub_tree(self, node):
        """
        递归构建子树
        :param node:
        :return:
        """
        if node["children_li"] == []:
            self.add_staff(node)
            return
        for i in range(0, len(self.node_li)):
            if str(self.node_li[i]["ID"]) in node["children_li"]:
                node["children"].append(self.node_li[i])  # 将字典添加进集合中
                self.build_sub_tree(node["children"][-1])
        for child in node["children"]:
            self.add_staff(child)

    def add_staff(self, node):
        if node["staff_li"] is not []:
            print(node["staff_li"])
            for staff_id in node["staff_li"]:
                staff = copy.deepcopy(self.staff)
                staff["ID"] = int(staff_id)
                name_ob = session.query(TStaff.StaffName).filter_by(ID=staff["ID"]).first()
                staff["Name"] = name_ob[0] if name_ob else ""
                node["children"].append(staff)






