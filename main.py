import pygame
import os
import neat

from bird import Bird
from pipe import Pipe
from ground import Ground
from image_scaler import image_scaler

pygame.font.init()

WIN_WIDTH = 576
WIN_HEIGHT = 800
GROUND_LEVEL = 730
DRAW_LINES = False

SCORE_FONT = pygame.font.SysFont('calibri', 50, bold=True)
BG_IMG = image_scaler(os.path.join("images", "bg.png"))

pygame.display.set_caption("Flappy Bird")

gen = 0


def draw_window(window, birds, pipes, ground, score, gen, pipe_ind):
    if gen == 0:
        gen = 1

    window.blit(BG_IMG, (0, 0))

    for pipe in pipes:
        pipe.draw(window)

    ground.draw(window)

    for bird in birds:
        # draw lines from bird to pipe
        if DRAW_LINES:
            try:
                pygame.draw.line(window, (255, 0, 0), (bird.x+bird.img.get_width()/2, bird.y + bird.img.get_height()/2), (pipes[pipe_ind].x + pipes[pipe_ind].PIPE_TOP.get_width()/2, pipes[pipe_ind].height), 5)
                pygame.draw.line(window, (255, 0, 0), (bird.x+bird.img.get_width()/2, bird.y + bird.img.get_height()/2), (pipes[pipe_ind].x + pipes[pipe_ind].PIPE_BOTTOM.get_width()/2, pipes[pipe_ind].bottom), 5)
            except:
                pass
        # draw bird
        bird.draw(window)

    score_text = SCORE_FONT.render(f"Score = {score[0]}", True, (255, 255, 255))
    window.blit(score_text, (WIN_WIDTH - 10 - score_text.get_width(), 10))

    score_label = SCORE_FONT.render("Gens: " + str(gen-1), True, (255, 255, 255))
    window.blit(score_label, (10, 10))

    score_label = SCORE_FONT.render("Alive: " + str(len(birds)), True, (255, 255, 255))
    window.blit(score_label, (10, 50))

    pygame.display.update()


def pipe_logic(window, pipes, birds, score, ge, nets):
    new_pipe = False  # Point of adding new pipe
    pipes_to_remove = []  # List of pipes to remove from the pipes list
    for pipe in pipes:
        pipe.move()

        for bird in birds:
            if pipe.collision(bird):
                ge[birds.index(bird)].fitness -= 1
                nets.pop(birds.index(bird))
                ge.pop(birds.index(bird))
                birds.pop(birds.index(bird))

        if not pipe.passed and pipe.x + pipe.PIPE_WIDTH < bird.x:
            pipe.passed = True
            new_pipe = True

        if pipe.x + pipe.PIPE_WIDTH < 0:
            pipes_to_remove.append(pipe)

    if new_pipe:
        score[0] += 1
        for genome in ge:
            genome.fitness += 5
        pipes.append(Pipe(600))

    for pipe_to_remove in pipes_to_remove:
        pipes.remove(pipe_to_remove)


def end_screen(window):
    run = True
    text_label = SCORE_FONT.render("Press Space to Restart",
                                   True,
                                   (255, 255, 255))
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                main()

        window.blit(text_label,
                    (WIN_WIDTH / 2 - text_label.get_width() / 2, 500))
        pygame.display.update()

    pygame.quit()
    quit()

def main(genomes, config):
    clock = pygame.time.Clock()
    ground = Ground(GROUND_LEVEL)
    pipes = [Pipe(600)]

    score = [0]

    nets = []
    birds = []
    ge = []

    global gen
    gen += 1

    for genome_id, genome in genomes:
        genome.fitness = 0  # start with fitness level of 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        birds.append(Bird(230, 350))
        ge.append(genome)

    window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

    run = True

    while run and len(birds) > 0:
        clock.tick(30)
        events = pygame.event.get()
        for event in events:

            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
                break

        pipe_ind = 0
        # determine whether to use the first
        # or second pipe on the screen for neural network input
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
                pipe_ind = 1

        # give each bird a fitness of 0.1 for each frame it stays alive
        for x, bird in enumerate(birds):
            ge[x].fitness += 0.1
            bird.move()

            # send bird location, top pipe location and bottom pipe location and determine from network whether to jump or not
            output = nets[birds.index(bird)].activate((bird.y, abs(bird.y - pipes[pipe_ind].height), abs(bird.y - pipes[pipe_ind].bottom)))

            if output[0] > 0.5:  # we use a tanh activation function so result will be between -1 and 1. if over 0.5 jump
                bird.jump()

        ground.move()

        pipe_logic(window, pipes, birds, score, ge, nets)

        for bird in birds:
            if bird.y + bird.image.get_height() - 10 >= GROUND_LEVEL or bird.y < -50:
                nets.pop(birds.index(bird))
                ge.pop(birds.index(bird))
                birds.pop(birds.index(bird))

        draw_window(window, birds, pipes, ground, score, gen, pipe_ind)

    # pygame.quit()
    # quit()


def run(config_file):
    """
    runs the NEAT algorithm to train a neural network to play flappy bird.
    :param config_file: location of config file
    :return: None
    """
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    # p.add_reporter(neat.Checkpointer(5))

    # Run for up to 50 generations.
    winner = p.run(main, 50)

    # show final stats
    print('\nBest genome:\n{!s}'.format(winner))


if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    run(config_path)
