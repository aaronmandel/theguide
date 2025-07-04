import pygame

pygame.init()
W, H = 800, 400
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption('Brawlhalla 2v2 Frame Recorder')

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
MIDDLE_GREEN = (0, 200, 0)
BLUE = (50, 120, 255)
RED = (255, 60, 60)
THREAT_RADIUS = 60
THREAT_COLOR = (255, 200, 0, 90)
RADIUS = 18

font = pygame.font.SysFont('Arial', 22, bold=True)
label_font = pygame.font.SysFont('Arial', 18, bold=True)
button_font = pygame.font.SysFont('Arial', 18, bold=True)
pygame

plat_w, plat_h = 450, 30
plat_x = (W - plat_w) // 2
plat_y = 200

player_start = [
    {'label': 'A', 'color': BLUE, 'pos': [200, 100]},
    {'label': 'B', 'color': BLUE, 'pos': [300, 320]},
    {'label': 'X', 'color': RED, 'pos': [600, 100]},
    {'label': 'Y', 'color': RED, 'pos': [550, 320]},
]
players = [dict(label=p['label'], color=p['color'], pos=p['pos'][:]) for p in player_start]

frames = []
frame_idx = 0
mode = "edit"  # "edit" or "playback"
dragged = None
drag_offset = (0, 0)

def record_frame():
    global frames, players, frame_idx
    # Store current positions (deep copy)
    snapshot = [p['pos'][:] for p in players]
    frames.append(snapshot)
    frame_idx = len(frames) - 1

def reset_to_start():
    global players, frames, frame_idx, mode
    for i, p in enumerate(player_start):
        players[i]['pos'] = p['pos'][:]
    frames.clear()
    frame_idx = 0
    mode = "edit"

def goto_frame(idx):
    global frame_idx
    frame_idx = max(0, min(idx, len(frames) - 1))
    for i, p in enumerate(players):
        p['pos'] = frames[frame_idx][i][:]

# Button positions
button_w, button_h = 140, 36
next_btn = pygame.Rect(30, H-50, button_w, button_h)
play_btn = pygame.Rect(next_btn.right + 30, H-50, button_w, button_h)
reset_btn = pygame.Rect(play_btn.right + 30, H-50, button_w, button_h)
prevf_btn = pygame.Rect(play_btn.left - 50, H-50, 36, button_h)
nextf_btn = pygame.Rect(play_btn.right + 10, H-50, 36, button_h)

def draw_threat_zone(surface, x, y):
    threat = pygame.Surface((W, H), pygame.SRCALPHA)
    pygame.draw.circle(threat, THREAT_COLOR, (int(x), int(y)), THREAT_RADIUS)
    surface.blit(threat, (0, 0))

