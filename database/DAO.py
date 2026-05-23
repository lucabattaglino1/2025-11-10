from database.DB_connect import DBConnect
from model.order import Order

from model.store import Store


class DAO():
    @staticmethod
    def getAllStores():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT * from stores"

        cursor.execute(query)

        for row in cursor:
            results.append(Store(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllNodes(store_name):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT o.order_id, o.customer_id, o.order_status, o.order_date, o.required_date, o.shipped_date, o.store_id, o.staff_id
                    FROM orders o, staff st, stores sr
                    WHERE sr.store_id = st.store_id 
                    and st.staff_id = o.staff_id 
                    and sr.store_name = %s
                    group by o.order_id"""

        cursor.execute(query, (store_name,))

        for row in cursor:
            results.append(Order(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllEdges(k, idMap):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT o1.order_id as ord1, o2.order_id as ord2, (COUNT(DISTINCT ot1.item_id) + COUNT(DISTINCT ot2.item_id)) / DATEDIFF(o2.order_date, o1.order_date) as peso
                    FROM orders o1, orders o2, order_items ot1, order_items ot2
                    where o1.order_id = ot1.order_id 
                    and  o2.order_id = ot2.order_id 
                    and o1.store_id = o2.store_id 
                    and o1.order_date < o2.order_date
                    and DATEDIFF(o2.order_date, o1.order_date) <=%s
                    group by o1.order_id , o2.order_id"""

        cursor.execute(query, (k,))

        for row in cursor:
            if row["ord1"] in idMap and row["ord2"] in idMap:
                c1 = idMap[row["ord1"]]
                c2 = idMap[row["ord2"]]
                peso = float(row["peso"])
                results.append((c1, c2, peso))

        cursor.close()
        conn.close()
        return results