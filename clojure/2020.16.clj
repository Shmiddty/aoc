(use '[clojure.string :only (split, includes?)])
(use '[io :rename {read-all yummy, printI printI}])
(use '[util :only (fargo)])
(use '[enum :only (zip, enumerate)])

(def numbers #(map read-string (re-seq #"\d+" %)))

(def inp
  (->> (yummy)
       (#(split % #"\n\n"))
       (map #(split % #"\n"))
       (apply (fargo
          (partial map #(concat [(first (split % #":"))] (numbers %)))
          #(numbers (second %))
          #(map numbers (rest %))
          ))
       ))

(defn isvalidvalue [value [field a b c d]]
  (or (and (<= a value) (>= b value)) (and (<= c value) (>= d value)))
  )

(->> (last inp)
     (mapcat (partial filter #(not-any? (partial isvalidvalue %) (first inp))))
     (reduce +)
     (println)
     )

; kinda sloppy here, eh?
(defn deduce [poss]
  (loop [solved [] remaining (sort-by #(count (second %)) (enumerate poss))]
    (if (empty? remaining)
      solved
      (->> (rest remaining)
           (map (partial apply (fargo
             identity
             (partial filter #(not= % (first (second (first remaining)))))
             )))
           (sort-by #(count (second %)))
           (recur (concat solved [(apply (fargo identity first) (first remaining))]))
           ))
    ))

(->> (last inp)
     (filter (partial every? #(some (partial isvalidvalue %) (first inp))))
     (apply zip)
     (map
       (fn [fvals]
         (map
           first
           (filter
             (fn [field] (every? #(isvalidvalue % field) fvals))
             (first inp)
             ))
         ))
     (deduce)
     (filter #(includes? (second %) "departure"))
     (map first)
     (map (partial nth (second inp)))
     (reduce *)
     (println)
     )
