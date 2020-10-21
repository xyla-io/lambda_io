from data_layer import get_connection, run_query, Query, UnloadQuery
from datetime import datetime, timedelta

end_date = str((datetime.now() - timedelta(days=2)).date())
start_date = str((datetime.now() - timedelta(days=30)).date())

def run():
  connection = get_connection(
    database='DATABASE',
    host='HOST',
    port=5439,
    user='USER',
    password='PASSWORD',
  )
  # connection.autocommit = True
  configs = []
  
  query_text = '''
select *
from {schema}.fetch_apple_search_ads_campaigns
where app_display_name=%s
and date between %s and %s
'''
  
  configs = [
    {
      'query': Query(
        query=query_text.format(schema= 'demo'),
        parameters=['Goalie', start_date, end_date]
      ),
      's3_key': 'lambda_io.csv',
    },
  ]
  
  
  results = []
  for config in configs:

    unload_query = UnloadQuery(
      select_query=config['query'],
      access_key_id='ACCESSKEYID',
      secret_access_key='SECRET',
      bucket='BUCKET',
      key=config['s3_key']
    )

    url = unload_query.unload(connection=connection)
    results.append(url)

  connection.commit()
  connection.close()
  return '\n'.join(results)