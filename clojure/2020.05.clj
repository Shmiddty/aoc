(use '[io :rename {read-all-lines yummy debug dbg}])

; https://stackoverflow.com/a/5058544
(defn exp [x n] (reduce * (repeat n x)))

(defn binstr [string zero] (map #(if (= zero %) 0 1) string))

(defn binsrch [[head & tail]]
  (if (= 0 (count tail))
    head
    (+ (* head (exp 2 (count tail))) (binsrch tail))
  ))

(def inp
  (->> (yummy)
       (map #(re-seq #"([FB]+)([LR]+)" %))
       (map #(rest (first %)))
       (map #(vector (binstr (first %) \F) (binstr (second %) \L)))
       (map #(map binsrch %))
       (map #(+ (* 8 (first %)) (second %)))
       ))

(->> inp
     (apply max)
     (println)
     )

; assumes collection is sorted and consecutive (except for the missing element)
(defn missing [[head & tail]]
  (if (= (+ 1 head) (first tail))
    (missing tail)
    (+ 1 head)
    ))

(->> inp
     (sort)
     (missing)
     (println)
     )
