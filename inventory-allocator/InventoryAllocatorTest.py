import unittest
from collections import OrderedDict
from InventoryAllocator import InventoryAllocator


class InventoryAllocatorTest(unittest.TestCase):
    def test_exact_match(self):
        """
        This test checks that the output for an order is correct when
        the quantity of the order item exactly matches that of the item in a warehouse
        """
        order = {"apple": 2}
        inventory = [{"name": "warehouse_one", "inventory": {"apple": 2}}]
        expected = [{"warehouse_one": {"apple": 2}}]

        inventory_allocator = InventoryAllocator(inventory)
        self.assertEqual(inventory_allocator.allocate_shipment(order), expected)

    def test_zero_inventory(self):
        """
        This test checks that the output for an order is correct when
        the quantity of the item in the warehouse is 0 or the item does not exist
        """
        order = {"apple": 5}
        inventory = [
            {"name": "warehouse_one", "inventory": {}},
            {"name": "warehouse_three", "inventory": {"apple": 0}},
        ]
        expected = []

        inventory_allocator = InventoryAllocator(inventory)
        self.assertEqual(inventory_allocator.allocate_shipment(order), expected)

    def test_single_item_split(self):
        """
        This test checks that the output for an order is correct when
        the item needs to be sourced from multiple warehouses for it to be fulfilled
        """
        order = {"apple": 12}
        inventory = [
            {"name": "warehouse_one", "inventory": {"apple": 0}},
            {"name": "warehouse_two", "inventory": {"apple": 6}},
            {"name": "warehouse_three", "inventory": {"apple": 12}},
        ]
        expected = [{"warehouse_two": {"apple": 6}}, {"warehouse_three": {"apple": 6}}]

        inventory_allocator = InventoryAllocator(inventory)
        self.assertEqual(inventory_allocator.allocate_shipment(order), expected)

    def test_multiple_item_split(self):
        """
        This test checks that the output for an order is correct when
        multiple items need to be sourced from multiple warehouses for them to be fulfilled
        """
        order = {"apple": 9, "orange": 1, "banana": 7, "pear": 0}
        inventory = [
            {"name": "warehouse_one", "inventory": {"banana": 2}},
            {"name": "warehouse_two", "inventory": {"apple": 6, "banana": 0}},
            {"name": "warehouse_three", "inventory": {"orange": 13, "apple": 3}},
            {"name": "warehouse_four", "inventory": {"apple": 7, "banana": 6}},
        ]
        expected = [
            {"warehouse_two": {"apple": 6}},
            {"warehouse_three": {"apple": 3, "orange": 1}},
            {"warehouse_one": {"banana": 2}},
            {"warehouse_four": {"banana": 5}},
        ]
        inventory_allocator = InventoryAllocator(inventory)
        self.assertEqual(inventory_allocator.allocate_shipment(order), expected)

    def test_precedence(self):
        """
        This test checks that the output for an order is correct when
        the item is available at multiple warehouses (cheapest needs to get picked first)
        """
        order = {"apple": 4}
        inventory = [
            {"name": "warehouse_one", "inventory": {"apple": 22}},
            {"name": "warehouse_two", "inventory": {"apple": 6}},
            {"name": "warehouse_three", "inventory": {"apple": 5}},
            {"name": "warehouse_four", "inventory": {"apple": 6}},
        ]
        expected = [{"warehouse_one": {"apple": 4}}]

        inventory_allocator = InventoryAllocator(inventory)
        self.assertEqual(inventory_allocator.allocate_shipment(order), expected)

    def test_zero_inventory_some(self):
        """
        This test checks that the output for an order is correct when
        some of the warehouses do not contain inventory of the item
        """
        order = {"apple": 4}
        inventory = [
            {"name": "warehouse_one", "inventory": {"apple": 0}},
            {"name": "warehouse_two", "inventory": {"orange": 15}},
            {"name": "warehouse_three", "inventory": {"apple": 4}},
            {"name": "warehouse_four", "inventory": {"apple": 11}},
        ]
        expected = [{"warehouse_three": {"apple": 4}}]

        inventory_allocator = InventoryAllocator(inventory)
        self.assertEqual(inventory_allocator.allocate_shipment(order), expected)

    def test_insufficent_single_multiple(self):
        """
        This test checks that the output for an order is correct when
        one item cannot be fulfilled but the others can
        """
        order = {"apple": 3, "orange": 6}
        inventory = [
            {"name": "warehouse_one", "inventory": {"apple": 1}},
            {"name": "warehouse_two", "inventory": {"apple": 2, "orange": 4}},
        ]
        expected = []

        inventory_allocator = InventoryAllocator(inventory)
        self.assertEqual(inventory_allocator.allocate_shipment(order), expected)

    def test_insufficent_multiple(self):
        """
        This test checks that the output for an order is correct when
        multiple items in the order cannot be fulfilled
        """
        order = {"apple": 33, "orange": 52}
        inventory = [
            {"name": "warehouse_one", "inventory": {"apple": 12}},
            {"name": "warehouse_two", "inventory": {"apple": 20, "orange": 49}},
        ]
        expected = []

        inventory_allocator = InventoryAllocator(inventory)
        self.assertEqual(inventory_allocator.allocate_shipment(order), expected)

    def test_item_quantity_update(self):
        """
        This test checks that the state of the warehouse is correct when
        an item quantity is updated 
        """
        inventory = [{"name": "warehouse_one", "inventory": {"apple": 1}}]
        new_inventory = [{ "name": "warehouse_one", "inventory": { "apple": 5 } }]
        expected = OrderedDict([("warehouse_one", {"apple": 6})])

        inventory_allocator = InventoryAllocator(inventory)
        inventory_allocator.add_warehouse_inventory(new_inventory)
        self.assertEqual(inventory_allocator.warehouse_data, expected)
    
    def test_item_update(self):
        """
        This test checks that the state of the warehouse is correct when
        an item is added to a warehouse
        """
        inventory = [{"name": "warehouse_one", "inventory": {"apple": 1}}]
        new_inventory = [{ "name": "warehouse_one", "inventory": { "orange": 5 } }]
        expected = OrderedDict([("warehouse_one", {"apple": 1, "orange": 5})])

        inventory_allocator = InventoryAllocator(inventory)
        inventory_allocator.add_warehouse_inventory(new_inventory)
        self.assertEqual(inventory_allocator.warehouse_data, expected)

    def test_warehouse_update(self):
        """
        This test checks that the state of the warehouse is correct when
        a warehouse with item is added
        """
        inventory = [{"name": "warehouse_one", "inventory": {"apple": 1}}]
        new_inventory = [{ "name": "warehouse_two", "inventory": { "orange": 5 } }]
        expected = OrderedDict([("warehouse_one", {"apple": 1}), ('warehouse_two', {'orange': 5})])

        inventory_allocator = InventoryAllocator(inventory)
        inventory_allocator.add_warehouse_inventory(new_inventory)
        self.assertEqual(inventory_allocator.warehouse_data, expected)


if __name__ == "__main__":
    unittest.main()
