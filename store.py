from transaction import Transaction
from datetime import datetime
import psycopg2
from psycopg2.extras import RealDictCursor

class Filter:
    def __init__(self, type: str = None, category: str = None, start_date: datetime = None, end_date: datetime = None):
        self.type = type
        self.category = category
        self.start_date = start_date
        self.end_date = end_date

class TypeAggregationFilter:
    def __init__(self, type: str = None, start_date: datetime = None, end_date: datetime = None):
        self.type = type
        self.start_date = start_date
        self.end_date = end_date
        
class CategoryAggregationFilter:
    def __init__(self, type: str = None, start_date: datetime = None, end_date: datetime = None, limit: int = 6):
        self.type = type
        self.start_date = start_date
        self.end_date = end_date
        self.limit = limit      
        
class AggregatedCategory:
    def __init__(self,category, total_amount):
        self.category = category
        self.total_amount = total_amount
        
    def get_formatted_total_amount(self):
        return f"€{self.total_amount}"

class Store:
    def __init__(self):
        pass
    
    def create_transactions(self, trx: Transaction):
        pass
    
    def get_transaction(self, index: int):
        pass
    
    def get_transactions(self, filter: Filter):
        pass
    
    def delete_transaction(self, index: int):
        pass
    
    def aggregate_by_category(self, filter: CategoryAggregationFilter):
        pass
    
    def aggregate_by_type(self, filter: TypeAggregationFilter):
        pass
  
class MemoryStore(Store):
    def __init__(self):
        super().__init__()
        self.list_of_trx :list[Transaction] = []
        
    def create_transactions(self, trx: Transaction):
        super().create_transactions(trx)
        self.list_of_trx.append(trx)
            
    def get_transaction(self, index: int): 
        super().get_transaction(index)
        return self.list_of_trx[index]
        
    def delete_transaction(self, index: int):
        super().delete_transaction(index)
        self.list_of_trx.pop(index)
        
    def get_transactions(self, filter: Filter):
        super().get_transactions(filter)
        filtered_tr_list = []
        for i in range(len(self.list_of_trx)):
            if filter.type != None and self.list_of_trx[i].transaction_type != filter.type:
                continue
            if filter.category != None and self.list_of_trx[i].category != filter.category:
                continue
            if filter.start_date != None and self.list_of_trx[i].date <= filter.start_date:
                continue
            if filter.end_date != None and self.list_of_trx[i].date > filter.end_date:
                continue
            filtered_tr_list.append(self.list_of_trx[i])
        return filtered_tr_list 
    
    def aggregate_by_type(self, filter: TypeAggregationFilter):
        super().aggregate_by_type(filter)
        
        aggregated_types = {}
        
        for i in range(len(self.list_of_trx)):
            if (
                filter.type == None or
                filter.type == self.list_of_trx[i].transaction_type
            ) and (
                filter.start_date == None or
                filter.start_date <= self.list_of_trx[i].date
            ) and (
                filter.end_date == None or
                filter.end_date >= self.list_of_trx[i].date
            ):
                if not self.list_of_trx[i].transaction_type in aggregated_types:
                    aggregated_types[self.list_of_trx[i].transaction_type] = self.list_of_trx[i].amount
                else:
                    aggregated_types[self.list_of_trx[i].transaction_type] += self.list_of_trx[i].amount
        return aggregated_types
            
    def aggregate_by_category(self, filter: CategoryAggregationFilter) -> list[AggregatedCategory]:
        super().aggregate_by_category(filter)
        filtered_map = {}
        type_flag = False
        start_date_flag = False
        end_date_flag = False
        
        for i in range(len(self.list_of_trx)):
            a = self.list_of_trx[i]
            if filter.type == None or filter.type == a.transaction_type:
                type_flag = True
            else:
                continue
            if filter.start_date == None or filter.start_date <= a.date:
                start_date_flag = True
            else:
                continue
            if filter.end_date == None or filter.end_date > a.date:
                end_date_flag = True
            else:
                continue
            if type_flag == True and start_date_flag == True and end_date_flag == True:
                if not a.category in filtered_map:
                    filtered_map[a.category] = a.amount
                else:
                    filtered_map[a.category] += a.amount
        category_list = self.convert_category_map_to_list(filtered_map)
        return self.sort_category_items(category_list)
    
    def convert_category_map_to_list(self,category_map: dict) -> list[AggregatedCategory]:
        """Converts a map of categories to a sorted list of categories"""
        category_list = []
        for item in category_map:
            categories = AggregatedCategory(item, category_map.get(item))
            category_list.append(categories)
        return category_list

    def sort_category_items(self, category_list: list[AggregatedCategory]) -> list[AggregatedCategory]:
        """Sorts a list of categories"""
        if len(category_list) < 2:
            return category_list
        else:
            less = []
            greater = []
            pivot = category_list[0]
            for i in range(1, len(category_list)):
                if category_list[i].total_amount <= pivot.total_amount:
                    less.append(category_list[i])
                else:
                    greater.append(category_list[i])
            return self.sort_category_items(greater) + [pivot] + self.sort_category_items(less)


class PostgreStore(Store):
    def __init__(self, dbname, user, password, host, port):
        self.conn = psycopg2.connect(
            dbname = dbname,
            user = user,
            password = password,
            host = host,
            port = port
        )
         
    def create_transactions(self, trx: Transaction):
        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO transactions (amount, type, category, transaction_datetime, description) VALUES (%s, %s, %s, %s, %s)", (trx.amount, trx.transaction_type, trx.category, trx.date, trx.description)
            )
            self.conn.commit()
            cur.close()
    
    def get_transaction(self, index: int):
        with self.conn.cursor() as cur:
            cur.execute("SELECT * from transactions where id = %s", (index)
            )
            row = cur.fetchone() 
            return(Transaction(row['amount'], row['category'], row['date'], row['transaction_type']))
    
    def get_transactions(self, filter: Filter):
        query = "SELECT * from transactions"
        conditions = []
        values = []
        if filter.type != None:
            conditions.append("type = %s")
            values.append(filter.type)
            
        if filter.category != None:
            conditions.append("category = %s")
            values.append(filter.category)
        
        if filter.start_date != None:
            conditions.append("transaction_datetime >= %s")
            values.append(filter.start_date)
            
        if filter.end_date != None:
            conditions.append("transaction_datetime <= %s")
            values.append(filter.end_date)
        
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, values)
            
            rows = cur.fetchall()
        rows_list = []
        for row in rows:
            rows_list.append(Transaction(
                amount = row['amount'],
                description = row['description'],
                date = row['transaction_datetime'],
                transaction_type= row['type'],
                category= row['category']
            ))
        return rows_list
    
    def delete_transaction(self, index: int):
        pass
    
    def aggregate_by_category(self, filter: CategoryAggregationFilter):
        pass
    
    def aggregate_by_type(self, filter: TypeAggregationFilter):
        pass
