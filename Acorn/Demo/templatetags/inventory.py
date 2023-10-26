from Inventory.models import Category, ProductInventory
from django.template import Library

from typing import Self

register = Library()



class TreeNode:
    def __init__(self, obj: Category, children: list[Self] = []):

        self.obj = obj
        self.children = children



@register.simple_tag
def get_categories_list():

    categories_list = Category.objects.filter(
        is_active=True
    ).order_by("name")

    def DFS(objects: list[Category]):
        if not objects:
            return []
        
        level = min([obj.get_level() for obj in objects])
        objects_on_level = [obj for obj in objects if obj.level == level]
        tree = []

        for obj in objects_on_level:
            children = obj.get_children()
            obj_node = TreeNode(obj, DFS(children))
            tree.append(obj_node)

        return tree
    
    cat_list = DFS(categories_list)
    
    return cat_list


@register.simple_tag(name="get_objects_count")
def get_category_objects_count(id):
    products_count = ProductInventory.objects.filter(
        product__category__id=id
    ).count()

    return products_count