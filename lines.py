import firebase_admin
from firebase_admin import credentials, firestore

firebase_admin.initialize_app(credentials.Certificate('snackbot-3fe7e-427b93f7fcc4.json'))
database = firestore.client()

def pt_lin_dist(pt, p1, p2):
    m = (p1[1] - p2[1])/(p1[0] - p2[0])
    b = m * p1[0] - p1[1]
    a = 1 / b
    b = m / b
    d = math.abs(pt[0] * a - pt[1] * b)/math.sqrt(a**2 + b**2)
    return d #don't ask, I found it online

class Line:
    @staticmethod
    def all_lines():
        points = database.collection('points')
        return list(points.get())

    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
    def clean_firebase(error_bar):
        points = database.collection('points')
        for pt in points.get():
            if pt_lin_dist((pt.x, pt.y), self.p1, self.p2) < error_bar:
                pt.reference.delete()
        points.add({'x': p1[0], 'y': p1[1], 'x_o': p2[0], 'y_o': p2[1]})
        points.add({'x': p2[0], 'y': p2[1], 'x_o': p1[0], 'y_o': p1[1]})
    def intersects(self, other):
        m1 = (self.p1[1] - self.p2[1])/(self.p1[0] - self.p2[0])
        m2 = (other.p1[1] - other.p2[1])/(other.p1[0] - other.p2[0])
        b1 = m1 * self.p1[0] - self.p1[1]
        b2 = m2 * other.p1[0] - other.p1[1]
        A1, A2 = 1/b1,  1/b2
        B1, B2 = m1/b1, m2/b2
        return A1 * B2 - B1 * A2 != 0

def best_guess(src, dest):
    path_line = Line(src, dest)
    points = database.collection('points')
    for pt in points.get():
        if Line((pt.x, pt.y), (pt.x_o, pt.y_o)).intersects(path_line):
            return [(pt.x, pt.y)] + guess_best((pt.x, pt.y), dest)
    return [dest]
