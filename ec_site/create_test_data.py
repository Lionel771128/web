import psycopg2
import argparse

def create_test_data(db="test", user="123", password="123", host='127.0.0.1', port='5432'):
    table_list = ['user_userprofile', 'shop_brand', 'shop_gamecategory',
                  'shop_productcategory', 'shop_product']
    db_connect = psycopg2.connect(database=db,
                                  user=user, password=password,
                                  host=host,
                                  port=port)
                                  # host="/var/run/postgresql/", port="5432")

    for t in table_list:
        copy_data_from_csv(db_connect, t)
    db_connect.close()


def copy_data_from_csv(db_conn, table_name=None):
    assert db_conn is not None, 'table_name should not be Null'
    assert table_name is not None, 'table_name should not be Null'
    # get column name
    cursor = db_conn.cursor()
    cursor.execute(f"Select * FROM {table_name} LIMIT 0")
    column_names = [desc[0] for desc in cursor.description]
    print(table_name ,column_names)
    with open(f'./test_data/{table_name}.csv', 'r') as f:
        cursor.copy_from(f, table_name, sep=',', columns=column_names)
    db_conn.commit()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some argument.')
    parser.add_argument('--host', default='127.0.0.1', metavar='db host', type=str,
                        help='db host')
    args = parser.parse_args()
    create_test_data(host=args.host)



