import web
import tempfile
import json
import os
import subprocess
import stat
import re

urls = (
    '/', 'index',
    '/R', 'verify'
)

class index:
    def GET(self):
        f = open("templates/index.html")
        html = f.read()
        f.close()
        return html

class verify:
    def POST(self):
        # First, get the POSTed input from the request
        i = web.input()

        # Setup a working directory to place the solution in
        working_dir = tempfile.mkdtemp(dir="/tmp/R-verifier")
        os.chmod(working_dir, 01755)
        # Also setup a subdirectory for tests
        os.mkdir(working_dir + "/tests")

        # Create the solution file
        source_code = i.source_code
        working_source = open(working_dir + "/solution.R", "w")
        working_source.write(source_code)
        working_source.close()

        # Create the RUnit test file from the template
        tests = i.tests
        runit_template = open("templates/1.R")
        runit_tests = open(working_dir + "/tests/1.R", "w")
        try:
            for line in runit_template:
                if line != "##TESTS##\n":
                    runit_tests.write(line)
                else:
                    runit_tests.write(tests)
        finally:
            runit_tests.close()

        # Create the test suite file from the template
        test_suite_template = open("templates/run_tests.R")
        test_suite = test_suite_template.read()
        test_suite_template.close()
        test_suite_file = open(working_dir + "/run_tests.R", "w")
        test_suite_file.write(test_suite)
        test_suite_file.close()

        # Run the code
        # Get the error code and output.
	r_error_code = self.run(working_dir)
        if r_error_code == 0:
            r_outfile = open(working_dir + "/output.txt")
            r_output = r_outfile.read()
            r_outfile.close()
        else:
            r_output = r_error_code

        if isinstance(r_output, int) and r_output == 137:
            solved = False
            verification_message - "Your solution did not complete in time.  Is there an infinite loop?"
            printed = ""
            error = r_output
        elif isinstance(r_output, int) and r_output == 1:
            solved = False
            verification_message - "Your solution did not parse correctly.  Is there a syntax error?"
            printed = ""
            error = r_output
        elif isinstance(r_output, int):
            solved = False
            verification_message - "Your solution did not run properly.  It returned an error code " + str(r_output) + "."
            printed = ""
            error = r_output
        elif re.search('^Number of failures: 0 $', r_output, flags=re.M):
            solved = True
            verification_message = "Your solution passes all tests."
            printed = r_output
            error = None
        else:
            solved = False
            verification_message = "Your solution does not pass all the provided tests."
            printed = ""
            error = r_output

        out = {
            'solved': solved,
            'verification_message': verification_message,
            'printed': printed,
            'error': error
        }
        web.header('Content-Type', 'application/json')
	return json.dumps(out)

    def run(self, working_dir):
        r_home = "/usr/lib/R"
        env = {
            "R_HOME": r_home, 
            "R_SHARE_DIR": r_home + "/share", 
            "R_INCLUDE_DIR": r_home + "/include",
            "LD_LIBRARY_PATH": "/usr/lib:" + r_home + "/lib"
        }
        try:
            error_code = subprocess.check_call('/usr/bin/timeout 3 ' + r_home + '/bin/exec/R --slave --vanilla -f run_tests.R > output.txt 2> errors.txt', 
                                             cwd=working_dir,
                                             shell=True,
                                             env=env)
        except subprocess.CalledProcessError as e:
            error_code = re.sub('Command .* returned', 'Command returned', str(e))
        return error_code
       

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
