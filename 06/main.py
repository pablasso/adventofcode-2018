"""
--- Day 6: Chronal Coordinates ---
The device on your wrist beeps several times, and once again you feel like you're falling.

"Situation critical," the device announces. "Destination indeterminate. Chronal interference detected. Please specify new target coordinates."

The device then produces a list of coordinates (your puzzle input). Are they places it thinks are safe or dangerous? It recommends you check manual page 729. The Elves did not give you a manual.

If they're dangerous, maybe you can minimize the danger by finding the coordinate that gives the largest distance from the other points.

Using only the Manhattan distance, determine the area around each coordinate by counting the number of integer X,Y locations that are closest to that coordinate (and aren't tied in distance to any other coordinate).

Your goal is to find the size of the largest area that isn't infinite. For example, consider the following list of coordinates:

1, 1
1, 6
8, 3
3, 4
5, 5
8, 9
If we name these coordinates A through F, we can draw them on a grid, putting 0,0 at the top left:

..........
.A........
..........
........C.
...D......
.....E....
.B........
..........
..........
........F.
This view is partial - the actual grid extends infinitely in all directions. Using the Manhattan distance, each location's closest coordinate can be determined, shown here in lowercase:

aaaaa.cccc
aAaaa.cccc
aaaddecccc
aadddeccCc
..dDdeeccc
bb.deEeecc
bBb.eeee..
bbb.eeefff
bbb.eeffff
bbb.ffffFf
Locations shown as . are equally far from two or more coordinates, and so they don't count as being closest to any.

In this example, the areas of coordinates A, B, C, and F are infinite - while not shown here, their areas extend forever outside the visible grid. However, the areas of coordinates D and E are finite: D is closest to 9 locations, and E is closest to 17 (both including the coordinate's location itself). Therefore, in this example, the size of the largest area is 17.

What is the size of the largest area that isn't infinite?
"""

with open('input.txt') as f:
    content = f.readlines()

class Anchor:
    def __init__(self, coord):
        self.coord = coord
        self.points = set()
        self.infinite = False

    def __repr__(self):
        return f'<Anchor>: coord:{self.coord} total_area:{self.total_area} infinite:{self.infinite}'

    @property
    def total_area(self):
        return len(self.points)

    def get_distance(self, point):
        return abs(point[0] - self.coord[0]) + abs(point[1] - self.coord[1])

    def assign(self, point, start, end):
        self.points.add(point)
        if point[0] == start[0] or point[1] == start[1] or point[0] == end[0] or point[1] == end[1]:
            self.infinite = True

def run():
    anchors = []
    x_lowest = 99999999
    y_lowest = 99999999
    x_highest = 0
    y_highest = 0
    
    def get_coord(line):
        parts = line.split(', ')
        return (int(parts[0]), int(parts[1]))

    def set_bounds(anchor):
        nonlocal x_lowest, y_lowest, x_highest, y_highest
        if x_lowest > anchor.coord[0]:
            x_lowest = anchor.coord[0]
        if y_lowest > anchor.coord[1]:
            y_lowest = anchor.coord[1]
        if x_highest < anchor.coord[0]:
            x_highest = anchor.coord[0]
        if y_highest < anchor.coord[1]:
            y_highest = anchor.coord[1]

    def get_bounds():
        start = (x_lowest-1, y_lowest-1)
        end = (x_highest+1, y_highest+1)
        return (start, end)

    for line in content:
        anchor = Anchor(get_coord(line))
        set_bounds(anchor)
        anchors.append(anchor)

    start, end = get_bounds()
    limit = 0
    for y in range(start[1], end[1]+1):
        for x in range(start[0], end[0]+1):
            current = (x, y)
            min_distance = 9999999
            closests = []

            for anchor in anchors:
                distance = anchor.get_distance(current)
                if distance < min_distance:
                    min_distance = distance
                    closests = [anchor]
                elif distance == min_distance:
                    closests.append(anchor)

            if len(closests) == 1:
                closests[0].assign(current, start, end)

            limit += 1

    largest = None
    for anchor in anchors:
        if anchor.infinite:
            continue
        if not largest or largest.total_area < anchor.total_area:
            largest = anchor

    return largest

largest = run()
print('largest:', largest)

"""
--- Part Two ---
On the other hand, if the coordinates are safe, maybe the best you can do is try to find a region near as many coordinates as possible.

For example, suppose you want the sum of the Manhattan distance to all of the coordinates to be less than 32. For each location, add up the distances to all of the given coordinates; if the total of those distances is less than 32, that location is within the desired region. Using the same coordinates as above, the resulting region looks like this:

..........
.A........
..........
...###..C.
..#D###...
..###E#...
.B.###....
..........
..........
........F.
In particular, consider the highlighted location 4,3 located at the top middle of the region. Its calculation is as follows, where abs() is the absolute value function:

Distance to coordinate A: abs(4-1) + abs(3-1) =  5
Distance to coordinate B: abs(4-1) + abs(3-6) =  6
Distance to coordinate C: abs(4-8) + abs(3-3) =  4
Distance to coordinate D: abs(4-3) + abs(3-4) =  2
Distance to coordinate E: abs(4-5) + abs(3-5) =  3
Distance to coordinate F: abs(4-8) + abs(3-9) = 10
Total distance: 5 + 6 + 4 + 2 + 3 + 10 = 30
Because the total distance to all coordinates (30) is less than 32, the location is within the region.

This region, which also includes coordinates D and E, has a total size of 16.

Your actual region will need to be much larger than this example, though, instead including all locations with a total distance of less than 10000.

What is the size of the region containing all locations which have a total distance to all given coordinates of less than 10000?
"""
