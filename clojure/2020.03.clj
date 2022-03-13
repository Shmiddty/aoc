(use '[io :rename {read-all-lines yummy}])

(def inp
  (->> (yummy)
       (map str)
       (map cycle)
       ))

(defn trees [forest [x, y]]
  (->> (take (/ (count forest) y) (range))
       (rest)
       (map #(vector (* x %) (* y %)))
       (map #(nth (nth inp (second %)) (first %)))
       (filter #(= \# %))
       (count)
       ))

; Part 1
(->> (trees inp [3 1])
     (println)
     )

; Part 2
(->> [[1 1] [3 1] [5 1] [7 1] [1 2]]
     (map #(trees inp %))
     (reduce *)
     (println)
     )

