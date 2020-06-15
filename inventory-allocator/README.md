## Solution

#### Author: Nikshep Saravanan
#### Email: nikshepsvn@gmail.com

I have used Python 3 to solve this problem. Below is a high-level overview of my approach to solve this problem and some notes on the implementation.

### Implementation

#### Calling the method
 
I started off by implementing the `InventoryAllocator` class and the `allocate_shipment` method. 

We initialize the class by calling it with the warehouse inventory data as such `InventoryAllocator(inventory_data)`.

We can then pass the order to the allocate_shipment method as such `allocate_shipment(order)` to get the cheapest possible shipment.

Both of these combined would look like the following

```
inventory_data = [{ "name": "owd", "inventory": { "apple": 1 } }]
order = { "apple": 1 }

inventory_allocator = InventoryAllocator(inventory_data)
result = inventory_allocator.allocate_shipment(order)

print(result) 
> [{ owd: { apple: 1 } }]

```

#### Bonus
In order to enable `InventoryAllocator` to be re-used for multiple orders/shipments I have implemented an additional `add_warehouse_inventory` method that can be used to update the inventories of items in the warehouses of the current `InventoryAllocator`. This way as items are re-stocked/added, we can update our `InventoryAllocator`, and re-use it to create new shipments by calling the `allocate_shipment` method.

```
inventory_data = [{ "name": "owd", "inventory": { "apple": 1 } }]
inventory_allocator = InventoryAllocator(inventory_data)

print(inventory_allocator.warehouse_data) 
> [('owd', {'apple': 1})]

new_inventory_data = [{ "name": "owd", "inventory": { "apple": 5 } }]
inventory_allocator.add_warehouse_inventory(new_inventory_data)

print(inventory_allocator.warehouse_data) 
> [('owd', {'apple': 6})]

new_inventory_data = [{ "name": "owd", "inventory": { "orange": 1 } }]
inventory_allocator.add_warehouse_inventory(new_inventory_data)

print(inventory_allocator.warehouse_data) 
> [('owd', {'apple': 6, 'orange': 1})]
```


#### The approach 

My approach to solve the problem is rather simple:
1. I start off my iterating through the items in our order and checking each item agaisnt all the warehouses. 
    1. If the warehouse can fulfill our item, we save that information and move on to our next item.
    2. If not, we fulfill as much of the item as we can and check the next warehouse. 
    3. In the end, if we are not able to fulfill an item completely then we do not allocate the order.
2. After fulfilling a single item, we take the next item, and check all the warehouses (in order of cost) and so on.

### Unit tests

The tests I have written are as follows:

* Exact match
* Not enough inventory -> no allocations!
* Split single item across warehouses if only way to ship item
* Split multiple item across warehoses if only way to ship item
* Take item from cheapest warehouse when given choice
* Handle case where warehouse 'has' item but 0 quantity
* Not enough inventory for some items -> no allocations!
* Not enough inventory for mutliple items -> no allocations!
* Item quantity is updated in a warehouse in inventory
* Item is added to a warehouse in inventory
* Warehouse is added to inventory

To run the unit tests, run `python3 InventoryAllocatorTest.py`


&nbsp;
-----

### Problem

The problem is compute the best way an order can be shipped (called shipments) given inventory across a set of warehouses (called inventory distribution). 

Your task is to implement InventoryAllocator class to produce the cheapest shipment.

The first input will be an order: a map of items that are being ordered and how many of them are ordered. For example an order of apples, bananas and oranges of 5 units each will be 

`{ apple: 5, banana: 5, orange: 5 }`

The second input will be a list of object with warehouse name and inventory amounts (inventory distribution) for these items. For example the inventory across two warehouses called owd and dm for apples, bananas and oranges could look like

`[ 
    {
    	name: owd,
    	inventory: { apple: 5, orange: 10 }
    }, 
    {
    	name: dm:,
    	inventory: { banana: 5, orange: 10 } 
    }
]`

You can assume that the list of warehouses is pre-sorted based on cost. The first warehouse will be less expensive to ship from than the second warehouse. 

You can use any language of your choice to write the solution (internally we use Typescript/Javascript, Python, and some Java). Please write unit tests with your code, a few are mentioned below, but these are not comprehensive. Fork the repository and put your solution inside of the src directory and include a way to run your tests!

### Examples

*Happy Case, exact inventory match!**

Input: `{ apple: 1 }, [{ name: owd, inventory: { apple: 1 } }]`  
Output: `[{ owd: { apple: 1 } }]`

*Not enough inventory -> no allocations!*

Input: `{ apple: 1 }, [{ name: owd, inventory: { apple: 0 } }]`  
Output: `[]`

*Should split an item across warehouses if that is the only way to completely ship an item:*

Input: `{ apple: 10 }, [{ name: owd, inventory: { apple: 5 } }, { name: dm, inventory: { apple: 5 }}]`  
Output: `[{ dm: { apple: 5 }}, { owd: { apple: 5 } }]`

### What are we looking for

We'll evaluate your code via the following guidelines in no particular order:

1. **Readability**: naming, spacing, consistency
2. **Correctness**: is the solution correct and does it solve the problem
1. **Test Code Quality**: Is the test code comperehensive and covering all cases.
1. **Tool/Language mastery**: is the code using up to date syntax and techniques. 
