import pygame
import random
from pygame.locals import QUIT, MOUSEBUTTONDOWN
import matplotlib.pyplot as plt

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
LIGHT_GRAY = (220, 220, 220)
OPTION_GAP = 150
OPTIONS_Y_START = HEIGHT // 2 - 50

formulas = {
    "sin(2\\theta)": "2sin(\\theta)cos(\\theta)",
    "cos(2\\theta)": "cos^2(\\theta) - sin^2(\\theta)",
    "tan(2\\theta)": "\\frac{2tan(\\theta)}{1-tan^2(\\theta)}",
    "\\frac{d}{dx} sin(\\theta)": "cos(\\theta)",
    "\\frac{d}{dx} cos(\\theta)": "-sin(\\theta)",
    "\\frac{d}{dx} tan(\\theta)": "sec^2(\\theta)",
    "\\frac{d}{dx} csc(\\theta)": "-csc(\\theta)cot(\\theta)",
    "\\frac{d}{dx} sec(\\theta)": "sec(\\theta)tan(\\theta)",
    "\\frac{d}{dx} cot(\\theta)": "-csc^2(\\theta)",
    "sin^2(\\frac{\\theta}{2})": "\\frac{1-cos(\\theta)}{2}",
    "cos^2(\\frac{\\theta}{2})": "\\frac{1+cos(\\theta)}{2}",
    "tan^2(\\frac{\\theta}{2})": "\\frac{1-cos(\\theta)}{1+cos(\\theta)}",
    "sin(A + B)": "sin(A)cos(B) + cos(A)sin(B)",
    "sin(A - B)": "sin(A)cos(B) - cos(A)sin(B)",
    "cos(A + B)": "cos(A)cos(B) - sin(A)sin(B)",
    "cos(A - B)": "cos(A)cos(B) + sin(A)sin(B)",
    "tan(A + B)": "\\frac{tan(A) + tan(B)}{1 - tan(A)tan(B)}",
    "tan(A - B)": "\\frac{tan(A) - tan(B)}{1 + tan(A)tan(B)}",
    # ... More formulas can be added as needed
}

font = pygame.font.Font(None, 36)

def latex_to_pygame(text, size=20, fgcolor=BLACK):
    """Render LaTeX text to a Pygame surface using Matplotlib."""
    import matplotlib
    matplotlib.use('Agg')  # Ensure the Agg backend is used

    fig, ax = plt.subplots(figsize=(5, 1))
    ax.text(0.5, 0.5, "$%s$" % text, size=size, ha="center", va="center", color=fgcolor)
    ax.axis("off")

    canvas = fig.canvas
    canvas.draw()
    image = canvas.renderer.buffer_rgba()
    width, height = canvas.get_width_height()
    surface = pygame.image.fromstring(image.tobytes(), (width, height), "RGBA")

    plt.close(fig)

    return surface

def pygame_color_to_mpl(pygame_color):
    """Convert a Pygame RGB color to a Matplotlib RGB format."""
    return tuple([x / 255.0 for x in pygame_color])


def show_options(screen, question, correct_answer, options):
    screen.fill(LIGHT_GRAY)
    question_surface = latex_to_pygame(question, size=50)
    screen.blit(question_surface, question_surface.get_rect(center=(WIDTH // 2, HEIGHT // 5)))

    option_rects = []
    for i, option in enumerate(options):
        option_surface = latex_to_pygame(option, fgcolor=pygame_color_to_mpl(BLUE))
        o_rect = option_surface.get_rect(center=(WIDTH // 2, OPTIONS_Y_START + i * OPTION_GAP))
        option_rects.append(o_rect.inflate(20, 10))
        pygame.draw.rect(screen, WHITE, option_rects[-1])
        pygame.draw.rect(screen, BLACK, option_rects[-1], 2)
        screen.blit(option_surface, o_rect)

    pygame.display.flip()
    return option_rects


def display_feedback(screen, question, feedback_text, color=RED):
    screen.fill(WHITE)
    question_surface = latex_to_pygame(question)
    feedback_surface = font.render(feedback_text, True, color)
    screen.blit(question_surface, question_surface.get_rect(center=(WIDTH // 2, HEIGHT // 3)))
    screen.blit(feedback_surface, feedback_surface.get_rect(center=(WIDTH // 2, 2 * HEIGHT // 3)))

    pygame.display.flip()
    pygame.time.wait(1000)



MAX_WRONG_QUESTIONS = 5  # Adjust this value as needed


def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Trig Memorization Game")

    clock = pygame.time.Clock()
    running = True
    score = 0

    # Initialize wrong questions list
    recent_wrong_questions = []

    while running:
        # Adjust question selection
        if recent_wrong_questions and random.random() < 0.5:  # 50% chance to pick from wrong questions
            question = random.choice(recent_wrong_questions)
        else:
            question = random.choice(list(formulas.keys()))

        correct_answer = formulas[question]
        options = random.sample(list(set(formulas.values()) - {correct_answer}), 2) + [correct_answer]
        random.shuffle(options)
        option_rects = show_options(screen, question, correct_answer, options)

        answered = False
        while not answered:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                    answered = True
                elif event.type == MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    for i, rect in enumerate(option_rects):
                        if rect.collidepoint(x, y):
                            if options[i] == correct_answer:
                                score += 10
                                display_feedback(screen, question, "Correct!", GREEN)
                                # Correct answer, remove from wrong questions list if present
                                if question in recent_wrong_questions:
                                    recent_wrong_questions.remove(question)
                            else:
                                display_feedback(screen, question, "Wrong!", RED)


                                # Wrong answer, add to the list if not present
                                if question not in recent_wrong_questions:
                                    recent_wrong_questions.append(question)
                                    # Ensure list doesn't grow indefinitely
                                    if len(recent_wrong_questions) > MAX_WRONG_QUESTIONS:
                                        recent_wrong_questions.pop(0)
                            answered = True
                            break

        clock.tick(30)

    pygame.quit()


if __name__ == "__main__":
    main()
