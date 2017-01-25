# Funktion "polyReg" für polynomiale Regression (mit optionalen Regressionssplines
# des höchsten Grads des Polynoms)

# Parameter:
# y           abhängige Variable
# x           erklärende Variable, von der Polynome gebildet werden
# knoten      entweder NULL (default) - keine selbstgewählten Knotenpunkte
#             oder Vektor - Vektor der selbstgewählten Knotenpunkte
# autoknoten  entweder NULL (default) - keine zusätzlichen äquidist. Knoten
#             oder Vektor - Vektor für verschiedene Anzahlen von zus. äquidist.
#             Knoten
# grad        Vektor mit den Graden der Polynomialen Regression (default 1:3)

# returns:
# eine Liste mit allen Modellkombinationen von grad und Knoten (sowie einer predict-
# Funktion) sowie einer plot-Funktion, die zur grafischen Darstellung der Modelle verwendet werden
# kann. plotall liefert alle Modelle als Plot.

# Beispiele : siehe unten

polyReg = function(y, x, grad = 1:3, knoten = NULL, autoknoten = NULL){
  
  # für Ergebnisse
  res = new.env()
  
  grad = sort(grad)
  
  # Terme basteln
  terme = paste("x", 1:max(grad), sep = "")
  for (i in 1:max(grad)) assign(terme[i], x^i)
  
  # falls autoknoten nicht NULL:
  if (!is.null(autoknoten)){
    
    # Kombinationen von grad und autoknoten ausschreiben, Knotenfunktion definieren
    kombi = expand.grid(g = grad, K = autoknoten)
    
    # knoten liefert K äquidistante Knoten:
    autoknoten.fun = function(K, from = min(x), to = max(x)){
      erg = seq(from = from, to = to, length = K + 2)
      return(erg[- c(1, length(erg))])
    }
    
    # Modelle schätzen
    
    res$modelle = apply(kombi, 1, function(one){
      # Knotenpunkte sind
      knotenpunkte = sort(unique(c(autoknoten.fun(one["K"]), knoten)))
      # Splineterme basteln:
      splineterme = paste("spterm", knotenpunkte, sep ="")
      for (i in 1:length(knotenpunkte))
        assign(splineterme[i], (x - knotenpunkte[i])^one["g"] * (x > knotenpunkte[i]))
      # Formel basteln:
      formel = as.formula(paste("y ~", paste(c(terme[1:one["g"]], splineterme), collapse = "+")))
      M = lm(formel)
      # Predict-Funktion:
      predicted = function(z1){
        terme1 = sapply(z1, function(x){x^(0:one["g"])})
        terme2 = sapply(z1, function(x){(x - knotenpunkte)^one["g"] * (x > knotenpunkte)})
        return( M$coef %*% rbind(terme1, terme2) )
      }
      # Modell, Knoten und predict-Funktion zurückgeben:
      return(list(M = M, Knoten = knotenpunkte, predicted = predicted))
    }
    )
    
    # aussagekräftige Namen vergeben
    names(res$modelle) = apply(kombi, 1, function(zeile){
      paste("Modell_g=", zeile["g"], "K=", zeile["K"], sep = "")
    }
    )
    
    # Plot-Funktion für ein Modell, modellname entweder character oder numeric
    res$plot = function(modellname,  knoteneinzeichnen = TRUE, genau = 100, ...){
      if (class(modellname) == "character"){
        position = which(names(res$modelle) == modellname)
        if (length(position) == 0) {
          cat("no such model\n")
          invisible()
        }
      }
      else position = modellname
      # Daten auslesen
      this.model = res$modelle[[position]][["M"]]
      this.predicted = res$modelle[[position]][["predicted"]]
      this.knoten = res$modelle[[position]][["Knoten"]]
      # Startplot
      plot(x, y, main = paste("g = ", kombi[position, "g"], ", K = ",
                              length(this.knoten), sep = ""), ...)
      # geschätztes Modell einzeichnen
      # für Plots:
      plot.x = seq(from = min(x), to = max(x), length = genau)
      lines(plot.x, this.predicted(plot.x), col = 2)
      # R-Quadrat hinschreiben
      Rsq = format(summary(this.model)$r.squared, digits = 3)
      legend("bottomright", legend = paste("Rsq =", Rsq), bty = "n")
      # Knotenpunkte
      if (knoteneinzeichnen){
        abline(v = this.knoten, col = "gray", lty = 2)
      }
    }
    
  }
  
  # falls autoknoten NULL ist:
  else {
    kein.spline = is.null(knoten)
    # Modelle schätzen
    res$modelle = lapply(grad, function(one){
      if (!kein.spline){
        # Knotenpunkte sind
        knotenpunkte = sort(unique(knoten))
        # Splineterme basteln:
        splineterme = paste("spterm", knotenpunkte, sep ="")
        for (i in 1:length(knotenpunkte))
          assign(splineterme[i], (x - knotenpunkte[i])^one * (x > knotenpunkte[i]))
        # Modell basteln:
        formel = as.formula(paste("y ~", paste(c(terme[1:one], splineterme), collapse = "+")))
        M = lm(formel)
        # Predict-Funktion:
        predicted = function(z1){
          terme1 = sapply(z1, function(x){x^(0:one)})
          terme2 = sapply(z1, function(x){(x - knotenpunkte)^one * (x > knotenpunkte)})
          return( M$coef %*% rbind(terme1, terme2) )
        }
        # Modell, Knoten und predict-Funktion zurückgeben:
        return(list(M = M, Knoten = knotenpunkte, predicted = predicted))
      }
      else {
        # Modell basteln:
        formel = as.formula(paste("y ~", paste(terme[1:one], collapse = "+")))
        M = lm(formel)
        # predict-Funktion:
        predicted = function(z1){
          terme = sapply(z1, function(x){x^(0:one)})
          return( M$coef %*% terme )
        }
        # Modell und predict-Funktion zurückgeben:
        return(list(M = M, predicted = predicted))
      }
    }
    )
    
    # aussagekräftige Namen vergeben
    names(res$modelle) = lapply(grad, function(x){
      KBez = ifelse(kein.spline, "", paste("K=", length(res$modelle[[which(grad == x)]]$Knoten), sep = ""))
      paste("Modell_g=", x, KBez, sep = "")
    }
    )
    
    # Plot-Funktion für ein Modell, modellname entweder character oder numeric
    res$plot = function(modellname,  knoteneinzeichnen = TRUE, genau = 100, ...){
      if (class(modellname) == "character"){
        position = which(names(res$modelle) == modellname)
        if (length(position) == 0) {
          cat("no such model\n")
          invisible()
        }
      }
      else position = modellname
      # Daten auslesen
      this.model = res$modelle[[position]][["M"]]
      this.predicted = res$modelle[[position]][["predicted"]]
      if (!kein.spline) this.knoten = res$modelle[[position]][["Knoten"]]
      # Startplot
      KBez = ifelse(kein.spline, "", paste(", K = ", length(this.knoten), sep = ""))
      plot(x, y, main = paste("g = ", grad[position], KBez, sep = ""), ...)
      # geschätztes Modell einzeichnen
      plot.x = seq(from = min(x), to = max(x), length = genau)
      lines(plot.x, this.predicted(plot.x), col = 2)
      # R-Quadrat hinschreiben
      Rsq = format(summary(this.model)$r.squared, digits = 3)
      legend("bottomright", legend = paste("Rsq =", Rsq), bty = "n")
      # Knotenpunkte
      if (knoteneinzeichnen & !kein.spline){
        abline(v = this.knoten, col = "gray", lty = 2)
      }
    }
    
  }
  
  # Ausgabe aller Modelle mit plotall, wobei anordnung z.B. default c(2,4)
  # für 2*4 Grafiken ist. Sollen die Knotenpunkte eingezeichnet werden ?
  # genau gibt an, an wievielen Werten das Polynom berechnet wird.
  res$plotall = function(anordnung = c(2,4), knoten = TRUE, genau = 500, ...){
    par(mfrow = anordnung)
    for (i in 1:length(res$modelle)){
      res$plot(i, knoten, genau = genau, ...)
      if ((i %% prod(anordnung)) == 0 & i < length(res$modelle)){
        answer = readline(prompt = "Weiter (RETURN) oder Abbruch (andere Eingabe)? ")
        if (answer == "") next
        else break
      }
    }
  }
  
  
  return(as.list(res))
  
}

