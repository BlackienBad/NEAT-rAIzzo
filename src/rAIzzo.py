# Autore: Carlo Parisi
import neat
import os
import pygame
import random


class Razzo:
    """
    La classe razzo che rappresenta il personaggio
    """

    def __init__(self, x, y):
        """
        Inizializza l'oggetto razzo

        Args:
        x (int): posizione x iniziale del razzo
        y (int): posizione y iniziale del razzo
        """
        self.TEMPO_ANIMAZIONE = 5  # tempo dell'animazione del personaggio (ciclo di immagini)
        self.IMGS = [
            pygame.transform.scale2x(
                pygame.image.load(os.path.abspath(os.path.join("imgs", "razzo" + str(x) + ".png"))))
            for x in
            range(1, 4)]  # immagini per l'animazione
        self.x = x  # posizione x del razzo
        self.y = y  # posizione y del razzo
        self.contatore_tick = 0  # ha una funzione simile a quella di un orologio, conta quanto tempo è passato da
        # quando ci muoviamo in una determinata direzione
        self.vel = 0  # velocità del razzo
        self.altezza = self.y  # altezza del razzo, ovver asse y
        self.img_contatore = 0  # contatore dell'immagine in cui ci si trova
        self.img = self.IMGS[0]  # immagine principale del razzo

    def vola(self):
        """
        Fa volare il razzo rendendo la sua velocità negativa
        """
        self.vel = -7  # la velocità diventa negativa quando si vola perchè così sale invece di scendere
        self.contatore_tick = 0
        self.altezza = self.y

    def muovi_razzo(self):
        """
        Fa muovere il razzo #da controllare
        """
        self.contatore_tick += 1

        # dislocamento serve a calcolare quanto pixel andremo su o giù in questo frame
        dislocamento = self.vel * self.contatore_tick + 0.5 * 3 * self.contatore_tick ** 2

        # il dislocamento non dovrebbe essere superiore a 16 per non scendere troppo velocemente se non si salta per
        # troppo tempo, quindi serve a rallentare la caduta
        if dislocamento >= 16:
            dislocamento = 16

        if dislocamento < 0:
            dislocamento -= 2  # serve ad avere salti più alti

        self.y = self.y + dislocamento

    def disegna_razzo(self, win):
        """
        disegna il razzo

        Args:
            win (pygame.Surface): una window pygame
        """
        self.img_contatore += 1

        # Per l'animazione del razzo, crea un loop con le 3 immagini utilizzando il tempo di animazione
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

        win.blit(self.img, (round(self.x), round(self.y)))

    def get_mask(self):
        """
        Prende la mask del razzo, questo per calcolare le collisioni in maniera più precisa

        Returns:
             pygame.mask.Mask: una maschera contentente una matrice che indica quali pixel dell'oggetto razzo
        sono visivamente occupati e quali no
        """
        return pygame.mask.from_surface(self.img)  # la maschera ci serve per controllare correttamente le collisioni


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
        self.distanza = 150  # distanza tra le due spine
        self.VEL = 6  # velocità di movimento delle spine
        self.x = x  # posizione x delle spine
        self.altezza = 0  # altezza delle spine
        self.su = 0  # parametro per la spina superiore
        self.giu = 0  # parametro per la spina inferiore
        self.spine_img = pygame.transform.scale2x(
            pygame.image.load(os.path.abspath(os.path.join("imgs", "spina.png"))).convert_alpha())  # caricamento
        # delle immagini della spina

        self.SPINA_SU = pygame.transform.flip(self.spine_img, False,
                                              True)  # girando l'immagine per ottenere la spina di sopra
        self.SPINA_GIU = self.spine_img

        self.superata = False  # bool per controllare se si è superato una spina per aumentare lo score e controllare
        # quella dopo

        self.set_height()

    def set_height(self):
        """
        Fa il set della posizione della spina
        """
        self.altezza = random.randrange(50, 450)  # altezza random della spina
        self.su = self.altezza - self.SPINA_SU.get_height()  # spina_su.get_height() ci da l'altezza dell immagine
        # spina superiore, questo, combinato con l'altezza, ci serve per posizionare il pixel 0:0 dell'immagine nel
        # punto giusto
        self.giu = self.altezza + self.distanza  # qui il concetto è molto più semplice, perchè il punto 0:0 è solo
        # l'altezza dell'altra spina + la distanza che si dovrà avere dall'altra spina

    def muovi_spine(self):
        """
        Muove le spine basandosi sulla velocità (VEL)
        """
        self.x -= self.VEL  # movimento della spina sull'asse x

    def disegna_spine(self, win):
        """
        Disegna la spina di sopra e la spina di sotto

        Args:
            win (pygame.Surface): una window pygame
        """
        win.blit(self.SPINA_SU, (self.x, self.su))
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
        mask_su = pygame.mask.from_surface(self.SPINA_SU)  # maschera della spina di su
        mask_giu = pygame.mask.from_surface(self.SPINA_GIU)  # maschera della spina di giu
        offsett_su = (self.x - razzo.x, self.su - round(razzo.y))  # distanza dal pixel più vicino del razzo a quello
        # più vicino della spina di sopra
        offset_giu = (self.x - razzo.x, self.giu - round(razzo.y))  # distanza dal pixel più vicino del razzo a quello
        # più vicino della spina di sotto

        punto_giu = razzo_mask.overlap(mask_giu, offset_giu)  # controlliamo le collisioni cercando collisione di
        # pixel tra la maschera della spina e l'offset, se non collidono la funzione fa return None, altrimenti True
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
        self.VEL = 5  # velocità dell'animazione del terreno
        self.IMG = pygame.transform.scale2x(
            pygame.image.load(os.path.join("imgs", "base.png")).convert_alpha())  # immagine del terreno
        self.LARGHEZZA = self.IMG.get_width()  # larghezza del terreno per creare una animazione fluida
        self.y = y  # altezza alla quale disegnare il terreno
        self.x1 = 0  # posizione della prima immagine
        self.x2 = self.LARGHEZZA  # posizione della seconda immagine

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
        win_larghezza = 600  # larghezza della finestra
        disegna_linee = True  # disegnare le linee dal centro del razzo alla punta delle spine
        pygame.font.init()  # inizializzazione del font
        stat_font = pygame.font.SysFont("comicsans", 50)

        if gen == 0:
            gen = 1

        bg_img = pygame.transform.scale(pygame.image.load(os.path.join("imgs", "bg.png")).convert_alpha(),
                                        (600, 900))  # immagine di background
        win.blit(bg_img, (0, 0))  # disegnare l'immagine di background

        for spina in spine:  # loop per disegnare tutte le spine
            spina.disegna_spine(win)

        pavimento.disegna_pavimento(win)
        for razzo in razzi:
            # if che utilizza la variabile disegna_linee per decidere se disegnarle
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
            razzo.disegna_razzo(win)

        # punteggio
        score_label = stat_font.render("Score: " + str(punteggio), 1, (255, 255, 255))
        win.blit(score_label, (win_larghezza - score_label.get_width() - 15, 10))

        # generazioni
        score_label = stat_font.render("Generazioni: " + str(gen - 1), 1, (255, 255, 255))
        win.blit(score_label, (10, 10))

        # vivi
        score_label = stat_font.render("Vivi: " + str(len(razzi)), 1, (255, 255, 255))
        win.blit(score_label, (10, 50))

        # punteggio massimo
        max_score_label = stat_font.render("Score Massimo: " + str(scoremassimo), 1, (255, 255, 255))
        win.blit(max_score_label, (win_larghezza - max_score_label.get_width() - 15, 50))

        # fitness attuale
        score_label = stat_font.render("Fitness Attuale: " + str("{:.2f}".format(fitnessattuale)), 1, (255, 255, 255))
        win.blit(score_label, (10, 90))

        # fitness massimo
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
        gen = 0  # generazione
        win_larghezza = 600  # larghezza della finestra
        win = pygame.display.set_mode((600, 800))  # istanzionamento della finestra da passare a disegna window
        scoremassimo = 0  # score massimo nella partita attuale
        fitnessmassimo = 0  # fitness massimo nella partita attuale
        gen += 1  # incremento della gen

        # creiamo liste che contengano il genoma, la neural network associata al genoma e l'oggetto razzo utilizzato
        nets = []
        razzi = []
        ge = []
        for genome_id, genome in genomi:
            genome.fitness = 0  # fitness inizializzato a 0, il fitness indica quanto un razzo procede nel livello,
            # più è alto il valore, meglio è andato il razzo
            net = neat.nn.FeedForwardNetwork.create(genome, config)
            nets.append(net)
            razzi.append(Razzo(230, 350))
            ge.append(genome)

        pavimento = Pavimento(730)  # istanziamento dell'oggetto pavimento
        spine = [Spina(700)]  # creazione dell'oggetto spine
        score = 0  # inizializzazione dello score
        currentfitness = 0  # inizializzazione del fitness

        clock = pygame.time.Clock()

        run = True
        while run and len(razzi) > 0:  # finchè ci sono razzi e run è true, continua a eseguire il loop di gioco
            clock.tick(30)  # abbiamo 30 tick per secondo, quindi tipo 30 fps, perchè più è potente un computer e più
            # veloce sarebbe andato il gioco, con questo tick(30) limitiamo al velocità di computer potenti

            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # se si preme la x rossa in alto a destra
                    run = False
                    pygame.quit()
                    quit()
                    break

            spine_index = 0
            if len(razzi) > 0:
                if len(spine) > 1 and razzi[0].x > spine[0].x + spine[0].SPINA_SU.get_width():
                    # se ci sono più coppie di spine, lo spine_index ci serve per decidere a quale coppia fare
                    # attenzione, 0 se quella più a sinistra, 1 se quella più a destra, al più ci saranno due coppie
                    # di spine sullo schermo
                    spine_index = 1

            for x, razzo in enumerate(razzi):  # diamo al razzo 0.1 fitness ogni frame che rimane vivo, ci sono 30
                # tick quindi 0.1*30 ogni secondo che rimane vivo
                ge[x].fitness += 0.1
                if ge[x].fitness > currentfitness:
                    currentfitness = ge[x].fitness
                if ge[x].fitness > fitnessmassimo:
                    fitnessmassimo = ge[x].fitness
                razzo.muovi_razzo()

                # mandiamo come neuroni di input la posizione del razzo, la posizione della spina di sopra e quella
                # di sotto per decidere se saltare oppure no, si potrebbe mandare anche solo il razzo e una delle due
                # spine, ma il tempo per apprendere aumenta notevolmente e i razzi tendono a rimanere vicino alla
                # spina di cui si passa la posizione
                output = nets[razzi.index(razzo)].activate(
                    (razzo.y, abs(razzo.y - spine[spine_index].altezza), abs(razzo.y - spine[spine_index].giu)))

                if output[0] > 0.5:  # utilizziamo una funzione di attivazione tanh, se il risultato è maggiore di
                    # 0.5 allora il razzo vola, altrimenti aspetta
                    razzo.vola()

            pavimento.muovi_pavimento()

            lista_spine = []
            nuove_spine = False
            for spina in spine:
                spina.muovi_spine()
                # controllo delle collisioni
                for razzo in razzi:
                    if spina.collisioni(razzo):
                        ge[razzi.index(razzo)].fitness -= 1
                        nets.pop(razzi.index(razzo))
                        ge.pop(razzi.index(razzo))
                        razzi.pop(razzi.index(razzo))

                if spina.x + spina.SPINA_SU.get_width() < 0:
                    lista_spine.append(spina)

                if not spina.superata and spina.x < razzo.x:
                    spina.superata = True  # se la spina viene superata allora ne vengono create delle altre
                    nuove_spine = True

            if nuove_spine:
                score += 1  # aumento dello score se vengono create nuove spine e quindi viene superata una spina
                if score > scoremassimo:  # aggiornamento dello score massimo
                    scoremassimo = score
                for genome in ge:
                    genome.fitness += 5  # al superamento di una spina si ottiene 5 di fitness in più
                spine.append(Spina(win_larghezza))  # mette una nuova spina al limite destro dello schermo

            for r in lista_spine:
                spine.remove(r)  # rimuove le spine vecchie

            for razzo in razzi:
                if razzo.y + razzo.img.get_height() - 10 >= 730 or razzo.y < -50:  # controllo per vedere se il razzo
                    # ha toccato il terreno o è uscito di 50 pixel verso l'alto
                    nets.pop(razzi.index(razzo))
                    ge.pop(razzi.index(razzo))
                    razzi.pop(razzi.index(razzo))
            window = Window()
            window.disegna_window(win, razzi, spine, pavimento, score, gen, spine_index, scoremassimo, fitnessmassimo,
                                  currentfitness)  # istanzia la finestra di gioco


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
        # configurando i "sub-heading" nel file config-feedforward.txt
        config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                    neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                    config_file)

        # Crea la popolazione, che è un oggetto top level per far runnare NEAT
        popolazione = neat.Population(config)

        # Aggiunto un stdout che ci da delle stats sulla popolazione nel terminale
        popolazione.add_reporter(neat.StdOutReporter(True))
        stats = neat.StatisticsReporter()
        popolazione.add_reporter(stats)

        genomi = Genomi
        vincitore = popolazione.run(genomi.eval_genomes, 50)

        # restituisce il miglior razzo e ci da informazioni su di esso
        print('\nMiglior Genoma:\n{!s}'.format(vincitore))


    dir_locale = os.path.dirname(__file__)
    path_configurazione = os.path.join(dir_locale, 'config-feedforward.txt')  # file di configurazione
    fit(path_configurazione)
