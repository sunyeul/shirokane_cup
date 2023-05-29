from datetime import datetime


def format_time_ago(datetime_series):
    def time_ago(t):
        time = datetime.strptime(t, "%Y-%m-%d %H:%M:%S.%f")
        delta = datetime.now() - time
        if delta.days > 365:
            return f"{delta.days // 365} years ago"
        elif delta.days > 30:
            return f"{delta.days // 30} months ago"
        elif delta.days > 0:
            return f"{delta.days} days ago"
        elif delta.seconds > 3600:
            return f"{delta.seconds // 3600} hours ago"
        elif delta.seconds > 60:
            return f"{delta.seconds // 60} minutes ago"
        else:
            return "just now"

    return datetime_series.apply(time_ago)
