"""Grasshopper Script"""

import rhinoscriptsyntax as rs
import math

# Calculating our golden ratio and angle
golden_ratio = (math.sqrt(5.0) + 1.0) / 2.0
golden_angle = (1.0 - 1.0 / golden_ratio) * (2 * math.pi)

# calculates the cartesian coordinates of a point in 3 dimensions given latitude / longitude
def calc_point_on_sphere(lon, lat):
    x = math.cos(lat) * math.cos(lon)
    y = math.sin(lat) * math.cos(lon)
    z = math.sin(lon)
    return rs.CreatePoint(x,y,z)


# calculating distances between a point and it's nearest neighbor
def check_distances(points):
    shortest_distances = []
    # nested for loop to check every point against each other
    for i in range(len(points)):
        # set the record value to some arbitrarily high value to start
        smallest_distance = 100000000.0
        # for every point in the list
        for j in range(len(points)):
            # if the point is not itself as that will return a distance of 0
            if(i != j):
                dist = rs.Distance(points[i], points[j])
                # replace smallest distance if current distance is less
                if(dist < smallest_distance):
                    smallest_distance = dist
        shortest_distances.append(smallest_distance)
    return shortest_distances

# a bit of an error check to show how the algorithm isn't a perfect distribution
def calc_min_max(distance_list):
    min_dist = min(distance_list)
    max_dist = max(distance_list)
    delta = max_dist - min_dist
    print("Distance between points")
    print(f"Min Distance : {min_dist}")
    print(f"Max Distance : {max_dist}")
    print(f"Delta : {delta}")

# Gets the normal vectors on the generated sphere
# list will be parallel to our points list input
def get_normal_vectors(sphere, points):
    normal_vectors = []
    for point in points:
        (U, V) = rs.SurfaceClosestPoint(sphere, point)
        normal_vector = rs.SurfaceNormal(sphere, [U, V])
        normal_vectors.append(normal_vector)
    return normal_vectors

# calculates evenly distributed points on a sphere
def calculate_points():
    point_list = []
    for i in range(int(num_pts)):
        # Calc evenly distributed latitude and longitude coordinates
        lon = math.asin(-1.0 + (2.0 * float(i) + 1.0) / float(num_pts))
        lat = golden_angle * float(i)

        # Convert to cartesian coordinates and create a new point
        new_point = calc_point_on_sphere(lon,lat)

        # scale the objects based on the radius of the sphere and the sphere's center
        scale_transformation = rs.XformScale(radius, center_point)
        rs.TransformObject(new_point, scale_transformation)

        point_list.append(new_point)
    return point_list


# calculate our evenly distributed points
points_list = calculate_points()

# Assign to our output variables
sphere = rs.AddSphere(center_point, radius)
normal_vectors = get_normal_vectors(sphere, points_list)
points = points_list

# Error checking analysis
distances = check_distances(points_list)
calc_min_max(distances)