def draw():
    screen.fill(WHITE)
    # Draw middle line
    pygame.draw.line(screen, MIDDLE_GREEN, (W//2, 0), (W//2, H), 2)
    text = label_font.render("Middle Line", True, MIDDLE_GREEN)
    text_rect = text.get_rect(center=(W//2, 20))
    screen.blit(text, text_rect)

    pygame.draw.rect(screen, BLACK, (10, 10, W-20, H-20), 3)
    # Threat zones
    threat_layer = pygame.Surface((W, H), pygame.SRCALPHA)
    for p in players:
        draw_threat_zone(threat_layer, *p['pos'])
    screen.blit(threat_layer, (0, 0))
    # Draw platform
    pygame.draw.rect(screen, GRAY, (plat_x, plat_y, plat_w, plat_h))
    # Draw players
    for idx, p in enumerate(players):
        x, y = p['pos']
        border = 5 if dragged == idx else 2
        pygame.draw.circle(screen, p['color'], (int(x), int(y)), RADIUS)
        pygame.draw.circle(screen, BLACK, (int(x), int(y)), RADIUS, border)
        txt = font.render(p['label'], True, WHITE)
        text_rect = txt.get_rect(center=(int(x), int(y)))
        screen.blit(txt, text_rect)

    # Buttons
    btn_color = (230, 255, 230)
    btn_edge = (0, 150, 0)
    # Next Frame
    pygame.draw.rect(screen, btn_color, next_btn, border_radius=8)
    pygame.draw.rect(screen, btn_edge, next_btn, 2, border_radius=8)
    screen.blit(button_font.render("Next Frame", True, (0, 70, 0)), (next_btn.x + 16, next_btn.y + 7))
    # Play/Step
    pygame.draw.rect(screen, btn_color, play_btn, border_radius=8)
    pygame.draw.rect(screen, btn_edge, play_btn, 2, border_radius=8)
    if mode == "edit":
        screen.blit(button_font.render("Play", True, (0, 70, 0)), (play_btn.x + 40, play_btn.y + 7))
    else:
        screen.blit(button_font.render("Edit", True, (0, 70, 0)), (play_btn.x + 40, play_btn.y + 7))
    # Reset
    pygame.draw.rect(screen, btn_color, reset_btn, border_radius=8)
    pygame.draw.rect(screen, btn_edge, reset_btn, 2, border_radius=8)
    screen.blit(button_font.render("Reset", True, (0, 70, 0)), (reset_btn.x + 40, reset_btn.y + 7))
    # Prev/Next Frame (for playback)
    if mode == "playback" and frames:
        pygame.draw.rect(screen, btn_color, prevf_btn, border_radius=8)
        pygame.draw.rect(screen, btn_edge, prevf_btn, 2, border_radius=8)
        pygame.draw.polygon(screen, (0, 100, 0), [(prevf_btn.centerx+8, prevf_btn.y+8), (prevf_btn.centerx-8, prevf_btn.centery), (prevf_btn.centerx+8, prevf_btn.bottom-8)])
        pygame.draw.rect(screen, btn_color, nextf_btn, border_radius=8)
        pygame.draw.rect(screen, btn_edge, nextf_btn, 2, border_radius=8)
        pygame.draw.polygon(screen, (0, 100, 0), [(nextf_btn.centerx-8, nextf_btn.y+8), (nextf_btn.centerx+8, nextf_btn.centery), (nextf_btn.centerx-8, nextf_btn.bottom-8)])
    # Frame number display
    fr_label = ""
    if frames:
        fr_label = f"Frame {frame_idx+1}/{len(frames)}"
    screen.blit(button_font.render(fr_label, True, (80,80,80)), (W-170, H-45))

running = True
clock = pygame.time.Clock()
while running:
    draw()
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            if mode == "edit":
                # Next Frame
                if next_btn.collidepoint(mx, my):
                    record_frame()
                # Play
                elif play_btn.collidepoint(mx, my) and frames:
                    mode = "playback"
                    goto_frame(0)
                # Reset
                elif reset_btn.collidepoint(mx, my):
                    reset_to_start()
                else:
                    # Drag players
                    for idx, p in enumerate(players):
                        x, y = p['pos']
                        if (mx - x) ** 2 + (my - y) ** 2 <= RADIUS ** 2:
                            dragged = idx
                            drag_offset = (x - mx, y - my)
                            break
            elif mode == "playback":
                # Edit
                if play_btn.collidepoint(mx, my):
                    mode = "edit"
                # Reset
                elif reset_btn.collidepoint(mx, my):
                    reset_to_start()
                # Prev frame
                elif prevf_btn.collidepoint(mx, my) and frames:
                    goto_frame(frame_idx - 1)
                # Next frame
                elif nextf_btn.collidepoint(mx, my) and frames:
                    goto_frame(frame_idx + 1)

        elif event.type == pygame.MOUSEBUTTONUP:
            if dragged is not None:
                dragged = None
        elif event.type == pygame.MOUSEMOTION and dragged is not None and mode == "edit":
            mx, my = event.pos
            players[dragged]['pos'][0] = mx + drag_offset[0]
            players[dragged]['pos'][1] = my + drag_offset[1]
    clock.tick(60)

pygame.quit()
