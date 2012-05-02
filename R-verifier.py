import web
import tempfile
import json
import os
import subprocess
import stat

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
        working_dir = tempfile.mkdtemp(dir="/tmp/R-verifier")
        os.chmod(working_dir, 01755)
        working_source = open(working_dir + "/solution.R", "w")
        i = web.input()
        solution = i.solution
        working_source.write(solution)
        working_source.close()

	self.run(working_dir)

        out = {
            'output': "/R/work/" + os.path.basename(working_dir) + "/output.txt",
            'pdf': "/R/work/" + os.path.basename(working_dir) + "/Rplots.pdf"
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
        output = open(working_dir + "/output.txt", "w")
        p = subprocess.Popen(['/usr/bin/timeout', '5', r_home + '/bin/exec/R', '--quiet', '--vanilla', '-f', 'solution.R'], 
                             cwd=working_dir,
                             env=env,
                             stdout=output,
                             stderr=subprocess.STDOUT)
       

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
