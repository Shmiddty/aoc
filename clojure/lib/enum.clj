(ns enum)

; flatten by one level
(defn flat [ls]
  (apply conj [] ls))

(defn pairs [[head & tail]]
  (if (empty? tail)
    []
    (apply conj (map #(vector head %) tail) (pairs tail))))

(defn combinations [N ls]
  (if (or (> N (count ls)) (= 0 N) (empty? ls))
    []
    (if (= N 1)
      (map vector ls) ; this bit is ugly but I'm too much of a noob to think of a better way to do this
      (->> ls
           (rest)
           (combinations N)
           (apply conj (map #(apply conj [(first ls)] %) (combinations (- N 1) (rest ls))))
      )
    )
  )
)

(defn has [v ls] (< 0 (count (filter #(= v %) ls))))

