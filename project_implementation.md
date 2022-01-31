# Thema 2 - Planetensimulation

### Gruppe 5 - Adrian Knorr, Maximilian Kapra, Paul Kaiser, Simon Meier

## Anforderungsanalyse

### Art der Simulation

Anforderung an die Simulation ist eine rundenbasierte Berechnung.
Es soll eine Dynamische Simulation verwendet werden, da Prozesse in Abhängigkeit der Zeit betrachtet werden. Weil nach
statischen zeitintervallen Ereignisse hervorgerufen werden, welche den nächsten Systemzustand bestimmen, handelt es sich
hierbei um eine diskrete Simulation.

### Aufgaben des Softwaresystems

Jede Runde (Tick / Zeiteinheit) muss das Spielfeld neu berechnet werden. Das neu errechnete Spielfeld wird dann grafisch
dargestellt. Zu jeder Runde werden Daten erfasst. Diese können in Echtzeit ausgegeben und analysiert werden.

**Aufgaben der Neuberechnung:**

- Zufälliges bewegen der Tiere
- Vermehrung der Tiere unter bestimmten Vorraussetzungen
- Tod eines Tieres unter bestimmten Vorraussetzungen

**Daten zur Analyse erfassen:**

- Anzahl der einzelnen Tiere zur jeweiligen Zeit

**Darstellung des Spielfeldes:**

- Darstellung muss auch bei großen Spielfeldern performant funktionieren

**Aufgaben der Analyse:**

- Momentane Veränderungsrate (Ableitung) der einzelnen Tiere zur jeweiligen Zeit
- Fagestellungen über das Ökosystem beantworten

### Softwaretechnische Aspekte

- Darstellung des Spielfelds
  - Unterscheidung Browser und Desktop Client
  - Komponentenbasierter Aufbau
  - Stylesheets (CSS) und Objekt-Attribute

### Genutzte Softwarelösungen

Nachdem uns nicht nur die Simulation interssiert, sondern auch die Implementierung, haben wir uns dazu entschieden die
Aufgabe in verschiedenen Varianten und Programmiersprachen zu implementieren.

1)

- **Programmiersprache**: Python
- **Version**: 3.10
- **Verwendete Biliotheken**:
  - tkinter
  - matplotlib
- **Verwendete Datentypen**:
  - Die Tiere werden jeweils als eigene Klasse abgebildet.
  - Die Welt, bzw. das Netz, wird als zweidimensionales Array abgebildet.

2)

- **Programmiersprache**: React + TypeScript
- **Version**: 17
- **Verwendete Biliotheken**:
  - ChartJS
  - Tailwind CSS
- **Verwendete Datentypen**:
  - Die Tiere werden jeweils als eigene Klasse abgebildet.
  - Die Welt, bzw. das Netz, wird als zweidimensionales Array abgebildet.

3)

- **Programmiersprache**: Angular + TypeScript
- **Version**: 13.1.4
- **Verwendete Biliotheken**:
  - ngx-charts
  - Bootstrap
- **Verwendete Datentypen**:
  - Die Tiere werden jeweils als eigene Klasse abgebildet.
  - Die Welt, bzw. das Netz, wird als zweidimensionales Array abgebildet.

### Projektmanagement und weiteres Vorgehen

Als erstes muss die Arbeitsaufteilung geklärt werden. Dabei teilen wir uns in 2 Teams auf. Eines für die Implementierung
der Logik und eines für die grafische Visualisierung.

Durch die Aufteilung der Arbeit kann gleichzeitig am Projekt gearbeitet werden.

Implementierungsvarianten können zum lernen bzw. testen auch selbstständig implementiert werden.

## Implementierung

## Dokumentation

## Fragestellung

### Ist das Ökosystem stabil?

### Was bedeutet in diesem Zusammenhang Stabilität?

### Wovon hängt die Stabilität ab?

### Wie kann man die Simulation geeignet visualisieren?
