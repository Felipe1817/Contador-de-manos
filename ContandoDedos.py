import cv2
import SeguimientoManos as sm

detector = sm.detectormanos(Confdeteccion=1)
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    frame = detector.encontrarmanos(frame)

    # Mano izquierda
    lista_mano_izquierda, bbox_izquierda = detector.encontrarposicion(frame, ManoNum=0, dibujar=False)
    dedos_izquierda = detector.dedosarriba(lista_mano_izquierda)
    contar_izquierda = dedos_izquierda.count(1)

    # Mano derecha
    lista_mano_derecha, bbox_derecha = detector.encontrarposicion(frame, ManoNum=1, dibujar=False)
    dedos_derecha = detector.dedosarriba(lista_mano_derecha, ManoNum=1)
    contar_derecha = dedos_derecha.count(1)

    # Total de dedos
    total_dedos = contar_izquierda + contar_derecha

    cv2.putText(frame, f'Izquierda: {contar_izquierda}', (10, 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
    cv2.putText(frame, f'Derecha: {contar_derecha}', (10, 100), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
    cv2.putText(frame, f'Total: {total_dedos}', (10, 150), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)

    cv2.imshow("Manos", frame)
    k = cv2.waitKey(1)

    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
