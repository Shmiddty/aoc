(use '[io :rename {read-all yummy, printI printI}])
(use '[enum :only (enumerate, slice)])

(def inp (map read-string (re-seq #"\d+" (yummy))))

(defn to-map [inp] (->> inp
  (enumerate)
  (map #(hash-map (second %) [(inc (first %))]))
  (apply merge)
))

(defn step [[state n o]] (
  (fn [N] [
    (merge state { N (take 2 (concat [(inc o)] (get state N []))) })
    N
    (inc o)
  ])
  (apply - (take 2 (concat (get state n [0 0]) [o])))
))

(->> inp
     (to-map)
     (#(iterate step [% (last inp) (count inp)]))
     (#(nth % (- 2020 (count inp))))
     (second)
     (println)
     )

(->> inp
     (to-map)
     (#(iterate step [% (last inp) (count inp)]))
     (#(nth % (- 30000000 (count inp))))
     (second)
     (println)
     )
