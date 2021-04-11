import csv
import xml.etree.ElementTree as ET
import json
import os
from datetime import datetime, timedelta
from datetime import date
from collections import namedtuple
from datetime import datetime, timezone
from pytz import timezone


class ModifyInputData():
    """The class that performs data input modification

    """

    def future_date(self, days: int):
        today = date.today()
        # print("Today's date is", today)
        new_date = str.join("", str(today + timedelta(days=days)).split('-'))
        # print(f'new date {days} days from today: {new_date}')
        return new_date

    ##
    #  1. a python script that updates xml test data file in-place
    ##
    def update_fields_xml(self, x: int, y: int, input_xml_file):
        """ this method to update given DEPART and RETURN fields with the new dates
            the result is saved into the same file <input_xml_file>

        :param x:
        :param y:
        :param input_xml_file:
        :return:
        """
        # update DEPART and RETURN fields

        new_depart_date = self.future_date(x)
        new_return_date = self.future_date(y)

        tree = ET.parse(xml_test_file)
        root = tree.getroot()
        try:
            with open(input_xml_file, "wb") as f:
                for element in tree.iter():
                    if element.tag == "DEPART":
                        print(f'Upding depart date {element.text} to {new_depart_date}')
                        element.text = str(new_depart_date)
                    if element.tag == "RETURN":
                        print(f'Upding return date {element.text} to {new_return_date}')
                        element.text = str(new_return_date)

                tree = ET.ElementTree(root)
                tree.write(xml_test_file)
                print(f'\nupdated xml request in file: {xml_test_file}\n')
        except Exception as e:
            print(f'Exception trying to write to a file {xml_test_file}, {e}')

    ##
    #  2. a python script that updates json test data and saves it into a new file
    ##
    def remove_element_json(self, el: str, input_json_file, modified_json_file):
        """ this method removes a field <el> from json file and saves the
            result in a new <modified_json_file>

        :param el:
        :param input_json_file:
        :param modified_json_file:
        :return:
        """
        self.fdict = {}

        with open(input_json_file) as f:
            self.fdict = json.load(f)

        for k, v in self.fdict.items():
            if k == el:
                removed = self.fdict.pop(k)
                print(f'removed top element {k} : {removed}')
                break
            elif isinstance(v, dict):
                # print(f'searching dict {k}:{v}')
                for key, value in v.items():
                    # print(f'element {key}: {value}')
                    if key == el:
                        # print(f'found element {el}')
                        removed = v.pop(key)
                        print(f'removed element [{key} : {removed}]')
                        break
        try:
            with open(modified_json_file, "w") as f:
                json.dump(self.fdict, f, indent=4)
        except Exception as e:
            print(f'Exception trying to write to a file {modified_json_file}, {e}')


##
#  3. Create a python script that parses jmeter log files
##
class AssertionResult(namedtuple('AssertionResult', (
        'label', 'responseCode', 'responseMessage', 'failureMessage', 'timeStamp'
))):
    """The class that stores the single assertion result.
    using namedtuple collection, which assigns names, as well as the numerical index, to each member
    It contains
    the following fields:

    label           -- label of the sample
    responseCode    -- response code
    responseMessage -- response message
    failureMessage  -- failure message
    timeStamp       -- time of non-200 response in human-readable format in PST timezone
                                                            (e.g. 2021-02-09 06:02:55 PST).
    """
    pass


class CSVParser():
    """The class that implements JTL (CSV) file parsing functionality.

    """

    def __init__(self, sourcef: str, resultf: str):
        """Initialize the class.

        Arguments:
        source -- name of the file containing the results data
        """
        self.source = sourcef
        self.outfile = resultf
        self.assertion_results = []

    def _get_assertion_results(self, row):
        """Get assertion results from the sample and return them as a list of
        AssertionResult class instances.
        # """
        if row.get('responseCode') != '200':
            fields = {}
            fields['label'] = row['label']
            fields['responseCode'] = row['responseCode']
            fields['responseMessage'] = row['responseMessage']
            fields['failureMessage'] = row['failureMessage']
            ts = int(row['timeStamp'])
            date_format = '%m/%d/%Y %H:%M:%S %Z'
            dt_obj = datetime.fromtimestamp(ts / 1000, timezone('US/Pacific'))
            # print('date & time is:', dt_obj.strftime(date_format))
            fields['timeStamp'] = dt_obj.strftime(date_format)
            self.assertion_results.append(AssertionResult(**fields))
            return fields

    def namedtuple_to_str(self, t, field_widths=15):
        if isinstance(field_widths, int):
            field_widths = [field_widths] * len(t)
        field_pairs = ['{}={}'.format(field, getattr(t, field)) for field in t._fields]
        s = ' '.join('{{:{}}}'.format(w).format(f) for w, f in zip(field_widths, field_pairs))
        result = '{}( {} )'.format(type(t).__name__, s)
        return result

    def iterfile(self):
        """method which finds failed tests in jtl file
           and saves them in list self.assertion_results

        """
        with open(self.source, 'r') as sf:
            reader = csv.DictReader(sf)
            for row in reader:
                assertion = self._get_assertion_results(row)
                if assertion:
                    print(assertion)

        with open(self.outfile, 'w') as rf:
            for each in self.assertion_results:
                rf.write(self.namedtuple_to_str(each, field_widths=[40, 20, 35, 20, 15]) + "\n")
                # print(self.namedtuple_to_str(each, field_widths=[40, 20, 35, 20, 15]))


if __name__ == "__main__":
    # test_root is the parent directory of the directory where program resides.
    test_root = os.path.join(os.path.dirname(__file__))
    print(test_root)
    xml_test_file = os.path.join(test_root, '../test_data/test_payload1.xml')
    # modified_xml_test_file = os.path.join(test_root, '../test_data/modified_test_payload.xml')
    json_test_file = os.path.join(test_root, '../test_data/test_payload.json')
    modified_json_test_file = os.path.join(test_root, '../test_data/modified_test_payload.json')
    """
    1. Create a python method that takes arguments int X and int Y,
    and updates DEPART and RETURN fields in test_payload1.xml
    """
    # print('\n1. Update xml request "test_payload1.xml" \n')
    modifier = ModifyInputData()
    modifier.update_fields_xml(5, 15, xml_test_file)

    """
    2. Create a python method that takes a json element
    as an argument, and removes that element from test_payload.json (e.g. "statecode" element ).
    """
    print('\n2. Update json request "test_payload.json" \n')
    modifier.remove_element_json("statecode", json_test_file, modified_json_test_file)
    # modifier.remove_element_json("inParams", json_test_file, modified_json_test_file)

    """
    3. Create a python script that parses jmeter log files
    """
    print('\n3. Parsing Jmeter_log1.jtl\n')
    myparser = CSVParser("../test_data/Jmeter_log1.jtl", "../test_output_data/Jmeter_log1_assertions.txt")
    myparser.iterfile()

    print('\nParsing Jmeter_log2.jtl\n')
    myparser = CSVParser("../test_data/Jmeter_log2.jtl", "../test_output_data/Jmeter_log2_assertions.txt")
    myparser.iterfile()
