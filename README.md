# generali-test-04112021

1. Create a python method that takes arguments int X and int Y,
and updates DEPART and RETURN fields
in test_payload1.xml:

- DEPART gets set to X days in the future from the current date
(whatever the current date is at the moment of executing the code)
- RETURN gets set to Y days in the future from the current date

2. Create a python method that takes a json element
as an argument, and removes that element from test_payload.json (e.g. "statecode" element ).

3. Create a python script that parses jmeter log files,
and in the case if there are any non-successful endpoint responses recorded in the log,
prints out the label, response code, response message, failure message,
and the time of non-200 response in human-readable format in PST timezone
(e.g. 2021-02-09 06:02:55 PST).

Please use Jmeter_log1.jtl, Jmeter_log2.jtl as input files for testing out your script.

++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
You can use any python libraries that are best suited for working on these assignments.
Please return python3 code that can be executed.

To return your completed assignments, please create a public github repository, save your code there,
and share the link to the repo.

As an alternative, please save your python code as .txt files and attach to an email.

Please do NOT attach .py files to an email, because .py files (plain or compressed)
are not allowed as attachments by our email system.
