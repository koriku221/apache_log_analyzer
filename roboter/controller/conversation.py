from roboter.models import robot


def talk_about_apache_log():
    analyzer = robot.AnalyzerRobot()
    analyzer.ask_selection()
    analyzer.end()
