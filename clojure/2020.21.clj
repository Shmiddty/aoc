(use '[clojure.string :only (split, join)])
(use '[clojure.set :only (union, intersection, difference)])
(use '[io :rename {read-all-lines yummy, printI dbg}])
(use '[util :only (deduce)])
(use '[enum :only (make-hash-map)])

(def inp
  (->> (yummy)
       (map #(split % #"contains"))
       (map (partial map #(set (re-seq #"\w+" %))))
       ))

(def ingredients
  (->> inp
       (map first)
       (reduce union)
       ))

(def allergens
  (->> inp
       (map second)
       (reduce union)
       ))

(def ingredigens
  (map
    (fn [a] [a, (apply intersection (map first (filter #(contains? (second %) a) inp)))])
    allergens
    ))

(def nonnergens
  (->> ingredigens
  (map second)
  (apply difference ingredients)
  ))

(->> nonnergens
     (map (fn [i] (filter #(contains? (first %) i) inp)))
     (map count)
     (reduce +)
     (println)
     )

(->> ingredigens
     (make-hash-map)
     (deduce)
     (sort-by first)
     (map second)
     (join #",")
     (println)
     )
