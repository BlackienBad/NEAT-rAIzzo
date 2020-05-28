# r(AI)zzo usando NEAT

Intelligenza Artificiale che impara a giocare a un gioco platform utilizzando l'algoritmo [NEAT](http://nn.cs.utexas.edu/downloads/papers/stanley.ec02.pdf)

![r(AI)zzo gameplay](https://media.giphy.com/media/dsRLxuHfKu5jlwJ1NH/giphy.gif)

Per installare i moduli sarà sufficiente fare da cmd:
-----------------------------------------------------
``
pip3 install -r requirements
``

oppure

``
pip3 install pygame
``

``
pip3 install neat-python
``

Non serve avere un IDE
----------------------

É Possibile compilare e vedere l'intelligenza artificiale giocare sul proprio browser, con l'IDE gratuito GitPod

Warning: il modulo pygame, al momento (5/29/2020) non va bene con la versione 3.8 di python, quindi dovrete usare una versione precedente alla suddetta

Per modificare la versione di python sarà sufficiente scrivere nella console di GitPod:

``
pyenv install 3.x
``
Dove la x può stare per qualsiasi numero inferiore ad 8

``
pyenv local 3.x
``
Questo serve a switchare la versione dove si installano i moduli

E successivamente è possibile installare i moduli come spiegato sopra, bisogna fare attenzione che il python utilizzato sia effettivamente cambiato

[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/BlackienBad/NEAT-rAIzzo)
