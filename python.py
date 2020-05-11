from collections import deque
from fireworks.core.rocket_launcher import rapidfire



from fireworks import *
from fireworks.core.rocket_launcher import rapidfire
from fireworks.flask_site.app import app
from fireworks.user_objects.queue_adapters.common_adapter import CommonAdapter
from fw_tutorials.dynamic_wf.printjob_task import PrintJobTask
from testEmail import Emailer
import json



# set up the LaunchPad and reset it
launchpad = LaunchPad()
launchpad.reset('', require_password=False)


# define five individual FireWorks used in the Workflow
task1 = ScriptTask.from_str('echo "Hello I am task one."')
task2 = ScriptTask.from_str('2/0')
task3 = ScriptTask.from_str('echo "Hello I am task three. I wait on task 1."')
task4 = ScriptTask.from_str('echo "Hello I am task four. I wait on task 3"')
task5 = ScriptTask.from_str('2/0')

fw1 = Firework(task1, fw_id=1, name='Task 1',  spec={"_pass_job_info":True})
fw2 = Firework(task2, name='Task2', spec={"_pass_job_info":True})
fw3 = Firework(task3, name ='Task3', spec={"_pass_job_info":True})
fw4 = Firework(task4, name='Task4', spec={"_pass_job_info":True})
fw5 = Firework(task5, fw_id=2, name='Task5', spec={"_pass_job_info": True, "_emailList": ''})

e = Emailer(filePath = "C:\\Users\\Cocka\\Downloads\\")
firework = Firework([e], name='emailer task1',parents=[fw5],fw_id=12, spec={"_allow_fizzled_parents":True})
firework2 = Firework([e], name='emailer task2',parents=[fw2], fw_id=10, spec={"_allow_fizzled_parents":True})




# assemble Workflow from FireWorks and their connections by id
# f2 and f3 wait on f1
# f4 waits on f2
#f4 waits on f3
workflow = Workflow([fw1, fw2, fw3, fw4, fw5, firework,firework2], {fw1: [fw2, fw3], fw2: [fw4], fw3: [fw4], fw4: [fw5]})

fw2 = Firework([PrintJobTask()], parents=[fw1], fw_id=2)
# store workflow and launch it locally
launchpad.add_wf(workflow)
# store workflow and launch it locally
# store workflow and launch it locally
rapidfire(launchpad, FWorker())

app.lp = launchpad  # change launchpad to the one you one to display - one Im using is defined at line 6
app.config["WEBGUI_USERNAME"] = "admin"
app.config["WEBGUI_PASSWORD"] = "admin"
app.run(debug=True)

