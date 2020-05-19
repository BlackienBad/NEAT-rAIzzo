# Autore: Carlo Parisi
import neat
import os
import pygame
import random


class Razzo:
    """
    La classe razzo rappresenta il personaggio, ha degli attributi statici come:
    tempo di animazione, che serve per dare il tempo al cambio delle immagini
    imgs che è il vettore di immagini definite fuori dalla classe come razzo_img
    """
    def __init__(self, x, y):
        """
        Inizializza l'oggetto razzo

        Args:
        x (int): posizione x iniziale del razzo
        y (int): posizione y iniziale del razzo
        """
        self.TEMPO_ANIMAZIONE = 5
        self.IMGS = [
        pygame.transform.scale2x(pygame.image.load(os.path.abspath(os.path.join("imgs", "razzo" + str(x) + ".png"))))
        for x in
        range(1, 4)]
        self.x = x
        self.y = y
        self.giro = 0  # degrees to tilt
        self.contatore_tick = 0
        self.vel = 0
        self.altezza = self.y
        self.img_contatore = 0
        self.img = self.IMGS[0]

    def vola(self):
        """
        Fa volare il razzo rendendo la sua velocità negativa
        """
        self.vel = -7
        self.contatore_tick = 0
        self.altezza = self.y

    def muovi_razzo(self):
        """
        Fa muovere il razzo #da controllare
        """
        self.contatore_tick += 1

        # for downward acceleration
        dislocamento = self.vel * self.contatore_tick + 0.5 * 3 * (
            self.contatore_tick) ** 2  # calculate displacement

        # terminal velocity
        if dislocamento >= 16:
            dislocamento = (dislocamento / abs(dislocamento)) * 16

        if dislocamento < 0:
            dislocamento -= 2

        self.y = self.y + dislocamento

    def disegna_razzo(self, win):
        """
        disegna il razzo

        Args:
            win (pygame.Surface): una window pygame
        """
        self.img_contatore += 1

        # For animation of bird, loop through three images
        if self.img_contatore <= self.TEMPO_ANIMAZIONE:
            self.img = self.IMGS[0]
        elif self.img_contatore <= self.TEMPO_ANIMAZIONE * 2:
            self.img = self.IMGS[1]
        elif self.img_contatore <= self.TEMPO_ANIMAZIONE * 3:
            self.img = self.IMGS[2]
        elif self.img_contatore <= self.TEMPO_ANIMAZIONE * 4:
            self.img = self.IMGS[1]
        elif self.img_contatore == self.TEMPO_ANIMAZIONE * 4 + 1:
            self.img = self.IMGS[0]
            self.img_contatore = 0

        # so when bird is nose diving it isn't flapping
        if self.giro <= -80:
            self.img = self.IMGS[1]
            self.img_contatore = self.TEMPO_ANIMAZIONE * 2

        # tilt the bird
        win.blit(self.img, (round(self.x), round(self.y)))

    def get_mask(self):
        """
        Prende la mask del razzo, questo per calcolare le collisioni in maniera più precisa

        Returns:
             pygame.mask.Mask: una maschera contentente una matrice che indica quali pixel dell'oggetto razzo
        sono visivamente occupati e quali no
        """
        return pygame.mask.from_surface(self.img)


class Spina:
    """
    Rappresenta un oggetto Spina
    """
    def __init__(self, x):
        """
        Inizializza l'oggetto spina

        Args:
            x (int): posizione x della spina
        """
        self.distanza = 150 # distanza tra le due spine
        self.VEL = 6 # velocità di movimento delle spine
        self.x = x
        self.altezza = 0
        self.su = 0
        self.giu = 0
        self.spine_img = pygame.transform.scale2x(
            pygame.image.load(os.path.abspath(os.path.join("imgs", "spina.png"))).convert_alpha())

        self.SPINA_SU = pygame.transform.flip(self.spine_img, False,
                                              True)  # girando l'immagine per ottenere la spina di sopra
        self.SPINA_GIU = self.spine_img

        self.superata = False

        self.set_height()

    def set_height(self):
        """
        Fa il set della posizione della spina
        """
        self.altezza = random.randrange(50, 450)
        self.su = self.altezza - self.SPINA_SU.get_height()
        self.giu = self.altezza + self.distanza

    def muovi_spine(self):
        """
        Muove le spine basandosi sulla velocità (VEL)
        """
        self.x -= self.VEL

    def disegna_spine(self, win):
        """
        Disegna la spina di sopra e la spina di sotto

        Args:
            win (pygame.Surface): una window pygame
        """
        # draw top
        win.blit(self.SPINA_SU, (self.x, self.su))
        # draw bottom
        win.blit(self.SPINA_GIU, (self.x, self.giu))

    def collisioni(self, razzo):
        """
        Controlla le collisioni

        Args:
            razzo (Razzo): un oggetto razzo

        Returns:
            Bool: un booleano, true se il razzo ha avuto una collisione con una delle due spine, falso altrimenti
        """
        razzo_mask = razzo.get_mask()
        mask_su = pygame.mask.from_surface(self.SPINA_SU)
        mask_giu = pygame.mask.from_surface(self.SPINA_GIU)
        offsett_su = (self.x - razzo.x, self.su - round(razzo.y))
        offset_giu = (self.x - razzo.x, self.giu - round(razzo.y))

        punto_giu = razzo_mask.overlap(mask_giu, offset_giu)
        punto_su = razzo_mask.overlap(mask_su, offsett_su)

        if punto_giu or punto_su:
            return True

        return False


