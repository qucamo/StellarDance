from __future__ import annotations
import time
import math
import pygame
import sys, json

fps = 120
k = 1000000  # meters in one pixel
mouse_x, mouse_y = 0, 0
time_speed = 5000  # default time acceleration

G = 6.67 / 10 ** 11
MS = 1.989 * 10 ** 30
RS = 696_340_000
AE = 149_597_870_700


class Star:
    def __init__(self, x: float, y: float, r: float, m: float, color: str) -> None:
        self.x = x
        self.y = y
        self.r = r
        self.mass = m
        self.color = color
        self.speed = [0, 0]
        self.force = [0, 0]
        self.status = True
        self.trace_count = 0
        self.trace = []

    def update_coordinates(self) -> None:
        self.speed[0] += (self.force[0] / self.mass) * time_speed ** 2 / fps ** 2
        self.speed[1] += (self.force[1] / self.mass) * time_speed ** 2 / fps ** 2

        self.x += self.speed[0]
        self.y += self.speed[1]

        self.trace_count += (self.speed[0] ** 2 + self.speed[1] ** 2) ** 0.5
        if self.trace_count / k >= 7:
            self.trace_count = 0
            self.trace.append((self.x, self.y))
        if len(self.trace) > 1000:
            self.trace.pop(0)

    def roche_radius(self, other: Star) -> float:
        q = other.mass / self.mass
        numerator = 0.49 * q ** (-2 / 3)
        denumerator = 0.6 * q ** (-2 / 3) + math.log(1 + q ** (-1 / 3))
        r = math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)
        return r * numerator / denumerator

    def draw_mass_exchange(self, other: Star) -> None:
        pygame.draw.line(
            screen,
            other.color,
            ((other.x - mouse_x) / k - other.r / k, (other.y - mouse_y) / k),
            ((self.x - mouse_x) / k + self.r / k, (self.y - mouse_y) / k),
            2,
        )

    def draw(self) -> None:
        pygame.draw.circle(screen, self.color, ((self.x - mouse_x) / k, (self.y - mouse_y) / k), self.r / k)
        for i in self.trace:
            pygame.draw.circle(screen, self.color, ((i[0] - mouse_x) / k, (i[1] - mouse_y) / k), 1)


def update_forces(stars: list[Star], collides: list[tuple[int]], exchanges: list[tuple[int]]) -> None:
    for i in range(len(stars)):
        for j in range(i + 1, len(stars)):
            dif_x = stars[j].x - stars[i].x
            dif_y = stars[j].y - stars[i].y
            d = (dif_x ** 2 + dif_y ** 2) ** 0.5
            f = G * stars[i].mass * stars[j].mass / d ** 2

            stars[i].force[0] += dif_x * f / d
            stars[i].force[1] += dif_y * f / d
            stars[j].force[0] -= dif_x * f / d
            stars[j].force[1] -= dif_y * f / d

            if stars[i].r + stars[j].r > d:
                collides.append((i, j))
                continue

            if stars[i].mass > stars[j].mass and stars[i].r + stars[j].r > stars[i].roche_radius(stars[j]):
                exchanges.append((i, j))
                continue


def remove_collides(stars: list[Star], collides: list[tuple[int, int]]) -> None:
    for i in collides:
        p1 = stars[i[0]]
        p2 = stars[i[1]]
        if p1.status and p2.status:
            if p1.mass > p2.mass:
                new_star = Star(p1.x, p1.y, p1.r + p2.r, p1.mass + p2.mass, p1.color)
            else:
                new_star = Star(p2.x, p2.y, p1.r + p2.r, p1.mass + p2.mass, p2.color)

            new_star.speed = [
                (p1.mass * p1.speed[0] + p2.mass * p2.speed[0]) / (p1.mass + p2.mass),
                (p1.mass * p1.speed[1] + p2.mass * p2.speed[1]) / (p1.mass + p2.mass),
            ]

            stars.append(new_star)
            p1.status = p2.status = False


def exchange_masses(stars: list[Star], exchanges: list[tuple[int]]) -> None:
    for i in exchanges:
        s1 = stars[i[0]]
        s2 = stars[i[1]]
        if s1.status and s2.status:
            amount = s2.mass * 1e-6
            s2.r -= amount * (s2.r / s2.mass)
            s2.mass -= amount
            s1.r += amount * (s1.r / s1.mass)
            s1.mass += amount
            s1.draw_mass_exchange(s2)


