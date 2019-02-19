
canvas = None
cv_img = None
photo = None

corners = []
corners_visual = []

scale_value = 0.0

polys = []
cur_poly = {
    'points': [],
    'walls': [],
    'background': None,
    'area': None
}
scale = {
    'points': [],
    'length': None,
    'wall': {}
}
