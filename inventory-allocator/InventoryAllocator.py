from typing import OrderedDict, Dict
from collections import defaultdict


class InventoryAllocator:
    """
    Class used to store warehouse data and allocate shipments
    
    ...

    Methods
    -------

    allocate_shipment(order)
        Allocate's the given shipment accross different warehouses
    
    add_warehouse_inventory(inventory)
        Used to re-stock/add items to the warehouses.
    
    InventoryAllocator(inventory)
        Creates an instance of the class with the inventory set to what is passed.
    """

    def _load_warehouse_data(self, inventory: Dict):
        """
        Private function that either sets inventory for warehouses if not present, or updates them if already present.

        Parameters
        ---------
        inventory : Dict
            Dictionary containing information about single/multiple warehouses and their inventory
        """

        for warehouse in inventory:
            # if information about warehouse already exists, update it with new data
            if warehouse["name"] in self.warehouse_data:
                for item, quantity in warehouse["inventory"].items():
                    if item in self.warehouse_data[warehouse["name"]]:
                        self.warehouse_data[warehouse["name"]][item] = (
                            quantity + self.warehouse_data[warehouse["name"]][item]
                        )
                    else:
                        self.warehouse_data[warehouse["name"]][item] = warehouse[
                            "inventory"
                        ][item]
            # first time encountering warehouse, initialize its inventory data
            else:
                self.warehouse_data[warehouse["name"]] = warehouse["inventory"]

    def __init__(self, inventory: Dict):
        """
        Constructor that initializes the warehouse inventory for the class.

        Parameters
        ---------
        inventory : Dict
            Dictionary containing information about single/multiple warehouses and their inventory
        """

        self.warehouse_data: OrderedDict[str, Dict[str, int]] = OrderedDict()
        self._load_warehouse_data(inventory)

    def add_warehouse_inventory(self, inventory: Dict):
        """
        Public function used to update/add new inventory to the warehouses of the class.

        Parameters
        ---------
        inventory : Dict
            Dictionary containing information about single/multiple warehouses and their inventory
        """
        self._load_warehouse_data(inventory)

    def _update_warehouse_item_quantity(
        self, warehouse_name: str, item_name: str, item_stock: int
    ):
        """
        Private function used to update inventory of items in the warehouse when they are consumed.

        Parameters
        ---------
        warehouse_name : str
            Name of warehouse that contains item quantity that needs updating
        
        item_name : str
            Name of item that needs updating

        item_stock : int
            New quantity/stock of item
        
        """
        self.warehouse_data[warehouse_name][item_name] = item_stock

    def allocate_shipment(self, order: Dict):
        """
        Public function used to find the cheapest way to ship the given order.

        Parameters
        ---------
        order : Dict
            Dictionary containing order information, ie. dict of the items (name and quantity) needed to be shipped.
        """

        warehouse_item_distribution = defaultdict(lambda: {})
        for item_name, quantity_required in order.items():
            inventory_distribution = dict()

            for warehouse_name, warehouse_inventory in self.warehouse_data.items():
                # if warehouse does not contain item, skip it
                if (
                    item_name not in warehouse_inventory
                    or warehouse_inventory[item_name] < 1
                ):
                    continue

                item_stock = warehouse_inventory[item_name]

                # if we have enough of item in warehouse, take it and break
                if quantity_required <= item_stock:
                    inventory_distribution[warehouse_name] = quantity_required
                    item_stock -= quantity_required
                    quantity_required = 0
                    self._update_warehouse_item_quantity(
                        warehouse_name, item_name, item_stock
                    )
                    break
                # if we don't have enough in this warehouse, take as much as possible and check next
                elif quantity_required > item_stock:
                    inventory_distribution[warehouse_name] = item_stock
                    quantity_required -= item_stock
                    item_stock = 0
                    self._update_warehouse_item_quantity(
                        warehouse_name, item_name, item_stock
                    )

            # if we require more of the item after checking all warehouses, we do not have enough, no allocations
            if quantity_required > 0:
                return []

            for warehouse_name, item_quantity in inventory_distribution.items():
                warehouse_item_distribution[warehouse_name][item_name] = item_quantity

        return [{name: items} for name, items in warehouse_item_distribution.items()]