class Pavimento:
    """
    Rappresenta il pavimento che si muove, serve a controllare quando il razzo è sceso troppo e non può risalire
    """

    def __init__(self, y):
        """
        Inizializza l'oggeto pavimento

        Args:
            y (int): altezza del pavimento
        """
        self.VEL = 5
        self.IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")).convert_alpha())
        self.LARGHEZZA = self.IMG.get_width()
        self.y = y
        self.x1 = 0
        self.x2 = self.LARGHEZZA

    def muovi_pavimento(self):
        """
        Crea due immagini identiche del pavimento che si muovono verso sinistra in maniera ciclica per dare una
        sensazione di movimento
        """
        self.x1 -= self.VEL
        self.x2 -= self.VEL
        if self.x1 + self.LARGHEZZA < 0:
            self.x1 = self.x2 + self.LARGHEZZA

        if self.x2 + self.LARGHEZZA < 0:
            self.x2 = self.x1 + self.LARGHEZZA

    def disegna_pavimento(self, win):
        """
        Disegna il pavimento

        Args:
            win (pygame.Surface): una window pygame
        """
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))


class Window:
    """
    classe che contiene il metodo principale per la visualizzazione del progetto
    """
    def __init__(self):
        pass

    def disegna_window(self, win, razzi, spine, pavimento, punteggio, gen, spine_index, scoremassimo, fitnessmassimo,
                       fitnessattuale):
        """
        disegna la finestra per visualizzare il gioco e tutte le sue componenti

        Args:
             win (pygame.Surface): una window pygame
             razzi (list): lista di razzi da visualizzare
             spine (list): lista di spine da visualizzare
             pavimento (Pavimento): oggetto pavimento da visualizzare
             punteggio (int): punteggio attuale
             gen (int): generazione attuale
             spine_index (int): intero che controlla quale insieme di spine è il prossimo da superare
             scoremassimo (int): punteggio massimo della partita in corso
             fitnessmassimo (int): fitness massimo della partita in corso
             fitnessattuale (int): fitness attuale
        """
        win_larghezza = 600
        disegna_linee = True
        pygame.font.init()
        stat_font = pygame.font.SysFont("comicsans", 50)
        if gen == 0:
            gen = 1
        bg_img = pygame.transform.scale(pygame.image.load(os.path.join("imgs", "bg.png")).convert_alpha(), (600, 900))
        win.blit(bg_img, (0, 0))

        for spina in spine:
            spina.disegna_spine(win)

        pavimento.disegna_pavimento(win)
        for razzo in razzi:
            # draw lines from razzo to spine
            if disegna_linee:
                try:
                    pygame.draw.line(win, (255, 0, 0),
                                     (round(razzo.x) + round(razzo.img.get_width() / 2),
                                      round(razzo.y) + round(razzo.img.get_height() / 2)),
                                     (round(spine[spine_index].x) + round(spine[spine_index].SPINA_SU.get_width() / 2),
                                      round(spine[spine_index].altezza)), 3)
                    pygame.draw.line(win, (255, 0, 0),
                                     (round(razzo.x) + round(razzo.img.get_width() / 2),
                                      round(razzo.y) + round(razzo.img.get_height() / 2)),
                                     (round(spine[spine_index].x) + round(spine[spine_index].SPINA_GIU.get_width() / 2),
                                      round(spine[spine_index].giu)), 3)
                except:
                    # ho messo pass e non qualche altra funzione o output con print perchè quando un razzo muore il
                    # gioco prova a disegnare linee, però ovviamente non ci riesce, e quindi pass è l'unica cosa
                    # sensata per non creare problemi/spam nella console
                    pass
            # draw razzo
            razzo.disegna_razzo(win)

        # score
        score_label = stat_font.render("Score: " + str(punteggio), 1, (255, 255, 255))
        win.blit(score_label, (win_larghezza - score_label.get_width() - 15, 10))

        # generations
        score_label = stat_font.render("Generazioni: " + str(gen - 1), 1, (255, 255, 255))
        win.blit(score_label, (10, 10))

        # alive
        score_label = stat_font.render("Vivi: " + str(len(razzi)), 1, (255, 255, 255))
        win.blit(score_label, (10, 50))

        max_score_label = stat_font.render("Score Massimo: " + str(scoremassimo), 1, (255, 255, 255))
        win.blit(max_score_label, (win_larghezza - max_score_label.get_width() - 15, 50))

        score_label = stat_font.render("Fitness Attuale: " + str("{:.2f}".format(fitnessattuale)), 1, (255, 255, 255))
        win.blit(score_label, (10, 90))

        score_label = stat_font.render("Fitness Massimo: " + str("{:.2f}".format(fitnessmassimo)), 1, (255, 255, 255))
        win.blit(score_label, (10, 130))

        pygame.display.update()


