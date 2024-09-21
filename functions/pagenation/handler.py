import json
import os
import psycopg2
import sys
from psycopg2.extras import RealDictCursor

# データベース接続情報
DB_HOST = os.environ['DB_HOST']
DB_USER = os.environ['DB_USER']
DB_PASSWORD = os.environ['DB_PASSWORD']
DB_NAME = os.environ['DB_NAME']
DB_PORT = os.environ['DB_PORT']

def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        dbname=DB_NAME,
        port=DB_PORT
    )

def fetch_all_records_with_pagination(page_size=10):
    connection = get_db_connection()
    try:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            # 総レコード数を取得
            cursor.execute("SELECT COUNT(*) as total FROM users")
            total_records = cursor.fetchone()['total']
            print(f'Total records: {total_records}')
            print(f'Page size: {sys.getsizeof(page_size)}')

            # ページ数を計算
            total_pages = (total_records + page_size - 1) // page_size

            total_data_size = 0
            all_results = []
            for page in range(1, total_pages + 1):
                offset = (page - 1) * page_size
                sql = "SELECT * FROM users ORDER BY id OFFSET %s LIMIT %s"
                cursor.execute(sql, (offset, page_size))
                results = cursor.fetchall()
                all_results.extend(results)
                print(f'Fetched page {page} of {total_pages}')
                print(f'Records size: {sys.getsizeof(results)}')
                total_data_size += sys.getsizeof(results)

            print(f'Total records fetched: {len(all_results)}')
            print(f'Total data size: {total_data_size}')
            return all_results
    finally:
        connection.close()



# def lambda_handler(event, context):



def __main__():
    page = 1
    page_size = 10
    offset = (page - 1) * page_size

    records = fetch_all_records_with_pagination(page_size)

        # # レスポンスの作成
        # response = {
        #     'statusCode': 200,
        #     'body': json.dumps({
        #         'data': results,
        #         'page': page,
        #     }, default=str)  # datetime objects のシリアライズ対応
        # }

    # return response

if __name__ == '__main__':
    __main__()
