# import pandas as pd
# import apache_log_parser
#
# DEFAULT_ROBOT_NAME = 'Robot'
# DEFAULT_LOG_PATH = r'C:\Apache24\logs\access.log'
# DEFAULT_LOG_FORMAT = "%h %l %u %t \"%r\" %>s %b"
# log_list = []
#
# with open(DEFAULT_LOG_PATH, 'r') as f:
#     read_count = 0
#     parser = apache_log_parser.make_parser(DEFAULT_LOG_FORMAT)
#
#     for s_line in f:
#         log_line_data = parser(s_line)
#         log_list.append(log_line_data)
#         read_count += 1
#
# df = pd.DataFrame(log_list)
# #df = pd.io.json.json_normalize()
#
# vc = df['remote_host'].value_counts()
# print(vc)
# print(type(vc))
# print(type(df))
# self.df['time_received_isoformat'] = pd.to_datetime(self.df['time_received_isoformat'],
#                                                     format='%Y-%m-%dT%H:%M:%S')
#
# from datetime import datetime, timedelta
#
#         start = datetime.strptime(time, '%Y/%m/%d')
#         end = start + timedelta(days=1) - timedelta(hours=1)
#         visits_df = pd.DataFrame()
#
#         def date_range(start_date, end_date):
#             for n in range((end_date - start_date).hours):
#                 yield start_date + timedelta(n)
#
#         for i in date_range(start, end):
#             visits_df += self.df[(self.df['time_received_isoformat'] >= start) &
#                                  (self.df['time_received_isoformat'] < start + timedelta(hours=1))]
#
#         visits_df.to_csv(path)