Inventory management system

1.Purprose

- This inventory management system helps a business record, track, monitor and analyze its inventory.

The system should provide an accurate view of:
  - Products available.
  - Current stock quantities
  - Product prices
  - Stock value
  - Low stock 
  - Out of stock
  - Potential profit
  - Inventory changes

2 Example  Business
 - The system can be used by a shop selling household products such as:
  --Flasks, Plates, Curtains, Flower Vases, Storage Containers, Cups, Thermos, Spoons

3. System Inputs
-The system receives information about:

Product information
-Product name
-Product category
-Product/SKU code
-Buying Price
-Selling Price
-Low-stock threshold
-Initial stock quantity

Inventory changes
-Stock received
-Stock sold
-Damaged stock
-Missing stock
-Stock adjustment


4. Business Rules
Stock Calculation
Current stock is calculated from inventory movements.
 current stock = Opening stock + stock received - stock sold - Damaged stock - missing stock +/- Stock Adjustments 

 Stock status 
 IF current_stock = 0
     status = OUT OF STOCK
  
  ELSE IF current_stock <= low_stock_threshold 
       status = Low
   ESLE 
      status = IN STOCK
 Inventory cost value

 Inventory Cost Value = 
 Current Stock * Buying Price

 Potential selling value

 Potential selling Value = 
 Current Stock * Selling Price

 Potential Gross Profit

 Potential Gross Profit = 
 Potential Selling Value - Inventory Cost Value

 5 Systsem Processing
 The system processes inventory data to determine:

 - Current stock quantity
 - Stock satus 
 - Inventory cost value
 - Potential gross profit
 - Low-stock products
 - Out-of-stock products
 - Overall inventory totals

 6.System Outputs

 Product-level outputs

 For each product, the system should display:

 - Product name
 - Current quantity
 - Buying price
 - selling price
 - Inventory cost value
 - Potential selling value






