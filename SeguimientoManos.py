import math
import cv2
import mediapipe as mp
import time

class detectormanos():

    def __init__(self, mode=False, maxManos=2, Confdeteccion=1, Confsegui=0.5):
        self.mode = mode
        self.maxManos = maxManos
        self.Confdeteccion = Confdeteccion
        self.Confsegui = Confsegui

        self.mpmanos = mp.solutions.hands
        self.manos = self.mpmanos.Hands(self.mode, self.maxManos, self.Confdeteccion, self.Confsegui)
        self.dibujo = mp.solutions.drawing_utils
        self.tip = [4, 8, 12, 16, 20]

    def encontrarmanos(self, frame, dibujar=True):
        imgcolor = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.resultados = self.manos.process(imgcolor)

        if self.resultados.multi_hand_landmarks:
            for mano in self.resultados.multi_hand_landmarks:
                if dibujar:
                    self.dibujo.draw_landmarks(frame, mano, self.mpmanos.HAND_CONNECTIONS)
        return frame

    def encontrarposicion(self, frame, ManoNum=0, dibujar=True):
        xlista = []
        ylista = []
        bbox = []
        self.lista = []

        if self.resultados.multi_hand_landmarks and len(self.resultados.multi_hand_landmarks) > ManoNum:
            miMano = self.resultados.multi_hand_landmarks[ManoNum]

            for id, lm in enumerate(miMano.landmark):
                alto, ancho, c = frame.shape
                cx, cy = int(lm.x * ancho), int(lm.y * alto)
                xlista.append(cx)
                ylista.append(cy)
                self.lista.append([id, cx, cy])

                if dibujar:
                    cv2.circle(frame, (cx, cy), 5, (0, 0, 0), cv2.FILLED)

            xmin, xmax = min(xlista), max(xlista)
            ymin, ymax = min(ylista), max(ylista)
            bbox = xmin, ymin, xmax, ymax

            if dibujar:
                cv2.rectangle(frame, (xmin - 20, ymin - 20), (xmax + 20, ymax + 20), (0, 255, 0), 2)

        return self.lista, bbox

    import math

    def dedosarriba(self, lista_mano, ManoNum=0):
        dedos = []

        if lista_mano:
            mano = lista_mano
            pulgar = mano[self.tip[0]][1:]  # Coordenadas x, y del pulgar
            dedo_indice = mano[self.tip[1]][1:]  # Coordenadas x, y del dedo índice
            pulgar_base = mano[0][1:]  # Coordenadas x, y de la base del pulgar
            pulgar_medio = [(pulgar[0] + pulgar_base[0]) // 2, (
                        pulgar[1] + pulgar_base[1]) // 2]  # Coordenadas x, y del punto medio entre el pulgar y su base
            dedo_medio = mano[self.tip[2]][1:]  # Coordenadas x, y del dedo medio
            muñeca = mano[0][1:]  # Coordenadas x, y de la muñeca

            # Calcular ángulos entre los diferentes puntos
            angulo_pulgar = math.degrees(math.atan2(pulgar[1] - pulgar_medio[1], pulgar[0] - pulgar_medio[0]))
            angulo_indice = math.degrees(math.atan2(dedo_indice[1] - muñeca[1], dedo_indice[0] - muñeca[0]))
            angulo_medio = math.degrees(math.atan2(dedo_medio[1] - muñeca[1], dedo_medio[0] - muñeca[0]))

            # Determinar si el pulgar está levantado basándose en los ángulos
            if angulo_pulgar < 0:
                angulo_pulgar += 360
            if angulo_indice < 0:
                angulo_indice += 360
            if angulo_medio < 0:
                angulo_medio += 360

            if ManoNum == 0:  # Mano izquierda
                if angulo_pulgar < angulo_indice:
                    dedos.append(1)
                else:
                    dedos.append(0)
            else:  # Mano derecha
                if angulo_pulgar > angulo_indice:
                    dedos.append(1)
                else:
                    dedos.append(0)

        for id in range(1, 5):
            if lista_mano and self.tip[id] < len(lista_mano) and self.tip[id] - 2 >= 0:
                if lista_mano[self.tip[id]][2] < lista_mano[self.tip[id] - 2][2]:
                    dedos.append(1)
                else:
                    dedos.append(0)
            else:
                dedos.append(0)

        return dedos