# Anwendung der Funktion:
daten = read.table("http://www.statistik.lmu.de/~greven/limo06/Datensatz7.txt",
                   col.names = c("Zeit.ms1", "Beschl.gr"))
attach(daten)

# ohne Splines:
c0 = polyReg(Beschl.gr, Zeit.ms1, g = 1:8)
c0$plotall(xlab = "Zeit [ms]", ylab = "Beschleunigung [gr]")

# Aufgaben:
c1 = polyReg(Beschl.gr, Zeit.ms1, g = 1:8, autoknoten = 3)
c1$plotall(xlab = "Zeit [ms]", ylab = "Beschleunigung [gr]")

c2 = polyReg(Beschl.gr, Zeit.ms1, g = 3, autoknoten = c(3,5,8,10,20))
c2$plotall(xlab = "Zeit [ms]", ylab = "Beschleunigung [gr]", anordnung = c(2,3))

# Welcher Wert wird für Zeit = 58 ms (also kurz außerhalb des Wertebereichs)
# im Modell g=3, K=20 vorhergesagt?
c2$modelle$"Modell_g=3K=20"$predicted(58)

# zufällig gewählte Knoten:
c3 = polyReg(Beschl.gr, Zeit.ms1, g = 3, knoten = runif(10, min(Zeit.ms1), max(Zeit.ms1)))
# erstes Modell (hier einziges) plotten:
c3$plot(1)