def simulate_one_tick(stars: list[Star]) -> list[Star]:
    collides = []
    exchanges = []
    update_forces(stars, collides, exchanges)
    remove_collides(stars, collides)
    exchange_masses(stars, exchanges)

    new_stars = []
    for star in stars:
        if star.status:
            star.update_coordinates()
            star.force = [0, 0]
            new_stars.append(star)
            star.draw()
    return new_stars


def two_body(custom_stars=None) -> list[Star]:
    if custom_stars:
        s1_data, s2_data = custom_stars
        s1 = Star(0, 19_591_000, s1_data["radius"], s1_data["mass"], s1_data["color"])
        s2 = Star(0, 0, s2_data["radius"], s2_data["mass"], s2_data["color"])
    else:
        s1 = Star(0, 19_591_000, 606_000, 1.52e21, 'gray')
        s2 = Star(0, 0, 1_188_000, 1.303e22, 'brown')

    s1.speed[0] += 210 * time_speed / fps
    s2.speed[0] += -24 * time_speed / fps
    return [s1, s2]


def three_body(custom_stars=None) -> list[Star]:
    if custom_stars:
        s1_data, s2_data, s3_data = custom_stars
        s1 = Star(0, 0.074 * AE, s1_data["radius"], s1_data["mass"], s1_data["color"])
        s2 = Star(0, -0.074 * AE, s2_data["radius"], s2_data["mass"], s2_data["color"])
        s3 = Star(2 * AE, 2 * AE, s3_data["radius"], s3_data["mass"], s3_data["color"])
    else:
        s1 = Star(0, 0.074 * AE, 2.84 * RS, 2.27 * MS, 'blue')
        s2 = Star(0, -0.074 * AE, 2.85 * RS, 2.30 * MS, 'yellow')
        s3 = Star(2 * AE, 2 * AE, 0.8 * RS, 4.4 * MS, 'green')

    s1.speed[0] += 51_000 * time_speed / fps
    s2.speed[0] += -51_000 * time_speed / fps
    s3.speed[0] += -10_000 * time_speed / fps
    s3.speed[1] += -5_000 * time_speed / fps
    return [s3, s2, s1]


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((800, 450))
    pygame.display.set_caption("Stellar Dance Simulation")
    style = pygame.font.SysFont("arial", 36)
    render_fps = style.render('fps ' + str(fps), True, 'blue')

    custom_config = None
    if len(sys.argv) > 1:
        try:
            with open(sys.argv[1], "r") as f:
                custom_config = json.load(f)
        except Exception as e:
            print("Could not load config:", e)

    if custom_config:
        user_time_speed = custom_config.get("time_speed", 5000)
        globals()["time_speed"] = user_time_speed
        stars_data = custom_config.get("stars", [])
        if len(stars_data) == 2:
            stars = two_body(stars_data)
        elif len(stars_data) == 3:
            stars = three_body(stars_data)
        else:
            stars = two_body()
    else:
        stars = two_body()

    tick = 0
    tm = time.time()
    running = True
    while running:
        tick += 1
        if tick == 100:
            tick = 0
            render_fps = style.render("fps:" + str(int(100 / (time.time() - tm))), True, "blue")
            tm = time.time()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                x = event.pos[0]
                y = event.pos[1]
                new_x = mouse_x + x * k
                new_y = mouse_y + y * k
                if event.button == 4:
                    k *= 0.85
                    mouse_x = new_x - x * k
                    mouse_y = new_y - y * k
                if event.button == 5:
                    k /= 0.85
                    mouse_x = new_x - x * k
                    mouse_y = new_y - y * k
            if event.type == pygame.MOUSEMOTION:
                if pygame.mouse.get_pressed()[0]:
                    mouse_x -= event.rel[0] * k
                    mouse_y -= event.rel[1] * k

        screen.fill("black")
        stars = simulate_one_tick(stars)
        screen.blit(render_fps, (10, 10))
        pygame.display.update()
    pygame.quit()