class Genomi:
    """
    Classe che contiene il metodo principale per l'intelligenza artificiale
    """
    def __init__(self):
        pass

    def eval_genomes(genomi, config):
        """
        Effettua la simulazione sulla popolazione corrente di razzi e setta il loro fitness in base ai parametri
        scelti, ovvero, in base a quanta distanza raggiungono

        Args:
            genomi (list): lista di genomi per l'algoritmo NEAT
            config (Config): oggetto config per il funzionamento dell'algoritmo
        """
        gen = 0
        win_larghezza = 600
        win = pygame.display.set_mode((600, 800))
        scoremassimo = 0
        fitnessmassimo = 0
        gen += 1

        # start by creating lists holding the genome itself, the
        # neural network associated with the genome and the
        # razzo object that uses that network to play
        nets = []
        razzi = []
        ge = []
        for genome_id, genome in genomi:
            genome.fitness = 0  # start with fitness level of 0
            net = neat.nn.FeedForwardNetwork.create(genome, config)
            nets.append(net)
            razzi.append(Razzo(230, 350))
            ge.append(genome)

        pavimento = Pavimento(730)
        spine = [Spina(700)]
        score = 0
        currentfitness = 0

        clock = pygame.time.Clock()

        run = True
        while run and len(razzi) > 0:
            clock.tick(30)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                    quit()
                    break

            spine_index = 0
            if len(razzi) > 0:
                if len(spine) > 1 and razzi[0].x > spine[0].x + spine[0].SPINA_SU.get_width():
                    # determine whether to use the first or second
                    spine_index = 1  # spina on the screen for neural network input

            for x, razzo in enumerate(razzi):  # give each razzo a fitness of 0.1 for each frame it stays alive
                ge[x].fitness += 0.1
                if ge[x].fitness > currentfitness:
                    currentfitness = ge[x].fitness
                if ge[x].fitness > fitnessmassimo:
                    fitnessmassimo = ge[x].fitness
                razzo.muovi_razzo()

                # send razzo location, top spina location and bottom spina location and determine from network
                # whether to jump or not
                output = nets[razzi.index(razzo)].activate(
                    (razzo.y, abs(razzo.y - spine[spine_index].altezza), abs(razzo.y - spine[spine_index].giu)))

                if output[0] > 0.5:  # we use a tanh activation function so result will be between -1 and 1. if over 0.5
                    # jump
                    razzo.vola()

            pavimento.muovi_pavimento()

            lista_spine = []
            nuove_spine = False
            for spina in spine:
                spina.muovi_spine()
                # check for collision
                for razzo in razzi:
                    if spina.collisioni(razzo):
                        ge[razzi.index(razzo)].fitness -= 1
                        nets.pop(razzi.index(razzo))
                        ge.pop(razzi.index(razzo))
                        razzi.pop(razzi.index(razzo))

                if spina.x + spina.SPINA_SU.get_width() < 0:
                    lista_spine.append(spina)

                if not spina.superata and spina.x < razzo.x:
                    spina.superata = True
                    nuove_spine = True

            if nuove_spine:
                score += 1
                if score > scoremassimo:
                    scoremassimo = score
                # can add this line to give more reward for passing through a spina (not required)
                for genome in ge:
                    genome.fitness += 5
                spine.append(Spina(win_larghezza))

            for r in lista_spine:
                spine.remove(r)

            for razzo in razzi:
                if razzo.y + razzo.img.get_height() - 10 >= 730 or razzo.y < -50:
                    nets.pop(razzi.index(razzo))
                    ge.pop(razzi.index(razzo))
                    razzi.pop(razzi.index(razzo))
            window = Window()
            window.disegna_window(win, razzi, spine, pavimento, score, gen, spine_index, scoremassimo, fitnessmassimo,
                                  currentfitness)


if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.

    def fit(config_file):
        """
        Runna l'algoritmo NEAT per fare training sulla rete neurale e giocare a rAIzzo

        Args:
            config_file (str): dove si trova il file di configurazione per l'algoritmo
        """
        config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                    neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                    config_file)

        # Create the population, which is the top-level object for a NEAT run.
        popolazione = neat.Population(config)

        # Add a stdout reporter to show progress in the terminal.
        popolazione.add_reporter(neat.StdOutReporter(True))
        stats = neat.StatisticsReporter()
        popolazione.add_reporter(stats)
        # popolazione.add_reporter(neat.Checkpointer(5))

        # Run for up to 50 generations.
        genomi = Genomi
        vincitore = popolazione.run(genomi.eval_genomes, 50)

        # show final stats
        print('\nMiglior Genoma:\n{!s}'.format(vincitore))


    dir_locale = os.path.dirname(__file__)
    path_configurazione = os.path.join(dir_locale, 'config-feedforward.txt')
    fit(path_configurazione)
