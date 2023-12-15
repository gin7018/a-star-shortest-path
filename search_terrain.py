import math
import queue
import sys

from PIL import Image, ImageDraw
from Types import Pixel, get_terrain_from_color


MAP_WIDTH = 395
MAP_HEIGHT = 500


def load_terrain_map(terrain_img, elevation_file):
    img = Image.open(terrain_img)

    terrain = []
    elvs = []

    with open(elevation_file) as elv:
        while True:
            elevations = [float(x) for x in next(elv, "").split()[:MAP_WIDTH]]
            if not elevations:
                break

            elvs.append(elevations)

    for y in range(0, MAP_HEIGHT):
        row = []
        for x in range(0, MAP_WIDTH):
            rgb = img.getpixel((x, y))
            px = Pixel((y, x), elvs[y][x], get_terrain_from_color(rgb))
            row.append(px)
        terrain.append(row)

    return terrain


def load_targets(terrain, path_file):
    targets = []

    with open(path_file) as f:
        for line in f:
            x, y = line.strip().split()
            px = terrain[int(y)][int(x)]
            targets.append(px)

    return targets


def find_optimal_path(terrain, start, end):
    pq = queue.PriorityQueue()
    path_to = {}
    g_score_of = {}
    f_score_of = {}
    visited = set()

    path_to[start] = start
    g_score_of[start] = 0
    f_score_of[start] = start.get_pixel_heuristic(target_pixel=start)

    pq.put((f_score_of[start], start))

    while pq.qsize() > 0:

        current_px = pq.get()[1]
        visited.add(current_px)
        # print("going to: ", current_px)

        if current_px.coordinates == end.coordinates:
            # we've reached one of the targets
            # construct the partial path now
            return construct_path(path_to, start, end)

        # get all the 4 neighbors
        nb = current_px.get_pixel_neighbors(terrain)
        for neighbor in nb:

            # update the g score: how far this neighbor pixel is to its parent (z axis included)
            x_diff_sq = ((current_px.coordinates[1] - neighbor.coordinates[1]) * Pixel.LONGITUDE) ** 2
            y_diff_sq = ((current_px.coordinates[0] - neighbor.coordinates[0]) * Pixel.LATITUDE) ** 2
            z_diff_sq = (current_px.elevation - neighbor.elevation) ** 2

            distance_to_neighbor = math.sqrt(x_diff_sq + y_diff_sq + z_diff_sq)

            g_score_of[neighbor] = g_score_of[current_px] + distance_to_neighbor

            # calculate f score
            potential_f_score = g_score_of[neighbor] + neighbor.get_pixel_heuristic(target_pixel=end)

            if f_score_of.get(neighbor) is None or f_score_of[neighbor] > potential_f_score:

                f_score_of[neighbor] = potential_f_score
                path_to[neighbor] = current_px

                if neighbor not in visited:
                    pq.put((f_score_of[neighbor], neighbor))

    return None


def find_path_to_all_targets(terrain, targets):
    total_path = []

    for i in range(1, len(targets)):
        total_path += find_optimal_path(terrain, targets[i - 1], targets[i])

    return total_path


def construct_path(path_to, start, end):
    path = []

    current = end
    path.insert(0, current)

    while current is not start:
        current = path_to[current]
        path.insert(0, current)

    return path


def draw_path_on_terrain(path, terrain_img, output):
    image = Image.open(terrain_img)
    draw = ImageDraw.Draw(image)

    path_color = (200, 100, 230, 255)
    total_path_distance = 0.0

    for i in range(0, len(path)):
        px = path[i]
        y, x = px.coordinates
        draw.point((x, y), fill=path_color)

        # add this point to the total distance
        if i > 0:
            prev_px = path[i-1]

            x_diff_sq = ((x - prev_px.coordinates[1]) * Pixel.LONGITUDE) ** 2
            y_diff_sq = ((y - prev_px.coordinates[0]) * Pixel.LATITUDE) ** 2
            z_diff_sq = (px.elevation - prev_px.elevation) ** 2
            total_path_distance += math.sqrt(x_diff_sq + y_diff_sq + z_diff_sq)

    print("Total Distance: ", total_path_distance, " m")

    image.save(output)
    # image.show()


def main():
    if len(sys.argv) != 5:
        print("not enough arguments")
        return

    terrain_img = sys.argv[1]
    elevation_file = sys.argv[2]
    path_file = sys.argv[3]
    output_img_file = sys.argv[4]

    terrain = load_terrain_map(terrain_img, elevation_file)
    targets = load_targets(terrain, path_file)

    path = find_path_to_all_targets(terrain, targets)
    if path is None:
        print("no solution")
    else:
        draw_path_on_terrain(path, terrain_img, output_img_file)


if __name__ == '__main__':
    main()
