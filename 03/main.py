"""
--- Day 3: No Matter How You Slice It ---
The Elves managed to locate the chimney-squeeze prototype fabric for Santa's suit (thanks to someone who helpfully wrote its box IDs on the wall of the warehouse in the middle of the night). Unfortunately, anomalies are still affecting them - nobody can even agree on how to cut the fabric.

The whole piece of fabric they're working on is a very large square - at least 1000 inches on each side.

Each Elf has made a claim about which area of fabric would be ideal for Santa's suit. All claims have an ID and consist of a single rectangle with edges parallel to the edges of the fabric. Each claim's rectangle is defined as follows:

The number of inches between the left edge of the fabric and the left edge of the rectangle.
The number of inches between the top edge of the fabric and the top edge of the rectangle.
The width of the rectangle in inches.
The height of the rectangle in inches.
A claim like #123 @ 3,2: 5x4 means that claim ID 123 specifies a rectangle 3 inches from the left edge, 2 inches from the top edge, 5 inches wide, and 4 inches tall. Visually, it claims the square inches of fabric represented by # (and ignores the square inches of fabric represented by .) in the diagram below:

...........
...........
...#####...
...#####...
...#####...
...#####...
...........
...........
...........
The problem is that many of the claims overlap, causing two or more claims to cover part of the same areas. For example, consider the following claims:

#1 @ 1,3: 4x4
#2 @ 3,1: 4x4
#3 @ 5,5: 2x2
Visually, these claim the following areas:

........
...2222.
...2222.
.11XX22.
.11XX22.
.111133.
.111133.
........
The four square inches marked with X are claimed by both 1 and 2. (Claim 3, while adjacent to the others, does not overlap either of them.)

If the Elves all proceed with their own plans, none of them will have enough fabric. How many square inches of fabric are within two or more claims?
"""

with open('input.txt') as f:
    content = f.readlines()

def part1():
    visited = {} # save the id of the claim as the value
    overlapping = set()
    did_not_overlap = set()

    def parse_line(line):
        _, _, edges, dimensions = line.split(' ')
        edges = edges[:len(edges)-1]
        edges = edges.split(',')
        edges = [int(edge) for edge in edges]
        dimensions = dimensions.split('x')
        dimensions = [int(dimension) for dimension in dimensions]
        return (edges, dimensions)

    def get_id(line):
        id = line.split(' ')
        return int(id[0][1:])

    def process_overlapping(id, edges, dimensions):
        start_point = (edges[0], edges[1])
        overlapped = False

        for y in range(start_point[1], start_point[1] + dimensions[1]):
            for x in range(start_point[0], start_point[0] + dimensions[0]):
                point = (x, y)
                if point in visited:
                    overlapping.add(point)
                    overlapped = True
                    if visited[point] in did_not_overlap:
                        did_not_overlap.remove(visited[point])
                else:
                    visited[point] = id

        if not overlapped:
            did_not_overlap.add(id)

    for line in content:
        edges, dimensions = parse_line(line)
        process_overlapping(get_id(line), edges, dimensions)

    return (len(overlapping), did_not_overlap)

overlapping = part1()
print(overlapping)

"""
--- Part Two ---
Amidst the chaos, you notice that exactly one claim doesn't overlap by even a single square inch of fabric with any other claim. If you can somehow draw attention to it, maybe the Elves will be able to make Santa's suit after all!

For example, in the claims above, only claim 3 is intact after all claims are made.

What is the ID of the only claim that doesn't overlap?
"""
