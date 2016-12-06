import csv
import os.path as path


class CsvCleaner(object):
    """Cleans misformatted csv files and rewrites them"""

    @staticmethod
    def clean_cc(source, target):
        """
            Cleans the misformatted CC csv file at the given source location and
            writes it to the target location. Note, that the target location will be
            overwritten, in case it already exists.

            Parameters
            ----------
            source: str
                    The path to the source file which should be cleaned up
            target: str
                    The path to the file in which the cleaned CC values are written to
        """

        if not path.isfile(source):
            raise "The given source path %s does not exits" % source

        # note, that the target file is cleared if already existing
        reader = csv.reader(open(source, "rb"))
        writer = csv.writer(open(target, "wb"))

        for row in reader:
            length_row = len(row)
            str = row[1]

            # each row should have exactly 4 fields, otherwise we
            # assume, the "what" field has multiple addresses in it
            if length_row > 4:
                for x in xrange(2, 2 + length_row - 4):
                    str = str + ',' + row[x].strip()

                row[1] = str
                row[2] = row[2 + length_row - 4]
                row[3] = row[3 + length_row - 4]

                del row[4 - length_row]

            # write (cleaned) row
            writer.writerow(row)
