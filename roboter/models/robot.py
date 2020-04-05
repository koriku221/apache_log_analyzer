import apache_log_parser
import pandas as pd
import datetime as dt
from glob import glob

from roboter.views import console

DEFAULT_ROBOT_NAME = 'Robot'
DEFAULT_LOG_PATH = r'C:\Apache24\logs\access*.log'
DEFAULT_LOG_FORMAT = "%h %l %u %t \"%r\" %>s %b"
RANKING_CSV_FILE_PATH = 'ranking.csv'
VISITS_PER_HOUR_PATH = 'visit_per_hour.csv'
LOG_CSV_FILE_PATH = 'logs.csv'


class Robot(object):
    def __init__(self, name=DEFAULT_ROBOT_NAME):
        self.name = name


class AnalyzerRobot(Robot):

    def __init__(self, name=DEFAULT_ROBOT_NAME, log_path=DEFAULT_LOG_PATH,
                 log_format=DEFAULT_LOG_FORMAT):
        super().__init__(name=name)

        self.parser = apache_log_parser.make_parser(log_format)
        self.log_path = log_path
        self.is_selection_start_time = None
        self.is_selection_end_time = None

        log_list = []
        for pl in glob(DEFAULT_LOG_PATH):
            with open(pl, 'r') as f:
                for s_line in f:
                    log_line_data = self.parser(s_line)
                    log_list.append(log_line_data)

        self.df = pd.DataFrame(log_list)
        self.df['time_received_isoformat'] = pd.to_datetime(self.df['time_received_isoformat'],
                                                            format='%Y-%m-%dT%H:%M:%S')

        self.df.to_csv(LOG_CSV_FILE_PATH)

    def _period_decorator(func):
        def wrapper(self):
            if self.is_selection_start_time and self.is_selection_end_time:
                self.df = self.df[(self.df['time_received_isoformat']
                                   >= dt.datetime.strptime(self.is_selection_start_time, '%Y/%m/%d'))
                                  & (self.df['time_received_isoformat']
                                     < (dt.datetime.strptime(self.is_selection_end_time, '%Y/%m/%d')
                                        + dt.timedelta(days=1)))]
            return func(self)

        return wrapper

    def ask_selection(self):
        template = console.get_template('select1.txt')
        is_selection1 = input(template.substitute({'robot_name': self.name}))

        if is_selection1 == '1':
            template = console.get_template('select2.txt')
            is_selection2 = input(template.substitute({'robot_name': self.name}))
            if is_selection2 == '1':
                self.get_visits_per_time()
            elif is_selection2 == '2':
                self.get_host_ranking()

            else:
                print("1か2を選択してください")
                exit()

        elif is_selection1 == '2':
            template = console.get_template('select_start_time.txt')
            self.is_selection_start_time = input(template.substitute({'robot_name': self.name}))
            template = console.get_template('select_end_time.txt')
            self.is_selection_end_time = input(template.substitute({'robot_name': self.name}))
            template = console.get_template('select2.txt')
            is_selection2 = input(template.substitute({'robot_name': self.name}))
            if is_selection2 == '1':
                self.get_visits_per_time()
            elif is_selection2 == '2':
                self.get_host_ranking()

            else:
                print("1か2を選択してください")
                exit()
            if not (self.is_selection_start_time or self.is_selection_end_time):
                print("フォーマット通りに入力してください")
                exit()
        else:
            print("1か2を選択してください")
            exit()

    @_period_decorator
    def get_host_ranking(self, path=RANKING_CSV_FILE_PATH):
        vc = self.df['remote_host'].value_counts()
        vc.to_csv(path)

    @_period_decorator
    def get_visits_per_time(self, path=VISITS_PER_HOUR_PATH):
        self.df['time_received_isoformat'] = self.df['time_received_isoformat'].dt.floor("H")
        vc = self.df['time_received_isoformat'].value_counts(sort=False)
        vc.to_csv(path)

    def end(self):
        template = console.get_template(('good_by.txt'))
        print(template.substitute({'robot_name': self.name}))
