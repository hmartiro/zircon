"""

"""

import csv
import argparse


class DataExporter():

    def __init__(self, datastore=None):

        if not datastore:
            from zircon.datastores.influx import InfluxDatastore
            datastore = InfluxDatastore()

        self.db = datastore

    def export_csv(self, signals, t0, t1, dt, aggregate='first', limit=0):

        for signal in signals:

            result = self.db.get_timeseries(
                [signal],
                t0,
                t1,
                dt,
                aggregate,
                limit
            )

            if signal not in result:
                print('Zero points found for signal {}, skipping.'.format(
                    signal
                ))
                return

            timeseries = result[signal]
            print('Exporting {} points for signal {}.'.format(
                len(timeseries),
                signal
            ))

            with open('{}.csv'.format(signal), 'w') as f:

                writer = csv.writer(f, delimiter=' ')
                writer.writerow(['Timestamp', 'Value'])

                for point in timeseries:
                    writer.writerow(point)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='Export signal data from the database.')
    parser.add_argument('--t0', type=int, help='start time (us)',
                        default=0)
    parser.add_argument('--t1', type=int, help='end time (us)',
                        default=2000000000000000)
    parser.add_argument('-d', '--dt', type=int,
                        help='sample rate (us)', default=1)
    parser.add_argument('-a', '--aggregate', type=str,
                        help='aggregate function', default='first')
    parser.add_argument('-l', '--limit', type=int,
                        help='max number of points per signal', default=0)
    parser.add_argument('signals', type=str, nargs='+',
                        help='signal IDs to export')

    args = parser.parse_args()
    print(args)

    de = DataExporter()

    de.export_csv(
        args.signals,
        t0=args.t0,
        t1=args.t1,
        dt=args.dt,
        aggregate=args.aggregate,
        limit=args.limit
    )
