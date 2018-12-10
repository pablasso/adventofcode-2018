"""
--- Day 7: The Sum of Its Parts ---
You find yourself standing on a snow-covered coastline; apparently, you landed a little off course. The region is too hilly to see the North Pole from here, but you do spot some Elves that seem to be trying to unpack something that washed ashore. It's quite cold out, so you decide to risk creating a paradox by asking them for directions.

"Oh, are you the search party?" Somehow, you can understand whatever Elves from the year 1018 speak; you assume it's Ancient Nordic Elvish. Could the device on your wrist also be a translator? "Those clothes don't look very warm; take this." They hand you a heavy coat.

"We do need to find our way back to the North Pole, but we have higher priorities at the moment. You see, believe it or not, this box contains something that will solve all of Santa's transportation problems - at least, that's what it looks like from the pictures in the instructions." It doesn't seem like they can read whatever language it's in, but you can: "Sleigh kit. Some assembly required."

"'Sleigh'? What a wonderful name! You must help us assemble this 'sleigh' at once!" They start excitedly pulling more parts out of the box.

The instructions specify a series of steps and requirements about which steps must be finished before others can begin (your puzzle input). Each step is designated by a single letter. For example, suppose you have the following instructions:

Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin.
Visually, these requirements look like this:


  -->A--->B--
 /    \      \
C      -->D----->E
 \           /
  ---->F-----
Your first goal is to determine the order in which the steps should be completed. If more than one step is ready, choose the step which is first alphabetically. In this example, the steps would be completed as follows:

Only C is available, and so it is done first.
Next, both A and F are available. A is first alphabetically, so it is done next.
Then, even though F was available earlier, steps B and D are now also available, and B is the first alphabetically of the three.
After that, only D and F are available. E is not available because only some of its prerequisites are complete. Therefore, D is completed next.
F is the only choice, so it is done next.
Finally, E is completed.
So, in this example, the correct order is CABDFE.

In what order should the steps in your instructions be completed?
"""

with open('input.txt') as f:
    content = f.readlines()

def parse(line):
    parts = line.split(' ')
    node_id = parts[7]
    dependency_id = parts[1]
    return (node_id, dependency_id)

WORKERS = 5
LETTERS = {
    'A':1, 'B':2, 'C':3, 'D':4, 'E':5, 'F':6, 'G':7, 'H':8, 'I':9, 'J':10, 'K':11, 'L':12, 'M':13, 'N':14, 'O':15,
    'P':16, 'Q':17, 'R':18, 'S':19, 'T':20, 'U':21, 'V':22, 'W':23, 'X':24, 'Y':25, 'Z':26
}
STEP_DURATION = 60
availables = []
nodes = {}

class Node():
    def __init__(self, id):
        self.id = id
        self.progress = 0
        self.depends_on = []
        self.depended_by = []

    def __repr__(self):
        return f'<Node> id:{self.id} progress:{self.progress}'

    @property
    def execution_time(self):
        return LETTERS[self.id] + STEP_DURATION

    @staticmethod
    def add_to_availables(node):
        if not node.depends_on and node not in availables:
            availables.append(node)

    @classmethod
    def get_or_create_node(cls, node_id):
        if node_id in nodes:
            return nodes[node_id]
        node = cls(node_id)
        nodes[node_id] = node
        return node

    def remove_availability(self):
        try:
            availables.remove(self)
        except:
            pass

    def add_dependency(self, dependency_id):
        dependency = self.get_or_create_node(dependency_id)
        self.depends_on.append(dependency)
        dependency.depended_by.append(self)
        self.remove_availability()
        self.add_to_availables(dependency)

    def execute(self):
        for node in self.depended_by:
            try:
                node.depends_on.remove(self)
            except:
                pass
            self.add_to_availables(node)

        self.remove_availability()

def single_thread():
    for line in content:
        node_id, dependency_id = parse(line)
        node = Node.get_or_create_node(node_id)
        node.add_dependency(dependency_id)

    order = ''
    while availables:
        availables.sort(key=lambda node: node.id)
        node = availables[0]
        node.execute()
        order += str(node.id)

    return order

# order = single_thread()
# print('single thread order:', order)

"""
--- Part Two ---
As you're about to begin construction, four of the Elves offer to help. "The sun will set soon; it'll go faster if we work together." Now, you need to account for multiple people working on steps simultaneously. If multiple steps are available, workers should still begin them in alphabetical order.

Each step takes 60 seconds plus an amount corresponding to its letter: A=1, B=2, C=3, and so on. So, step A takes 60+1=61 seconds, while step Z takes 60+26=86 seconds. No time is required between steps.

To simplify things for the example, however, suppose you only have help from one Elf (a total of two workers) and that each step takes 60 fewer seconds (so that step A takes 1 second and step Z takes 26 seconds). Then, using the same instructions as above, this is how each second would be spent:

Second   Worker 1   Worker 2   Done
   0        C          .        
   1        C          .        
   2        C          .        
   3        A          F       C
   4        B          F       CA
   5        B          F       CA
   6        D          F       CAB
   7        D          F       CAB
   8        D          F       CAB
   9        D          .       CABF
  10        E          .       CABFD
  11        E          .       CABFD
  12        E          .       CABFD
  13        E          .       CABFD
  14        E          .       CABFD
  15        .          .       CABFDE
Each row represents one second of time. The Second column identifies how many seconds have passed as of the beginning of that second. Each worker column shows the step that worker is currently doing (or . if they are idle). The Done column shows completed steps.

Note that the order of the steps has changed; this is because steps now take time to finish and multiple workers can begin multiple steps simultaneously.

In this example, it would take 15 seconds for two workers to complete these steps.

With 5 workers and the 60+ second step durations described above, how long will it take to complete all of the steps?
"""

def multi_thread():
    for line in content:
        node_id, dependency_id = parse(line)
        node = Node.get_or_create_node(node_id)
        node.add_dependency(dependency_id)

    availables.sort(key=lambda node: node.id)
    order = ''
    ticks = 0
    in_progress = []

    def execute_tick(nodes):
        nonlocal ticks
        finished = []
        for node in nodes:
            node.progress += 1
            if node.progress == node.execution_time:
                finished.append(node)
        ticks += 1
        return finished

    def clear_finished(finished):
        nonlocal order
        for node in finished:
            node.execute()
            order += str(node.id)
            in_progress.remove(node)
        availables.sort(key=lambda node: node.id)

    while availables or in_progress:
        if availables and len(in_progress) < WORKERS:
            nodes = availables[:WORKERS - len(in_progress)]
            for node in nodes:
                in_progress.append(node)
                availables.remove(node)
        finished = execute_tick(in_progress)
        clear_finished(finished)

    return (order, ticks)

order, ticks = multi_thread()
print("multi_thread:", order, ticks)
