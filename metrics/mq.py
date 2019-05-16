from prometheus_client import Metric
import pymqi


class Exporter(object):

    def __init__(self, queue_manager, channel, connection, user, password,targets: []):
        self.queue_manager = queue_manager
        self.channel = channel
        self.connection = connection
        self.user = user
        self.password = password
        self.targets = targets

    def collect(self):
        # Get the data
        qmgr = pymqi.connect(self.queue_manager, self.channel, self.connection, self.user, self.password)

        # Current Queue Depth
        metric_queue_depth = Metric('mq_current_queue_depth', 'Current Queue Depth', 'gauge')

        # Open input count
        metric_open_input_count = Metric('mq_open_input_count', 'Open Input Count', 'gauge')

        # Open output count
        metric_open_output_count = Metric('mq_open_output_count', 'Open Output Count', 'gauge')

        for target in self.targets:
            queue = pymqi.Queue(qmgr, target)
            current_depth = queue.inquire(pymqi.CMQC.MQIA_CURRENT_Q_DEPTH)
            metric_queue_depth.add_sample(
                'mq_current_queue_depth',
                labels={'queue_name': target},
                value=int(current_depth)
            )

            open_input_count = queue.inquire(pymqi.CMQC.MQIA_OPEN_INPUT_COUNT)
            metric_open_input_count.add_sample(
                'mq_open_input_count',
                labels={'queue_name': target},
                value=int(open_input_count)
            )

            open_output_count = queue.inquire(pymqi.CMQC.MQIA_OPEN_OUTPUT_COUNT)
            metric_open_output_count.add_sample(
                'mq_open_output_count',
                labels={'queue_name': target},
                value=int(open_output_count)
            )

            queue.close()
        qmgr.disconnect()
        yield metric_queue_depth
        yield metric_open_input_count
        yield metric_open_output_count

